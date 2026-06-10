"""
Phase 0: SSM + Mamba Basics
============================
Teaches the core concepts of State Space Models (SSM) and the Mamba architecture.

Key concepts:
1. SimplifiedSSM: h(t) = A*h(t-1) + B*x(t), y(t) = C*h(t)
   - Linear recurrence with state transition
2. SelectiveSSM: B and C are computed from input (not fixed parameters)
   - This is the key innovation of Mamba over standard SSMs
3. MambaBlock: RMSNorm -> SelectiveSSM -> Residual -> MLP -> Residual
   - Full Mamba block with normalization and MLP
4. Complexity: Mamba processes sequences in O(n) vs Transformer's O(n^2)

No GPU or mamba-ssm package required. Pure PyTorch implementation.
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


# ============================================================================
# 1. Simplified SSM (Non-selective, fixed parameters)
# ============================================================================

class SimplifiedSSM(nn.Module):
    """
    Basic State Space Model.

    Discrete SSM recurrence:
        h(t) = A * h(t-1) + B * x(t)     (state update)
        y(t) = C * h(t)                    (output projection)

    A, B, C are LEARNED but FIXED (not input-dependent).
    This is equivalent to a linear RNN.
    """

    def __init__(self, d_model: int, d_state: int = 16):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state

        # Learnable state transition matrix (d_state, d_state)
        # Initialized near identity for stable training (HIPPO-inspired)
        self.A_log = nn.Parameter(torch.log(torch.ones(d_state) * 0.9))

        # Input projection: (d_model) -> (d_state)
        self.B = nn.Parameter(torch.randn(d_state, d_model) * 0.01)

        # Output projection: (d_state) -> (d_model)
        self.C = nn.Parameter(torch.randn(d_model, d_state) * 0.01)

        # Skip connection projection
        self.D = nn.Parameter(torch.ones(d_model))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, d_model)

        Returns:
            y: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = x.shape

        # Discretize A (exponential of log parameter)
        A = -torch.exp(self.A_log)  # (d_state,) negative for stability

        # Initialize hidden state
        h = torch.zeros(batch, self.d_state, device=x.device, dtype=x.dtype)

        outputs = []
        for t in range(seq_len):
            # h(t) = A * h(t-1) + B * x(t)
            # A is diagonal, so element-wise multiply
            h = A * h + (self.B @ x[:, t].T).T  # (batch, d_state)

            # y(t) = C * h(t)
            y_t = (self.C @ h.T).T  # (batch, d_model)

            # Add skip connection D * x(t)
            y_t = y_t + self.D * x[:, t]

            outputs.append(y_t)

        return torch.stack(outputs, dim=1)  # (batch, seq_len, d_model)


# ============================================================================
# 2. Selective SSM (Input-dependent B, C, delta)
# ============================================================================

class SelectiveSSM(nn.Module):
    """
    Selective State Space Model (Mamba's core innovation).

    Key difference from SimplifiedSSM:
        B, C, and delta (step size) are COMPUTED FROM INPUT, not fixed.
        This allows the model to selectively remember or forget information.

    Why "selective"?
        - When input is important -> large delta, meaningful B/C -> update state
        - When input is noise -> small delta, near-zero B/C -> ignore input
        - This mimics gating in LSTMs but through the SSM framework

    Complexity: O(n) for sequential processing (vs O(n^2) for Transformers)
    """

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv

        # Input projection (expands for two branches: x and z for gating)
        self.in_proj = nn.Linear(d_model, d_model * 2, bias=False)

        # Conv1d for local context (causal convolution)
        self.conv1d = nn.Conv1d(
            in_channels=d_model,
            out_channels=d_model,
            kernel_size=d_conv,
            padding=d_conv - 1,  # Causal: only look at past
            groups=d_model,  # Depthwise convolution
        )

        # SSM parameters
        self.A_log = nn.Parameter(torch.log(torch.ones(d_state) * 0.9))
        self.D = nn.Parameter(torch.ones(d_model))

        # Projection from d_model input to d_state (for B computation)
        self.B_proj = nn.Linear(d_model, d_state, bias=False)
        # Projection to compute selective C and delta from input
        self.C_delta_proj = nn.Linear(d_model, d_state + 1, bias=False)

        # Projection from d_state back to d_model
        self.dt_proj = nn.Linear(d_state, d_model, bias=False)

        # Output projection
        self.out_proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, d_model)

        Returns:
            y: (batch, seq_len, d_model)
        """
        batch, seq_len, _ = x.shape

        # Split input into two branches
        xz = self.in_proj(x)  # (batch, seq_len, d_model * 2)
        x_branch, z_branch = xz.chunk(2, dim=-1)  # Each (batch, seq_len, d_model)

        # Causal conv1d for local context
        x_conv = x_branch.transpose(1, 2)  # (batch, d_model, seq_len)
        x_conv = self.conv1d(x_conv)[:, :, :seq_len]  # Truncate for causal
        x_conv = x_conv.transpose(1, 2)  # (batch, seq_len, d_model)
        x_conv = F.silu(x_conv)  # Activation

        # Compute SELECTIVE parameters from input
        B = self.B_proj(x_conv)  # (batch, seq_len, d_state) - input-dependent B
        c_delta = self.C_delta_proj(x_conv)  # (batch, seq_len, d_state + 1)
        C = c_delta[:, :, :self.d_state]  # (batch, seq_len, d_state)
        delta = F.softplus(c_delta[:, :, -1:])  # (batch, seq_len, 1) positive

        # Discretize A with input-dependent delta
        A = -torch.exp(self.A_log)  # (d_state,)
        # Discretized: A_bar = exp(delta * A)
        A_bar = torch.exp(delta * A)  # (batch, seq_len, d_state)

        # Sequential SSM scan (O(n) complexity)
        # h(t) = A_bar(t) * h(t-1) + B(t) * x(t)
        # B(t) is (d_state,) per batch, acting as input-dependent weights
        h = torch.zeros(batch, self.d_state, device=x.device, dtype=x.dtype)
        outputs = []

        for t in range(seq_len):
            # B[:, t] shape: (batch, d_state) - controls HOW input updates state
            # x_conv[:, t] shape: (batch, d_model) - the actual input
            # B acts as a projection: each state dim gets a weighted combination
            h = A_bar[:, t] * h + B[:, t]  # (batch, d_state)

            # y(t) = C(t) * h(t) - dot product of C and h
            # C[:, t] shape: (batch, d_state), h shape: (batch, d_state)
            y_t = (C[:, t] * h).sum(dim=-1)  # (batch,)

            outputs.append(y_t)

        y = torch.stack(outputs, dim=1)  # (batch, seq_len)
        # Project from scalar per timestep back to d_model dimension
        # In real Mamba this uses the dt_proj and out_proj
        y = y.unsqueeze(-1).expand(-1, -1, self.d_model)  # (batch, seq_len, d_model)

        # Add skip connection
        y = y + self.D * x_conv

        # Gating with z_branch (like GLU)
        y = y * F.silu(z_branch)

        # Output projection
        y = self.out_proj(y)

        return y


# ============================================================================
# 3. RMSNorm (used in Mamba, lighter than LayerNorm)
# ============================================================================

class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization."""

    def __init__(self, d_model: int, eps: float = 1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d_model))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
        return x / rms * self.weight


# ============================================================================
# 4. MambaBlock: Full block with residual connections
# ============================================================================

class MambaBlock(nn.Module):
    """
    Full Mamba Block.

    Architecture (same as residual block in Transformers):
        1. RMSNorm (pre-norm)
        2. SelectiveSSM (replaces self-attention)
        3. Residual connection
        4. RMSNorm
        5. MLP (feed-forward)
        6. Residual connection

    Key difference from Transformer:
        - No self-attention (O(n^2)) -> SSM (O(n))
        - No positional encoding needed (SSM has implicit position via recurrence)
    """

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4, mlp_ratio: float = 2.0):
        super().__init__()
        self.norm1 = RMSNorm(d_model)
        self.ssm = SelectiveSSM(d_model, d_state, d_conv)
        self.norm2 = RMSNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, int(d_model * mlp_ratio)),
            nn.GELU(),
            nn.Linear(int(d_model * mlp_ratio), d_model),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # SSM with residual
        x = x + self.ssm(self.norm1(x))
        # MLP with residual
        x = x + self.mlp(self.norm2(x))
        return x


# ============================================================================
# 5. MambaEncoder: Stack of MambaBlocks
# ============================================================================

class MambaEncoder(nn.Module):
    """Stack of MambaBlocks, analogous to Transformer encoder."""

    def __init__(self, d_model: int, n_layers: int = 2, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.layers = nn.ModuleList([
            MambaBlock(d_model, d_state, d_conv) for _ in range(n_layers)
        ])
        self.norm_f = RMSNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x)
        return self.norm_f(x)


# ============================================================================
# 6. Equivalent Transformer for comparison
# ============================================================================

class TransformerBlock(nn.Module):
    """Standard Transformer block for parameter count comparison."""

    def __init__(self, d_model: int, n_heads: int = 4, mlp_ratio: float = 2.0):
        super().__init__()
        self.norm1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.norm2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, int(d_model * mlp_ratio)),
            nn.GELU(),
            nn.Linear(int(d_model * mlp_ratio), d_model),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Self-attention with residual: O(n^2) in seq_len
        attn_out, _ = self.attn(self.norm1(x), self.norm1(x), self.norm1(x))
        x = x + attn_out
        # MLP with residual
        x = x + self.mlp(self.norm2(x))
        return x


class TransformerEncoder(nn.Module):
    """Transformer encoder for parameter comparison."""

    def __init__(self, d_model: int, n_layers: int = 2, n_heads: int = 4):
        super().__init__()
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, n_heads) for _ in range(n_layers)
        ])
        self.norm_f = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x)
        return self.norm_f(x)


# ============================================================================
# 7. Demonstration
# ============================================================================

def count_parameters(model: nn.Module) -> int:
    """Count trainable parameters."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def generate_sine_data(seq_len: int, n_features: int, noise_std: float = 0.1):
    """Generate synthetic time series: sine wave + Gaussian noise."""
    t = torch.linspace(0, 4 * math.pi, seq_len).unsqueeze(1)  # (seq_len, 1)
    # Replicate to d_model dimensions with different frequencies
    frequencies = torch.linspace(0.5, 2.0, n_features).unsqueeze(0)  # (1, n_features)
    multi_signal = torch.sin(t * frequencies)  # (seq_len, n_features)
    noise = torch.randn(seq_len, n_features) * noise_std
    data = multi_signal + noise
    return data.unsqueeze(0)  # (1, seq_len, n_features)


def main():
    print("=" * 70)
    print("Phase 0: SSM + Mamba Basics")
    print("=" * 70)

    torch.manual_seed(42)

    # Configuration
    d_model = 32
    d_state = 16
    seq_len = 64
    batch_size = 2

    # ---- 1. SimplifiedSSM ----
    print("\n--- SimplifiedSSM (Fixed Parameters) ---")
    ssm = SimplifiedSSM(d_model=d_model, d_state=d_state)
    x = torch.randn(batch_size, seq_len, d_model)
    y_ssm = ssm(x)
    print(f"  Input shape:  {x.shape}")
    print(f"  Output shape: {y_ssm.shape}")
    print(f"  Parameters:   {count_parameters(ssm):,}")
    print(f"  A (state transition): diagonal, {d_state} dims")
    print(f"  State dim:    {d_state}")

    # ---- 2. SelectiveSSM ----
    print("\n--- SelectiveSSM (Input-Dependent B, C, delta) ---")
    sel_ssm = SelectiveSSM(d_model=d_model, d_state=d_state, d_conv=4)
    y_sel = sel_ssm(x)
    print(f"  Input shape:  {x.shape}")
    print(f"  Output shape: {y_sel.shape}")
    print(f"  Parameters:   {count_parameters(sel_ssm):,}")
    print("  Key: B, C, delta computed from input (selective mechanism)")

    # ---- 3. MambaBlock ----
    print("\n--- MambaBlock (RMSNorm + SSM + Residual + MLP + Residual) ---")
    mamba_block = MambaBlock(d_model=d_model, d_state=d_state)
    y_block = mamba_block(x)
    print(f"  Input shape:  {x.shape}")
    print(f"  Output shape: {y_block.shape}")
    print(f"  Parameters:   {count_parameters(mamba_block):,}")

    # ---- 4. MambaEncoder (2 blocks) ----
    print("\n--- MambaEncoder (2 stacked MambaBlocks) ---")
    mamba = MambaEncoder(d_model=d_model, n_layers=2, d_state=d_state)
    y_mamba = mamba(x)
    print(f"  Input shape:  {x.shape}")
    print(f"  Output shape: {y_mamba.shape}")
    print(f"  Parameters:   {count_parameters(mamba):,}")

    # ---- 5. Transformer comparison ----
    print("\n--- TransformerEncoder (2 blocks, for comparison) ---")
    transformer = TransformerEncoder(d_model=d_model, n_layers=2, n_heads=4)
    y_transformer = transformer(x)
    print(f"  Input shape:  {x.shape}")
    print(f"  Output shape: {y_transformer.shape}")
    print(f"  Parameters:   {count_parameters(transformer):,}")

    # ---- 6. Parameter comparison ----
    print("\n--- Parameter Count Comparison ---")
    mamba_params = count_parameters(mamba)
    transformer_params = count_parameters(transformer)
    ratio = transformer_params / mamba_params
    print(f"  MambaEncoder:      {mamba_params:>8,} params")
    print(f"  TransformerEncoder: {transformer_params:>8,} params")
    print(f"  Ratio (T/M):       {ratio:.2f}x")

    # ---- 7. Synthetic time series demo ----
    print("\n--- Synthetic Time Series (sine + noise) ---")
    ts_data = generate_sine_data(seq_len=seq_len, n_features=d_model, noise_std=0.1)
    y_ts = mamba(ts_data)
    print("  Input:  sine wave (64 steps, 32 features) + Gaussian noise")
    print(f"  Shape:  {ts_data.shape} -> {y_ts.shape}")
    print(f"  Mean output: {y_ts.mean().item():.4f}")
    print(f"  Std output:  {y_ts.std().item():.4f}")

    # ---- 8. Complexity comparison ----
    print("\n--- Complexity Analysis ---")
    print("  +------------------+----------+----------+")
    print("  | Operation         | Mamba    | Transformer |")
    print("  +------------------+----------+----------+")
    print("  | Self-Attention    | N/A      | O(n^2 * d)  |")
    print("  | SSM Scan         | O(n * d) | N/A          |")
    print("  | MLP/FFN          | O(n * d^2)| O(n * d^2) |")
    print("  | Memory (attn)    | O(1)     | O(n^2)       |")
    print("  +------------------+----------+----------+")
    print(f"  n = seq_len = {seq_len}, d = d_model = {d_model}")
    print(f"  Transformer attention: O({seq_len}^2 * {d_model}) = {seq_len**2 * d_model:,}")
    print(f"  Mamba SSM scan:       O({seq_len} * {d_model}) = {seq_len * d_model:,}")
    print(f"  Speedup factor:       {(seq_len**2 * d_model) / (seq_len * d_model):.0f}x")

    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("  1. SimplifiedSSM: Fixed params, linear recurrence (like linear RNN)")
    print("  2. SelectiveSSM:  Input-dependent B/C/delta (Mamba's innovation)")
    print("  3. Mamba processes sequences in O(n) vs Transformer's O(n^2)")
    print("  4. No positional encoding needed (implicit position via recurrence)")
    print("  5. Selective mechanism acts like LSTM gating but via SSM framework")
    print("=" * 70)


if __name__ == "__main__":
    main()
