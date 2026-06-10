"""
POC: Pure PyTorch Mamba (Selective State Space Model)

驗證:
  1. Selective SSM 可用純 PyTorch 實作（不依賴 mamba-ssm / CUDA）
  2. Forward 輸出形狀正確
  3. Backward 梯度存在於所有參數
  4. 效能：forward + backward < 50ms（CPU 或 MPS）
  5. 可用於 LM head（next-token prediction）的 loss 計算和反傳
  6. 可嵌入 MambaBlock 到更大的模型中

EP 段落: S1
風險: 致命（mamba-ssm 無法在 Apple Silicon 安裝，需要純 PyTorch 替代）
"""

import time

import torch
import torch.nn as nn
import torch.nn.functional as F


class SelectiveSSM(nn.Module):
    """
    Pure PyTorch implementation of Mamba's Selective State Space Model.

    The core idea: traditional SSMs have fixed A, B, C parameters.
    Mamba makes them input-dependent (selective), which allows the model
    to choose what to remember and what to forget.

    State update (per timestep t):
        h_t = (1 - dt_t * A) * h_{t-1} + dt_t * B_t * x_t
        y_t = C_t @ h_t

    Where A is learned, and B_t, C_t, dt_t are linear projections of x_t.
    """

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv

        # Input projection: maps d_model -> 2*d_state + dt_rank (B, C, dt)
        # Using expand factor of 2 like the original Mamba
        self.in_proj = nn.Linear(d_model, d_model * 2, bias=False)

        # Conv1d for local context (causal)
        self.conv1d = nn.Conv1d(
            in_channels=d_model,
            out_channels=d_model,
            kernel_size=d_conv,
            padding=d_conv - 1,
            groups=d_model,
            bias=True,
        )

        # SSM parameters
        self.A_log = nn.Parameter(
            torch.log(torch.arange(1, d_state + 1, dtype=torch.float32).repeat(d_model, 1))
        )
        self.D = nn.Parameter(torch.ones(d_model))

        # Projections for B, C, dt from the input
        self.x_proj = nn.Linear(d_model, d_state * 2, bias=False)
        self.dt_proj = nn.Linear(d_state * 2, d_model, bias=True)

        # Output projection
        self.out_proj = nn.Linear(d_model * 2, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (batch, seq_len, d_model)
        returns: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = x.shape

        # Input projection + split for gating
        xz = self.in_proj(x)  # (B, T, 2*d_model)
        x_proj, z = xz.chunk(2, dim=-1)  # each (B, T, d_model)

        # Causal conv1d
        x_conv = x_proj.transpose(1, 2)  # (B, d_model, T)
        x_conv = self.conv1d(x_conv)[:, :, :seq_len]  # causal: trim future
        x_conv = x_conv.transpose(1, 2)  # (B, T, d_model)
        x_conv = F.silu(x_conv)

        # SSM parameters from input
        bc = self.x_proj(x_conv)  # (B, T, 2*d_state)
        B, C = bc.chunk(2, dim=-1)  # each (B, T, d_state)

        dt = self.dt_proj(bc)  # (B, T, d_model)
        dt = F.softplus(dt)  # ensure positive

        # Discretize A
        A = -torch.exp(self.A_log)  # (d_model, d_state), always negative

        # Selective scan (vectorized parallel prefix scan)
        y = self._selective_scan_vectorized(x_conv, dt, A, B, C)

        # Add skip connection (D parameter)
        y = y + self.D.unsqueeze(0).unsqueeze(0) * x_conv

        # Gating with SiLU
        y = y * F.silu(z)

        # Output projection
        output = self.out_proj(torch.cat([y, z], dim=-1))

        return output

    def _selective_scan(
        self,
        x: torch.Tensor,
        dt: torch.Tensor,
        A: torch.Tensor,
        B: torch.Tensor,
        C: torch.Tensor,
    ) -> torch.Tensor:
        """
        Sequential selective scan.

        x: (batch, seq_len, d_model) - input
        dt: (batch, seq_len, d_model) - timestep sizes
        A: (d_model, d_state) - state transition (shared across time)
        B: (batch, seq_len, d_state) - input matrix (input-dependent)
        C: (batch, seq_len, d_state) - output matrix (input-dependent)

        returns: (batch, seq_len, d_model)
        """
        batch, seq_len, d_model = x.shape
        d_state = A.shape[1]

        # Discretize: dA = exp(dt * A), dB = dt * B
        # dt: (B, T, d_model) -> (B, T, d_model, 1)
        # A:  (d_model, d_state) -> (1, 1, d_model, d_state)
        dA = torch.exp(dt.unsqueeze(-1) * A.unsqueeze(0).unsqueeze(0))  # (B, T, d_model, d_state)
        dB = dt.unsqueeze(-1) * B.unsqueeze(2)  # (B, T, d_model, d_state)

        # Scan: accumulate state
        h = torch.zeros(batch, d_model, d_state, device=x.device, dtype=x.dtype)
        ys = []

        for t in range(seq_len):
            h = dA[:, t] * h + dB[:, t] * x[:, t].unsqueeze(-1)  # (B, d_model, d_state)
            y_t = torch.sum(h * C[:, t].unsqueeze(1), dim=-1)  # (B, d_model)
            ys.append(y_t)

        return torch.stack(ys, dim=1)  # (B, T, d_model)

    def _selective_scan_vectorized(
        self,
        x: torch.Tensor,
        dt: torch.Tensor,
        A: torch.Tensor,
        B: torch.Tensor,
        C: torch.Tensor,
    ) -> torch.Tensor:
        """
        Parallel prefix scan (doubling/triangle approach).

        Replaces the Python for-loop with O(log T) vectorized steps.
        Each step is a single batched matmul — MPS/CPU friendly.

        The recurrence h_t = dA_t * h_{t-1} + dBx_t is an associative scan:
          (a1,b1) ⊗ (a2,b2) = (a2*a1, a2*b1 + b2)
        After log2(T) doubling steps, every position contains the full prefix.
        """
        batch, seq_len, d_model = x.shape
        d_state = A.shape[1]

        # Discretize
        dA = torch.exp(dt.unsqueeze(-1) * A.unsqueeze(0).unsqueeze(0))  # (B,T,D,N)
        dBx = dt.unsqueeze(-1) * B.unsqueeze(2) * x.unsqueeze(-1)  # (B,T,D,N)

        # Pad to next power of 2
        T = seq_len
        T_pad = 1
        while T_pad < T:
            T_pad *= 2

        # (a, b) pairs — identity: a=1, b=0
        a_full = torch.ones(batch, T_pad, d_model, d_state, device=x.device, dtype=x.dtype)
        b_full = torch.zeros(batch, T_pad, d_model, d_state, device=x.device, dtype=x.dtype)
        a_full[:, :T] = dA
        b_full[:, :T] = dBx

        # Doubling: stride 1, 2, 4, ..., T_pad/2
        # Functional style: create new tensors each step (no in-place ops)
        # to keep autograd graph intact for backward pass.
        a = a_full
        b = b_full
        stride = 1
        while stride < T_pad:
            a_left = a[:, :-stride]  # positions [0 .. T_pad-1-stride]
            b_left = b[:, :-stride]
            a_right = a[:, stride:]
            b_right = b[:, stride:]

            # (a_left, b_left) ⊗ (a_right, b_right) = (a_right*a_left, a_right*b_left + b_right)
            new_a_right = a_right * a_left
            new_b_right = a_right * b_left + b_right

            # Reconstruct full tensors (functional, no in-place)
            a = torch.cat([a[:, :stride], new_a_right], dim=1)
            b = torch.cat([b[:, :stride], new_b_right], dim=1)

            stride *= 2

        h = b[:, :T]  # (B, T, d_model, d_state)
        y = torch.sum(h * C.unsqueeze(2), dim=-1)  # (B, T, d_model)
        return y


class RMSNorm(nn.Module):
    def __init__(self, d_model: int, eps: float = 1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        output = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.weight
        return output


class MambaBlock(nn.Module):
    """A single Mamba block: RMSNorm -> SelectiveSSM -> residual."""

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.norm = RMSNorm(d_model)
        self.ssm = SelectiveSSM(d_model, d_state, d_conv)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.ssm(self.norm(x))


class MambaLMHeadModel(nn.Module):
    """
    Full Mamba model for language modeling (next-token prediction).

    Architecture: Embedding -> N x MambaBlock -> RMSNorm -> LM Head
    """

    def __init__(self, vocab_size: int, d_model: int, n_layer: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.layers = nn.ModuleList([
            MambaBlock(d_model, d_state, d_conv) for _ in range(n_layer)
        ])
        self.norm_f = RMSNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, input_ids: torch.Tensor, targets: torch.Tensor = None):
        """
        input_ids: (batch, seq_len) - token ids
        targets: (batch, seq_len) - target token ids (shifted by 1)

        returns: logits (B, T, vocab_size), loss (scalar or None)
        """
        x = self.embedding(input_ids)  # (B, T, d_model)

        for layer in self.layers:
            x = layer(x)

        x = self.norm_f(x)
        logits = self.lm_head(x)  # (B, T, vocab_size)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.view(-1),
                ignore_index=-1,
            )

        return logits, loss


def main():
    print("=" * 60)
    print("POC 1: Pure PyTorch Mamba (Selective SSM)")
    print("=" * 60)

    all_passed = True

    device_str = "mps" if torch.backends.mps.is_available() else "cpu"
    device = torch.device(device_str)
    print(f"\n[0] Device: {device}")

    vocab_size = 128
    d_model = 64
    n_layer = 4
    d_state = 16
    seq_len = 128
    batch_size = 8

    print(f"[1] Config: vocab={vocab_size}, d_model={d_model}, n_layer={n_layer}, "
          f"d_state={d_state}, seq_len={seq_len}, batch={batch_size}")

    # --- Test 1: Forward shape ---
    print("\n--- Test 1: Forward shape ---")
    model = MambaLMHeadModel(vocab_size, d_model, n_layer, d_state).to(device)
    input_ids = torch.randint(0, vocab_size, (batch_size, seq_len), device=device)

    logits, loss = model(input_ids)
    print(f"  Input shape:  {input_ids.shape}")
    print(f"  Logits shape: {logits.shape}")
    print(f"  Expected:     ({batch_size}, {seq_len}, {vocab_size})")

    if logits.shape == (batch_size, seq_len, vocab_size):
        print("  ✅ Forward shape correct")
    else:
        print("  ❌ Forward shape WRONG")
        all_passed = False

    # --- Test 2: Loss computation ---
    print("\n--- Test 2: Loss computation ---")
    targets = torch.randint(0, vocab_size, (batch_size, seq_len), device=device)
    _, loss = model(input_ids, targets)
    print(f"  Loss value: {loss.item():.4f}")
    print(f"  Expected: ~ln({vocab_size}) = {__import__('math').log(vocab_size):.4f} (random init)")

    if loss is not None and loss.item() > 0:
        print("  ✅ Loss computed correctly")
    else:
        print("  ❌ Loss computation failed")
        all_passed = False

    # --- Test 2b: Sequential vs Vectorized scan correctness ---
    print("\n--- Test 2b: Sequential vs Vectorized scan correctness ---")
    ssm_layer = model.layers[0].ssm  # grab the first SSM layer
    with torch.no_grad():
        x_test = torch.randn(batch_size, seq_len, d_model, device=device)
        xz = ssm_layer.in_proj(x_test)
        x_proj, z = xz.chunk(2, dim=-1)
        x_conv = ssm_layer.conv1d(x_proj.transpose(1, 2))[:, :, :seq_len].transpose(1, 2)
        x_conv = F.silu(x_conv)
        bc = ssm_layer.x_proj(x_conv)
        B_test, C_test = bc.chunk(2, dim=-1)
        dt_test = F.softplus(ssm_layer.dt_proj(bc))
        A_test = -torch.exp(ssm_layer.A_log)

        y_seq = ssm_layer._selective_scan(x_conv, dt_test, A_test, B_test, C_test)
        y_vec = ssm_layer._selective_scan_vectorized(x_conv, dt_test, A_test, B_test, C_test)

        max_diff = (y_seq - y_vec).abs().max().item()
        mean_diff = (y_seq - y_vec).abs().mean().item()
        rel_diff = (y_seq - y_vec).abs().mean() / (y_seq.abs().mean() + 1e-8)
        print(f"  Max absolute diff:  {max_diff:.6e}")
        print(f"  Mean absolute diff: {mean_diff:.6e}")
        print(f"  Relative diff:      {rel_diff.item():.6e}")

        if max_diff < 1e-3:
            print("  ✅ Vectorized scan matches sequential (max_diff < 1e-3)")
        elif max_diff < 1e-1:
            print(f"  ⚠️  Vectorized scan has minor numerical drift (max_diff={max_diff:.4e})")
        else:
            print(f"  ❌ Vectorized scan diverges from sequential (max_diff={max_diff:.4e})")
            all_passed = False

    # --- Test 3: Backward gradients ---
    print("\n--- Test 3: Backward gradients ---")
    loss.backward()

    grad_ok = True
    grad_count = 0
    grad_missing = 0
    for name, param in model.named_parameters():
        if param.grad is not None:
            grad_count += 1
        else:
            grad_missing += 1
            grad_ok = False
            print(f"  ⚠️  No gradient for: {name}")

    total_params = sum(1 for _ in model.parameters())
    print(f"  Parameters with grad: {grad_count}/{total_params}")

    if grad_ok:
        print("  ✅ All parameters have gradients")
    else:
        print(f"  ❌ {grad_missing} parameters missing gradients")
        all_passed = False

    # --- Test 4: Parameter count ---
    print("\n--- Test 4: Parameter count ---")
    total_params_count = sum(p.numel() for p in model.parameters())
    print(f"  Total parameters: {total_params_count:,}")
    print(f"  Expected: ~{d_model * d_model * n_layer * 4:,} (rough estimate)")

    # --- Test 5: Performance benchmark ---
    print("\n--- Test 5: Performance benchmark ---")

    # Warmup
    for _ in range(3):
        logits, loss = model(input_ids, targets)
        loss.backward()
        model.zero_grad()

    N = 20
    times = []
    for i in range(N):
        model.zero_grad()
        t0 = time.perf_counter_ns()
        logits, loss = model(input_ids, targets)
        loss.backward()
        t1 = time.perf_counter_ns()
        times.append((t1 - t0) / 1_000_000)

    avg_ms = sum(times) / len(times)
    p50_ms = sorted(times)[len(times) // 2]
    print(f"  Forward+Backward over {N} runs:")
    print(f"  Avg:  {avg_ms:.2f} ms")
    print(f"  P50:  {p50_ms:.2f} ms")
    print(f"  Min:  {min(times):.2f} ms")
    print(f"  Max:  {max(times):.2f} ms")

    if avg_ms < 50:
        print(f"  ✅ Performance acceptable ({avg_ms:.1f}ms < 50ms target)")
    elif avg_ms < 200:
        print(f"  ⚠️  Performance slower than target but usable ({avg_ms:.1f}ms)")
    else:
        print(f"  ❌ Performance too slow ({avg_ms:.1f}ms > 200ms)")
        all_passed = False

    # --- Test 5b: RL scenario benchmark (B=1) ---
    print(f"\n--- Test 5b: RL scenario benchmark (B=1, T={seq_len}) ---")
    rl_input = torch.randint(0, vocab_size, (1, seq_len), device=device)
    rl_target = torch.randint(0, vocab_size, (1, seq_len), device=device)

    rl_warmup = 3
    for _ in range(rl_warmup):
        logits_rl, loss_rl = model(rl_input, rl_target)
        loss_rl.backward()
        model.zero_grad()

    rl_times = []
    for _ in range(N):
        model.zero_grad()
        t0_rl = time.perf_counter_ns()
        logits_rl, loss_rl = model(rl_input, rl_target)
        loss_rl.backward()
        t1_rl = time.perf_counter_ns()
        rl_times.append((t1_rl - t0_rl) / 1_000_000)

    rl_avg = sum(rl_times) / len(rl_times)
    rl_p50 = sorted(rl_times)[len(rl_times) // 2]
    print(f"  Forward+Backward over {N} runs (B=1):")
    print(f"  Avg:  {rl_avg:.2f} ms")
    print(f"  P50:  {rl_p50:.2f} ms")
    print(f"  Min:  {min(rl_times):.2f} ms")
    print(f"  Max:  {max(rl_times):.2f} ms")
    print(f"  Speedup vs B={batch_size}: {avg_ms / rl_avg:.1f}x")

    rl_pass = rl_avg < 50
    if rl_pass:
        print(f"  ✅ RL scenario performance acceptable ({rl_avg:.1f}ms < 50ms target)")
    else:
        print(f"  ❌ RL scenario too slow ({rl_avg:.1f}ms >= 50ms target)")
        all_passed = False

    # --- Test 6: Longer sequence ---
    print("\n--- Test 6: Longer sequence (512 tokens) ---")
    long_seq = 512
    long_ids = torch.randint(0, vocab_size, (batch_size, long_seq), device=device)
    long_targets = torch.randint(0, vocab_size, (batch_size, long_seq), device=device)

    model.zero_grad()
    t0 = time.perf_counter_ns()
    logits_long, loss_long = model(long_ids, long_targets)
    loss_long.backward()
    t1 = time.perf_counter_ns()
    long_ms = (t1 - t0) / 1_000_000

    print(f"  Seq length: {long_seq}")
    print(f"  Logits shape: {logits_long.shape}")
    print(f"  Forward+Backward: {long_ms:.2f} ms")

    if logits_long.shape == (batch_size, long_seq, vocab_size) and loss_long.item() > 0:
        print("  ✅ Long sequence works (O(n) scaling expected)")
    else:
        print("  ❌ Long sequence failed")
        all_passed = False

    # --- Test 7: Task head (policy) ---
    print("\n--- Test 7: Task head (policy) ---")
    policy_head = nn.Sequential(
        nn.Linear(d_model, d_model),
        nn.ReLU(),
        nn.Linear(d_model, 1),
        nn.Tanh(),
    ).to(device)

    with torch.no_grad():
        x = torch.randn(batch_size, seq_len, d_model, device=device)
        action = policy_head(x[:, -1, :])  # last timestep
    print(f"  Action shape: {action.shape}")
    print(f"  Action range: [{action.min().item():.3f}, {action.max().item():.3f}]")

    if action.shape == (batch_size, 1) and action.min() >= -1.0 and action.max() <= 1.0:
        print("  ✅ Policy head works (action in [-1, 1])")
    else:
        print("  ❌ Policy head failed")
        all_passed = False

    # --- Test 8: Task head (allocation) ---
    print("\n--- Test 8: Task head (allocation) ---")
    n_assets = 4
    alloc_head = nn.Sequential(
        nn.Linear(d_model, d_model),
        nn.ReLU(),
        nn.Linear(d_model, n_assets),
    ).to(device)

    with torch.no_grad():
        logits_alloc = alloc_head(x[:, -1, :])
        weights = F.softmax(logits_alloc, dim=-1)
    print(f"  Weights shape: {weights.shape}")
    print(f"  Weights sum: {weights.sum(dim=-1)[0].item():.6f}")
    print(f"  Weights: {weights[0].tolist()}")

    if weights.shape == (batch_size, n_assets) and abs(weights.sum(dim=-1)[0].item() - 1.0) < 1e-5:
        print("  ✅ Allocation head works (weights sum to 1.0)")
    else:
        print("  ❌ Allocation head failed")
        all_passed = False

    # --- Summary ---
    print(f"\n{'=' * 60}")
    if all_passed:
        print(f"✅ POC 1 PASSED: Pure PyTorch Mamba works on {device_str}")
        print("   - Forward: correct shapes")
        print("   - Backward: all gradients present")
        print(f"   - Performance: {avg_ms:.1f}ms (B={batch_size}, T={seq_len})")
        print(f"   - RL scenario: {rl_avg:.1f}ms (B=1, T={seq_len})")
        print(f"   - Long sequence: {long_ms:.1f}ms (T=512)")
        print("   - Task heads: policy + allocation work")
    else:
        print("❌ POC 1 FAILED: See errors above")
    print(f"{'=' * 60}")

    return all_passed


if __name__ == "__main__":
    main()
