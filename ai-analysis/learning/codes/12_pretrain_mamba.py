"""
Phase 2: Self-Supervised Pre-train Mamba on Market Tokens
============================================================
Teaches how to pre-train a Mamba model on discrete market token sequences
using a next-token prediction objective (like GPT pre-training).

Key concepts:
1. SimplifiedSSM / MambaBlock / MambaEncoder (copied inline from file 10)
2. Synthetic token sequences with learnable patterns
3. MambaDataset: sliding window -> (input_ids, target_ids) pairs
4. PretrainTrainer: cross-entropy loss, perplexity tracking
5. Verification: loss decreases, perplexity < vocab_size

Why pre-train? The model learns statistical regularities in market tokens
(e.g., TREND_UP often followed by TREND_UP, VOL_SURGE often follows BREAKOUT).
This learned representation can then be fine-tuned for trading decisions.
"""

import math
import random
from typing import List
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import Dataset


# ============================================================================
# 1. Mamba components (inline, no external import)
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


class SelectiveSSM(nn.Module):
    """
    Selective State Space Model (simplified Mamba core).
    h(t) = A_bar(t) * h(t-1) + B(t)
    y(t) = C(t) . h(t)
    B, C, delta are input-dependent (selective mechanism).
    """

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state

        self.in_proj = nn.Linear(d_model, d_model * 2, bias=False)
        self.conv1d = nn.Conv1d(d_model, d_model, kernel_size=d_conv,
                                padding=d_conv - 1, groups=d_model)
        self.A_log = nn.Parameter(torch.log(torch.ones(d_state) * 0.9))
        self.D = nn.Parameter(torch.ones(d_model))
        self.B_proj = nn.Linear(d_model, d_state, bias=False)
        self.C_delta_proj = nn.Linear(d_model, d_state + 1, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, seq_len, _ = x.shape
        xz = self.in_proj(x)
        x_branch, z_branch = xz.chunk(2, dim=-1)

        x_conv = x_branch.transpose(1, 2)
        x_conv = self.conv1d(x_conv)[:, :, :seq_len]
        x_conv = x_conv.transpose(1, 2)
        x_conv = F.silu(x_conv)

        B = self.B_proj(x_conv)
        c_delta = self.C_delta_proj(x_conv)
        C = c_delta[:, :, :self.d_state]
        delta = F.softplus(c_delta[:, :, -1:])

        A = -torch.exp(self.A_log)
        A_bar = torch.exp(delta * A)

        h = torch.zeros(batch, self.d_state, device=x.device, dtype=x.dtype)
        outputs = []
        for t in range(seq_len):
            h = A_bar[:, t] * h + B[:, t]
            y_t = (C[:, t] * h).sum(dim=-1)
            outputs.append(y_t)

        y = torch.stack(outputs, dim=1).unsqueeze(-1).expand(-1, -1, self.d_model)
        y = y + self.D * x_conv
        y = y * F.silu(z_branch)
        y = self.out_proj(y)
        return y


class MambaBlock(nn.Module):
    """Full Mamba block: RMSNorm -> SSM -> Residual -> RMSNorm -> MLP -> Residual."""

    def __init__(self, d_model: int, d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.norm1 = RMSNorm(d_model)
        self.ssm = SelectiveSSM(d_model, d_state, d_conv)
        self.norm2 = RMSNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.ssm(self.norm1(x))
        x = x + self.mlp(self.norm2(x))
        return x


class MambaEncoder(nn.Module):
    """Stack of MambaBlocks with final normalization."""

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
# 2. Mamba Language Model (with token embedding + output head)
# ============================================================================

class MambaForCausalLM(nn.Module):
    """
    Mamba model for causal (autoregressive) language modeling.

    Architecture:
        Token Embedding -> MambaEncoder -> LM Head (linear -> vocab logits)

    This is analogous to GPT but with Mamba blocks instead of Transformer blocks.
    Training objective: next-token prediction (cross-entropy loss).
    """

    def __init__(self, vocab_size: int, d_model: int = 64, n_layers: int = 2,
                 d_state: int = 16, d_conv: int = 4):
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model

        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.encoder = MambaEncoder(d_model, n_layers, d_state, d_conv)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

        # Weight tying: share embedding and output weights (like GPT-2)
        self.lm_head.weight = self.token_embedding.weight

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """
        Args:
            input_ids: (batch, seq_len) integer token IDs
        Returns:
            logits: (batch, seq_len, vocab_size)
        """
        x = self.token_embedding(input_ids)  # (batch, seq_len, d_model)
        x = self.encoder(x)  # (batch, seq_len, d_model)
        logits = self.lm_head(x)  # (batch, seq_len, vocab_size)
        return logits


# ============================================================================
# 3. Synthetic token sequence generator with patterns
# ============================================================================

# Token IDs (matching Phase 1 vocabulary)
PAD, BOS, EOS, SEP = 0, 1, 2, 3
STRONG_UP, TREND_UP, SIDEWAY, TREND_DOWN, STRONG_DOWN = 4, 5, 6, 7, 8
VOL_LOW, VOL_NORMAL, VOL_HIGH, VOL_EXTREME = 9, 10, 11, 12
VOL_DRY, VOL_NORMAL_VOL, VOL_ACTIVE, VOL_SURGE = 13, 14, 15, 16

# Transition patterns: given a trend token, what likely follows?
# This creates learnable structure in the synthetic data
TREND_TRANSITIONS = {
    STRONG_UP: [STRONG_UP, TREND_UP, TREND_UP, SIDEWAY],     # 75% continue up
    TREND_UP: [TREND_UP, STRONG_UP, SIDEWAY, TREND_DOWN],    # 50% continue up, 25% sideways
    SIDEWAY: [SIDEWAY, SIDEWAY, TREND_UP, TREND_DOWN],       # 50% stay sideways
    TREND_DOWN: [TREND_DOWN, STRONG_DOWN, SIDEWAY, TREND_UP], # 50% continue down
    STRONG_DOWN: [STRONG_DOWN, TREND_DOWN, TREND_DOWN, SIDEWAY], # 75% continue down
}

# Volatility tends to follow trend: strong moves -> higher vol
VOL_AFTER_TREND = {
    STRONG_UP: [VOL_HIGH, VOL_ACTIVE, VOL_ACTIVE],
    TREND_UP: [VOL_NORMAL, VOL_ACTIVE, VOL_ACTIVE],
    SIDEWAY: [VOL_LOW, VOL_NORMAL, VOL_NORMAL],
    TREND_DOWN: [VOL_NORMAL, VOL_ACTIVE, VOL_ACTIVE],
    STRONG_DOWN: [VOL_HIGH, VOL_ACTIVE, VOL_ACTIVE],
}

# Volume tends to follow volatility
VOL_REGIME_AFTER = {
    VOL_LOW: [VOL_DRY, VOL_NORMAL_VOL, VOL_NORMAL_VOL],
    VOL_NORMAL: [VOL_NORMAL_VOL, VOL_ACTIVE, VOL_NORMAL_VOL],
    VOL_ACTIVE: [VOL_ACTIVE, VOL_SURGE, VOL_ACTIVE],
    VOL_HIGH: [VOL_SURGE, VOL_ACTIVE, VOL_SURGE],
}


def generate_pattern_sequence(length: int = 30, rng: random.Random = None) -> List[int]:
    """Generate a synthetic token sequence with learnable patterns."""
    if rng is None:
        rng = random.Random()

    tokens = [BOS]
    trend = rng.choice([TREND_UP, SIDEWAY, TREND_DOWN])

    for _ in range(length):
        # Trend token (with transition pattern)
        tokens.append(trend)

        # Volatility token (conditioned on trend)
        vol = rng.choice(VOL_AFTER_TREND[trend])
        tokens.append(vol)

        # Volume token (conditioned on volatility)
        volume = rng.choice(VOL_REGIME_AFTER[vol])
        tokens.append(volume)

        tokens.append(SEP)

        # Transition to next trend
        trend = rng.choice(TREND_TRANSITIONS[trend])

    tokens.append(EOS)
    return tokens


def generate_dataset(n_sequences: int = 500, seq_length: int = 30, seed: int = 42) -> List[List[int]]:
    """Generate multiple synthetic sequences."""
    rng = random.Random(seed)
    return [generate_pattern_sequence(seq_length, rng) for _ in range(n_sequences)]


# ============================================================================
# 4. Dataset for next-token prediction
# ============================================================================

class MambaDataset(Dataset):
    """
    Sliding window dataset for next-token prediction.

    Each sample: (input_ids, target_ids) where target is shifted by 1.
    input_ids:  tokens[0:window_size]
    target_ids: tokens[1:window_size+1]
    """

    def __init__(self, sequences: List[List[int]], window_size: int = 32, stride: int = 4):
        self.window_size = window_size
        self.samples: List[Tuple[torch.Tensor, torch.Tensor]] = []

        for seq in sequences:
            # Create sliding windows with stride to control dataset size
            for start in range(0, len(seq) - window_size, stride):
                window = seq[start:start + window_size + 1]
                if len(window) == window_size + 1:
                    input_ids = torch.tensor(window[:window_size], dtype=torch.long)
                    target_ids = torch.tensor(window[1:window_size + 1], dtype=torch.long)
                    self.samples.append((input_ids, target_ids))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.samples[idx]


# ============================================================================
# 5. Trainer
# ============================================================================

class PretrainTrainer:
    """
    Trainer for next-token prediction.

    Loss: cross-entropy between predicted logits and actual next token.
    Metric: perplexity = exp(average_loss), should be < vocab_size for learning.
    """

    def __init__(self, model: MambaForCausalLM, lr: float = 1e-3):
        self.model = model
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
        self.loss_fn = nn.CrossEntropyLoss(ignore_index=PAD)

    def train_epoch(self, dataloader: DataLoader) -> Tuple[float, float]:
        """Train one epoch. Returns (avg_loss, perplexity)."""
        self.model.train()
        total_loss = 0.0
        total_tokens = 0

        for input_ids, target_ids in dataloader:
            logits = self.model(input_ids)  # (batch, seq_len, vocab_size)

            # Reshape for cross-entropy: (batch * seq_len, vocab_size) vs (batch * seq_len,)
            loss = self.loss_fn(
                logits.view(-1, self.model.vocab_size),
                target_ids.view(-1),
            )

            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()

            total_loss += loss.item() * target_ids.numel()
            total_tokens += target_ids.numel()

        avg_loss = total_loss / total_tokens if total_tokens > 0 else float("inf")
        perplexity = math.exp(avg_loss) if avg_loss < 10 else float("inf")
        return avg_loss, perplexity

    def compute_accuracy(self, dataloader: DataLoader) -> float:
        """Compute token prediction accuracy (excluding PAD)."""
        self.model.eval()
        correct = 0
        total = 0

        with torch.no_grad():
            for input_ids, target_ids in dataloader:
                logits = self.model(input_ids)
                preds = logits.argmax(dim=-1)  # (batch, seq_len)

                # Only count non-PAD tokens
                mask = target_ids != PAD
                correct += (preds[mask] == target_ids[mask]).sum().item()
                total += mask.sum().item()

        return correct / total if total > 0 else 0.0


# ============================================================================
# 6. Main: pre-train and verify
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 2: Self-Supervised Pre-train Mamba on Market Tokens")
    print("=" * 70)

    torch.manual_seed(42)
    random.seed(42)

    # Configuration
    VOCAB_SIZE = 30
    D_MODEL = 64
    N_LAYERS = 2
    D_STATE = 16
    WINDOW_SIZE = 32
    BATCH_SIZE = 64
    N_EPOCHS = 20
    LR = 3e-3

    print("\n--- Configuration ---")
    print(f"  Vocab size:   {VOCAB_SIZE}")
    print(f"  d_model:      {D_MODEL}")
    print(f"  n_layers:     {N_LAYERS}")
    print(f"  Window size:  {WINDOW_SIZE}")
    print(f"  Batch size:   {BATCH_SIZE}")
    print(f"  Epochs:       {N_EPOCHS}")
    print(f"  Learning rate:{LR}")

    # ---- Generate synthetic data ----
    print("\n--- Generating Synthetic Data ---")
    sequences = generate_dataset(n_sequences=100, seq_length=30, seed=42)
    dataset = MambaDataset(sequences, window_size=WINDOW_SIZE, stride=8)
    print(f"  Sequences: {len(sequences)}")
    print(f"  Training samples (sliding windows): {len(dataset)}")

    # Split into train/eval
    n_train = int(len(dataset) * 0.8)
    n_eval = len(dataset) - n_train
    train_dataset, eval_dataset = torch.utils.data.random_split(
        dataset, [n_train, n_eval],
        generator=torch.Generator().manual_seed(42)
    )
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    eval_loader = DataLoader(eval_dataset, batch_size=BATCH_SIZE)

    # Show a sample
    sample_input, sample_target = dataset[0]
    print(f"  Sample input:  {sample_input[:10].tolist()}...")
    print(f"  Sample target: {sample_target[:10].tolist()}...")

    # ---- Create model ----
    print("\n--- Creating MambaForCausalLM ---")
    model = MambaForCausalLM(
        vocab_size=VOCAB_SIZE,
        d_model=D_MODEL,
        n_layers=N_LAYERS,
        d_state=D_STATE,
    )
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Parameters: {n_params:,}")
    print(f"  Architecture: Embedding({VOCAB_SIZE},{D_MODEL}) -> {N_LAYERS}x MambaBlock -> LM_Head")

    # ---- Train ----
    print(f"\n--- Training ({N_EPOCHS} epochs) ---")
    trainer = PretrainTrainer(model, lr=LR)

    initial_loss = None
    final_loss = None

    for epoch in range(N_EPOCHS):
        loss, ppl = trainer.train_epoch(train_loader)

        if epoch == 0:
            initial_loss = loss
        final_loss = loss

        # Only compute accuracy every 5 epochs (expensive)
        if (epoch + 1) % 5 == 0 or epoch == 0:
            accuracy = trainer.compute_accuracy(eval_loader)
        else:
            accuracy = float("nan")

        if accuracy != accuracy:  # NaN check
            print(f"  Epoch {epoch + 1:2d}/{N_EPOCHS}: "
                  f"loss={loss:.4f}  "
                  f"ppl={ppl:.2f}")
        else:
            print(f"  Epoch {epoch + 1:2d}/{N_EPOCHS}: "
                  f"loss={loss:.4f}  "
                  f"ppl={ppl:.2f}  "
                  f"acc={accuracy:.2%}")

    # ---- Verification ----
    print("\n--- Verification ---")

    # 1. Loss decreased
    loss_decreased = final_loss < initial_loss
    print(f"  Loss decreased: {initial_loss:.4f} -> {final_loss:.4f} "
          f"({'PASS' if loss_decreased else 'FAIL'})")
    assert loss_decreased, "FAIL: Loss did not decrease!"

    # 2. Perplexity < vocab_size (model learned something)
    # Use final_loss to compute perplexity (no extra training needed)
    final_ppl = math.exp(final_loss) if final_loss < 10 else float("inf")
    ppl_ok = final_ppl < VOCAB_SIZE
    print(f"  Final perplexity: {final_ppl:.2f} < {VOCAB_SIZE} "
          f"({'PASS' if ppl_ok else 'FAIL'})")
    assert ppl_ok, f"FAIL: Perplexity {final_ppl:.2f} >= vocab_size {VOCAB_SIZE}"

    # 3. Accuracy above chance
    final_acc = trainer.compute_accuracy(eval_loader)
    chance = 1.0 / VOCAB_SIZE
    acc_ok = final_acc > chance * 5  # At least 5x random chance
    print(f"  Final accuracy: {final_acc:.2%} > {chance:.2%} (5x chance) "
          f"({'PASS' if acc_ok else 'FAIL'})")

    # ---- Show learned predictions ----
    print("\n--- Example Predictions ---")
    model.eval()
    with torch.no_grad():
        sample_input, sample_target = dataset[0]
        logits = model(sample_input.unsqueeze(0))  # (1, seq, vocab)
        preds = logits.argmax(dim=-1).squeeze(0)  # (seq,)

        TOKEN_NAMES = {
            0: "PAD", 1: "BOS", 2: "EOS", 3: "SEP",
            4: "STR_UP", 5: "TR_UP", 6: "SIDE", 7: "TR_DN", 8: "STR_DN",
            9: "V_LO", 10: "V_NORM", 11: "V_HI", 12: "V_EXT",
            13: "VOL_DRY", 14: "VOL_N", 15: "VOL_ACT", 16: "VOL_SRGE",
            17: "GAP_UP", 18: "GAP_DN", 19: "BRK_UP", 20: "BRK_DN",
            21: "REV_UP", 22: "REV_DN", 23: "NEW_HI", 24: "NEW_LO",
            25: "DOJI", 26: "HAMMER", 27: "SH_STAR", 28: "ENG_BUL", 29: "ENG BER",
        }

        print(f"  Input:     {[TOKEN_NAMES.get(t, '?') for t in sample_input[:12].tolist()]}")
        print(f"  Target:    {[TOKEN_NAMES.get(t, '?') for t in sample_target[:12].tolist()]}")
        print(f"  Predicted: {[TOKEN_NAMES.get(t, '?') for t in preds[:12].tolist()]}")
        match = (preds[:12] == sample_target[:12]).sum().item()
        print(f"  First 12 accuracy: {match}/12 = {match / 12:.0%}")

    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("  1. MambaForCausalLM: Embedding -> MambaEncoder -> LM_Head")
    print("  2. Training objective: next-token prediction (cross-entropy)")
    print("  3. Perplexity < vocab_size means model learned patterns")
    print("  4. Synthetic data has transition patterns that Mamba can learn")
    print("  5. Pre-trained weights capture market token statistics")
    print("  6. These weights transfer to downstream trading tasks (Phase 3)")
    print("=" * 70)


if __name__ == "__main__":
    main()
