# EP: Mamba Foundation Model for Multi-Task Financial RL

## 實作總覽

建立一套 Mamba-based 金融 Foundation Model 訓練框架。核心路線：

```
Pre-train Mamba（自監督學習市場動態）
  → RL fine-tune Task A：資產配置（multi-asset allocation）
  → RL fine-tune Task B：大單拆單（smart order execution）
  → RL fine-tune Task C：單資產交易（single-asset trading）
```

### 核心設計原則

1. **Pre-train → RL fine-tune**：一次 pre-train 學會市場通用表示，多個任務共享 encoder、只換 task head + reward function
2. **NT 為 RL 環境**：BacktestEngine streaming mode 當 Gym env，Portfolio API 當 reward signal，ExecAlgorithm 當執行層
3. **Mamba 的獨特價值**：O(n) 長序列處理、隱藏狀態自帶記憶（不需要手動設計 observation window）、跨資產序列輸入
4. **Event Token 而非 Raw OHLCV**：遵循 GPT 方向的核心洞察——OHLCV 是原始感測器資料，先轉換成高資訊密度 Event Token 再進模型

### 執行路徑

```
S1（基礎設施）→ S2（Tokenizer）→ S3（Pre-train）
                                    ↓
                              S4（RL Gym）
                              ↙    ↓    ↘
                        S5(Task C) S6(Task A) S7(Task B)
```

S5/S6/S7 之間無依賴，可平行開發。S4 是三者的共同前置。

### 技術棧

| 元件 | 選擇 | 理由 |
|------|------|------|
| 序列模型 | 純 PyTorch Mamba（parallel prefix scan） | mamba-ssm 無法在 macOS 安裝（需 Linux+CUDA）；純 PyTorch 實作 B=1,T=128: 18ms，滿足 RL 訓練需求 |
| RL 訓練 | PyTorch + 自建 REINFORCE | 沿用 nanochat pattern（簡化 GRPO），reward function 自訂 |
| RL 環境 | NT BacktestEngine streaming | 已 POC 驗證：ExecAlgorithm spawn_market ✅、多資產 3 instrument ✅、equity API 可用 |
| 資料來源 | NT ParquetDataCatalog + 自建 | 歷史 K 線為 pre-train 語料 |
| 訓練框架 | 自建（參考 nanochat） | 不依賴 HF transformers，保持輕量 |

### 檔案結構

```
nautilus_trader/rl/
├── __init__.py
├── mamba/
│   ├── __init__.py
│   ├── config.py              # MambaConfig, TaskHeadConfig
│   ├── model.py               # MambaEncoder, MambaPolicy
│   ├── tokenizer.py           # MarketEventTokenizer, EventVocabulary
│   └── trainer.py             # PretrainTrainer, RLTrainer
├── gym/
│   ├── __init__.py
│   ├── base.py                # NTGymBase(gymnasium.Env)
│   ├── single_asset.py        # NTSingleAssetGym(Task C)
│   ├── allocation.py          # NTAllocationGym(Task A)
│   └── execution.py           # NTExecutionGym(Task B)
├── strategies/
│   ├── __init__.py
│   ├── mamba_strategy.py      # MambaStrategy(Strategy) for Task C/A
│   └── mamba_exec_algo.py     # MambaExecAlgorithm(ExecAlgorithm) for Task B
├── data/
│   ├── __init__.py
│   ├── dataset.py             # MambaDataset for pre-train
│   └── features.py            # Feature extraction from OHLCV
└── scripts/
    ├── pretrain.py             # Pre-train entry point
    ├── rl_train.py             # RL fine-tune entry point
    └── eval.py                 # Evaluation entry point
```

---

## Scenario Matrix

| # | 場景 | 觸發 | 預期行為 | Checkpoint | 對應段 |
|---|------|------|---------|------------|--------|
| SM-1 | Pre-train 收斂 | 執行 pretrain.py | next-event prediction loss 下降，perplexity 穩定 | 最後 checkpoint | S3 |
| SM-2 | Task C 交易跑贏 buy-and-hold | rl_train.py --task trading | Mamba policy Sharpe > 1.0（BTC daily） | pre-trained weights | S5 |
| SM-3 | Task A 配置優化 Sharpe | rl_train.py --task allocation | Mamba allocation Sharpe > equal-weight | pre-trained weights | S6 |
| SM-4 | Task B 拆單減少滑價 | rl_train.py --task execution | IS < fixed TWAP IS | pre-trained weights | S7 |
| SM-5 | 無 pre-train 直接 RL | 跳過 S3 | 也能訓練但收斂慢、最終績效差 | 無 | S3 vs S5 對比 |
| SM-6 | 新資產加入 | 新增 instrument config | 只需重新 tokenize，不需改模型架構 | tokenizer state | S2 |
| SM-7 | 長序列（>1000 steps） | 多年 daily bars | Mamba O(n) 穩定，Transformer OOM | model state | S1 |
| SM-8 | 空市場資料 | 資料缺失 | assert fail + 清晰錯誤訊息 | 無 | S2 |

---

## 段落劃分原則

- 每段 self-contained：AI 只需讀該段落 + 相關 NT 原始碼就能實作
- 段落間依賴透過介面合約（function signature + data format）錨定
- S5/S6/S7 平行開發，不共享內部狀態，只共享 S1 的 model.py 和 S4 的 gym

---

## S1: Core Infrastructure — Mamba Model + Training Framework

### Context

**目標**：建立 Mamba 模型包裝層和通用訓練工具。所有下游段落（S3/S5/S6/S7）都使用這裡定義的 MambaEncoder。

**依賴**：
- 外部：`torch >= 2.0`、`gymnasium`（**不依賴 mamba-ssm**，見 EP Validate 說明）
- 內部：無（這是最底層）

> **EP Validate 驗證（POC 1）**：`mamba-ssm` 無法在 macOS Apple Silicon 安裝（需 Linux + NVIDIA GPU + CUDA）。改用純 PyTorch 實作 Selective SSM，核心為 **parallel prefix scan**（O(log T) vectorized steps），消除 Python for-loop。結果：B=8,T=128: 38ms / B=1,T=128: 18ms / T=512: 110ms，43/43 參數梯度正確，sequential vs vectorized max diff 2.98e-08。POC 檔案：`lab/poc_pure_mamba.py` ✅

**語義約束**：
- 與 S3/S5/S6/S7 共享：MambaEncoder 的輸入格式固定為 `(batch, seq_len, d_model)` float tensor
- 與 S2 共享：Event Token 的 embedding 由 MambaEncoder 內部處理，輸入為 integer token ids

**基礎設施盤點**：
- 純 PyTorch `SelectiveSSM`（parallel prefix scan）— 自行實作，`lab/poc_pure_mamba.py` 為參考
- 裝置策略：CPU/MPS 開發 + 可選 CUDA（mamba-ssm）生產加速
- NT 不提供 ML 訓練設施，全部自建

**依賴錨點**：
- `MambaEncoder` → 定義 `rl/mamba/model.py:15` / 消費 `rl/mamba/trainer.py:40`, `rl/strategies/mamba_strategy.py:30`, `rl/strategies/mamba_exec_algo.py:25`
- `MambaConfig` → 定義 `rl/mamba/config.py:10` / 消費 `rl/mamba/model.py:15`, `rl/scripts/pretrain.py:20`
- `SelectiveSSM` → 定義 `rl/mamba/ssm.py` / 消費 `rl/mamba/model.py:20`

**技術選型**：
- 純 PyTorch 實作 Selective SSM（parallel prefix scan）— 跨平台相容（CPU/MPS/CUDA），RL 場景 B=1 效能充足（18ms）
- mamba-ssm 作為**可選加速路徑**（如果未來有雲端 GPU），透過 feature flag 切換
- 訓練迴圈自建（參考 nanochat pattern）而非用 HuggingFace Trainer — 保持輕量、完全控制

**成功標準**：
- MambaEncoder 可正確 forward 一個 batch 的 token ids
- 可載入/儲存 checkpoint
- 可在 CPU/MPS/CUDA 上跑 forward + backward

### 核心實作要點

#### 1. MambaConfig

凍結 dataclass，控制模型架構。Task-specific config 透過 `task_head_type` 欄位切換。

關鍵欄位：
- `d_model`: 特徵維度（default 256）
- `n_layer`: Mamba block 層數（default 8）
- `d_state`: SSM 狀態擴展因子（default 16）
- `d_conv`: 局部卷積寬度（default 4）
- `vocab_size`: Event Token 詞彙表大小
- `seq_len`: 最大序列長度（default 512）
- `task_head_type`: "none"（pre-train）| "policy"（Task C）| "allocation"（Task A）| "execution"（Task B）

#### 2. MambaEncoder

包裝 `mamba_ssm.Mamba` block 的堆疊。支援兩種輸入模式：

```
mode A (pre-train):  token_ids (B, T) → Embedding → N × MambaBlock → output (B, T, d_model)
mode B (RL policy):  token_ids (B, T) → Embedding → N × MambaBlock → TaskHead → action
```

核心結構：
- `token_embedding`: nn.Embedding(vocab_size, d_model)
- `layers`: nn.ModuleList of MambaBlock（含 RMSNorm + residual）
- `output_norm`: RMSNorm
- `task_head`: 依 task_head_type 切換（MLP / Softmax / ExecutionHead）
- `lm_head`: 僅 pre-train 使用，nn.Linear(d_model, vocab_size)

#### 3. Task Heads

```
PolicyHead (Task C):
  (B, T, d_model) → 取最後 timestep → MLP → tanh → action in [-1, 1]
  用於連續動作空間（position sizing）

AllocationHead (Task A):
  (B, T, d_model) → 取最後 timestep → MLP → softmax → weights sum to 1.0
  用於多資產權重分配

ExecutionHead (Task B):
  (B, T, d_model) → 取最後 timestep → MLP → sigmoid × max_qty
  用於決定這一步拆多少單
```

#### 4. 訓練工具

- `setup_optimizer()`: 分離 embedding / matrix / head 參數的 learning rate（沿用 nanochat 的 MuonAdamW 思路，matrix 用 Muon，embedding/head 用 Adam）
- `save_checkpoint()` / `load_checkpoint()`: model state_dict + config
- `compute_loss()`: pre-train 用 cross-entropy，RL 用 policy gradient

### Pseudo Code

```python
class MambaEncoder(nn.Module):
    def __init__(self, config: MambaConfig):
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.layers = nn.ModuleList([
            MambaBlock(config) for _ in range(config.n_layer)
        ])
        self.norm_f = RMSNorm(config.d_model)

        if config.task_head_type == "none":
            self.lm_head = nn.Linear(config.d_model, config.vocab_size)
        elif config.task_head_type == "policy":
            self.task_head = PolicyHead(config.d_model, action_dim=1)
        elif config.task_head_type == "allocation":
            self.task_head = AllocationHead(config.d_model, n_assets=config.n_assets)
        elif config.task_head_type == "execution":
            self.task_head = ExecutionHead(config.d_model)

    def forward(self, token_ids: torch.Tensor, targets=None):
        x = self.token_embedding(token_ids)
        for layer in self.layers:
            x = layer(x) + x
        x = self.norm_f(x)

        if self.config.task_head_type == "none":
            logits = self.lm_head(x)
            if targets is not None:
                loss = F.cross_entropy(
                    logits[:, :-1].reshape(-1, logits.size(-1)),
                    targets[:, 1:].reshape(-1),
                    ignore_index=-1
                )
                return logits, loss
            return logits, None
        else:
            return self.task_head(x)


class MambaBlock(nn.Module):
    def __init__(self, config: MambaConfig):
        self.norm = RMSNorm(config.d_model)
        self.mamba = Mamba(
            d_model=config.d_model,
            d_state=config.d_state,
            d_conv=config.d_conv,
            expand=2,
        )
        self.norm2 = RMSNorm(config.d_model)
        self.mlp = nn.Sequential(
            nn.Linear(config.d_model, config.d_model * 2),
            nn.ReLU(),
            nn.Linear(config.d_model * 2, config.d_model),
        )

    def forward(self, x):
        x = x + self.mamba(self.norm(x))
        x = x + self.mlp(self.norm2(x))
        return x
```

### 驗證策略

**Example: test_mamba_encoder.py**
- 建立 MambaConfig(d_model=32, n_layer=2, vocab_size=100)
- Forward random token_ids (B=4, T=64) → 確認輸出形狀
- Forward with targets → 確認 loss 是 scalar
- Backward → 確認梯度存在
- test task_head_type="policy" → 輸出在 [-1, 1]
- test task_head_type="allocation" → 輸出 sum to 1.0

**測試計畫**：
- 單元測試：MambaEncoder 各 task_head 輸出形狀和範圍
- 單元測試：save/load checkpoint 一致性
- 整合測試：GPU 上 forward + backward（需 CUDA）

**完成檢查**：
- [ ] MambaEncoder 可 forward pre-train 模式
- [ ] MambaEncoder 可 forward policy/allocation/execution 模式
- [ ] Checkpoint save/load 正確
- [ ] 可在 CUDA 上跑通 forward + backward

---

## S2: Market Event Tokenizer

### Context

**目標**：將 OHLCV 原始資料轉換為 Event Token 序列。遵循 GPT 方向的核心洞察：OHLCV 是原始感測器資料，不是特徵。

**UC 引用**：本段定義 Event Tokenization 的核心能力。

**依賴**：
- 外部：`numpy`、`pandas`
- 內部：S1 的 MambaConfig.vocab_size（詞彙表大小由 tokenizer 決定）

**語義約束**：
- 與 S3/S5/S6/S7 共享：Event Token 是 integer，範圍 [0, vocab_size)
- 輸入：單一 Bar 的 OHLCV + 前置狀態（前一根 Bar 的 MA、前 N 根的統計量）
- 輸出：一個或多個 Event Token

**基礎設施盤點**：
- NT `Bar` 物件有 open/high/low/close/volume/ts_event
- 無既有 tokenizer — 全部自建
- 參考 GPT 方向建議的特徵清單：MA Slope、RS、Volume Ratio、Breakout State

**依賴錨點**：
- `MarketEventTokenizer` → 定義 `rl/mamba/tokenizer.py:15` / 消費 `rl/mamba/trainer.py:30`, `rl/gym/base.py:25`, `rl/data/dataset.py:20`
- `EventVocabulary` → 定義 `rl/mamba/tokenizer.py:10` / 消費 `rl/mamba/config.py:12`

**技術選型**：
- 先做離散化 tokenizer（將連續特徵分箱成 token）→ 後續可進化為 learnable tokenizer
- 特徵計算用 numpy/pandas（不用 TA-Lib，避免額外依賴）

**成功標準**：
- 給定 N 根 Bar，輸出 N 個 Event Token
- Token 分佈不極端（任一 token 佔比 < 50%）
- 同樣的輸入永遠產生同樣的 token（deterministic）

### 核心實作要點

#### 1. EventVocabulary

定義所有可能的 Event Token。每個 token 對應一個市場狀態。

```
Token 分類:

價格位置 Tokens (0-19):
  PRICE_ABOVE_MA5, PRICE_BELOW_MA5,
  PRICE_ABOVE_MA20, PRICE_BELOW_MA20,
  PRICE_NEAR_HIGH_20, PRICE_NEAR_LOW_20,
  ...

趨勢狀態 Tokens (20-39):
  TREND_UP_STRONG, TREND_UP, TREND_UP_WEAK,
  TREND_FLAT, TREND_DOWN_WEAK, TREND_DOWN, TREND_DOWN_STRONG,
  MA5_SLOPE_POS, MA5_SLOPE_NEG, MA5_SLOPE_ZERO,
  MA20_SLOPE_POS, MA20_SLOPE_NEG, MA20_SLOPE_ZERO,
  ...

波動率 Tokens (40-49):
  VOL_EXPANDING, VOL_CONTRACTING, VOL_NORMAL,
  ...

成交量 Tokens (50-59):
  VOL_SPIKE, VOL_DRY_UP, VOL_NORMAL, VOL_EXPANSION,
  ...

突破事件 Tokens (60-79):
  BREAKOUT_UP, BREAKOUT_DOWN,
  NEW_HIGH_20, NEW_LOW_20,
  PULLBACK_TO_MA, BOUNCE_FROM_MA,
  ...

相對強弱 Tokens (80-89):
  RS_STRONG, RS_WEAK, RS_NEUTRAL,
  RS_ACCEL, RS_DECEL,
  ...

特殊 Tokens:
  PAD = 0
  BOS = 1 (beginning of sequence)
  EOS = 2 (end of sequence)
  SEP = 3 (asset separator, for multi-asset sequences)
```

#### 2. Feature Extraction

從 Bar 序列計算特徵，不從單一根 Bar 計算（需要歷史統計量）。

```
features.py 計算:
  - MA(5, 20, 60) + slopes + accelerations
  - ATR(14) + relative ATR
  - Volume ratio (current / MA20_volume)
  - Price position (close relative to high/low range)
  - Return (1-bar, 5-bar, 20-bar)
  - RS (relative to benchmark, if multi-asset)
```

#### 3. MarketEventTokenizer

核心類。吃 Bar 序列，吐 Event Token 序列。

流程：
1. 累積 Bar 序列直到有足夠歷史（至少 60 根）
2. 計算所有特徵
3. 每個特徵獨立分箱 → 映射到 token 子集
4. 組合多個特徵的 token → 最終 token（用查表或組合邏輯）

設計決策：每根 Bar 產生**一個** token（而非多個）。原因是下游 Mamba 的序列是一維的。多特徵透過組合邏輯壓縮成單一 token。

### Pseudo Code

```python
class EventVocabulary:
    PAD: int = 0
    BOS: int = 1
    EOS: int = 2
    SEP: int = 3

    def __init__(self):
        self._tokens = self._build_vocabulary()

    @property
    def size(self) -> int:
        return len(self._tokens)

    def _build_vocabulary(self) -> dict[str, int]:
        tokens = {"PAD": 0, "BOS": 1, "EOS": 2, "SEP": 3}
        idx = 4

        trend_states = [
            "TREND_UP_STRONG", "TREND_UP", "TREND_UP_WEAK",
            "TREND_FLAT",
            "TREND_DOWN_WEAK", "TREND_DOWN", "TREND_DOWN_STRONG",
        ]
        for s in trend_states:
            tokens[s] = idx; idx += 1

        vol_states = ["VOL_EXPAND", "VOL_CONTRACT", "VOL_NORMAL"]
        for s in vol_states:
            tokens[s] = idx; idx += 1

        volume_states = ["V_SPIKE", "V_DRY", "V_NORMAL", "V_EXPAND"]
        for s in volume_states:
            tokens[s] = idx; idx += 1

        event_states = [
            "BREAKOUT_UP", "BREAKOUT_DOWN",
            "NEW_HIGH_20", "NEW_LOW_20",
            "PULLBACK_MA", "BOUNCE_MA",
            "CONSOLIDATION", "BREAKOUT_FAIL",
        ]
        for s in event_states:
            tokens[s] = idx; idx += 1

        return tokens

    def encode(self, name: str) -> int:
        return self._tokens.get(name, self.PAD)

    def decode(self, token_id: int) -> str:
        for name, idx in self._tokens.items():
            if idx == token_id:
                return name
        return "UNKNOWN"


class MarketEventTokenizer:
    def __init__(self, vocab: EventVocabulary):
        self.vocab = vocab
        self._history: list[Bar] = []
        self._min_history = 60

    def reset(self):
        self._history = []

    def tokenize_bar(self, bar: Bar) -> int:
        self._history.append(bar)
        if len(self._history) < self._min_history:
            return self.vocab.PAD

        closes = np.array([float(b.close) for b in self._history])
        volumes = np.array([float(b.volume) for b in self._history])
        highs = np.array([float(b.high) for b in self._history])
        lows = np.array([float(b.low) for b in self._history])

        ma5 = np.mean(closes[-5:])
        ma20 = np.mean(closes[-20:])
        atr14 = np.mean(highs[-14:] - lows[-14:])
        vol_ma20 = np.mean(volumes[-20:])

        close = closes[-1]
        volume = volumes[-1]

        trend = self._classify_trend(close, ma5, ma20, closes)
        vol_state = self._classify_volatility(highs[-14:], lows[-14:], atr14)
        volume_state = self._classify_volume(volume, vol_ma20)
        event = self._detect_event(close, highs, lows, ma5, ma20)

        token_name = f"{trend}_{vol_state}_{volume_state}"
        if event:
            token_name = event

        return self.vocab.encode(token_name)

    def tokenize_sequence(self, bars: list[Bar]) -> list[int]:
        self.reset()
        tokens = [self.vocab.BOS]
        for bar in bars:
            tokens.append(self.tokenize_bar(bar))
        tokens.append(self.vocab.EOS)
        return tokens
```

### 驗證策略

**Example: test_tokenizer.py**
- 建立合成 Bar 序列（上升趨勢、下降趨勢、盤整）
- Tokenize → 驗證上升趨勢的 token 以 TREND_UP 為主
- Tokenize → 驗證盤整的 token 以 TREND_FLAT + CONSOLIDATION 為主
- 驗證 determinism：同樣輸入兩次 tokenize 結果相同

**測試計畫**：
- 單元測試：各 _classify_* 方法
- 單元測試：完整 tokenize_bar 產出合法 token id
- 整合測試：真實 BTC daily bars 的 token 分佈（不應極端偏斜）

**完成檢查**：
- [ ] EventVocabulary 定義完整、vocab_size 可查
- [ ] 合成資料的 token 分佈符合預期
- [ ] 真實資料的 token 分佈不極端
- [ ] Deterministic

---

## S3: Pre-train — Self-Supervised Market Learning

### Context

**目標**：在歷史市場資料上自監督訓練 MambaEncoder。學到的權重作為 S5/S6/S7 RL fine-tune 的初始化。

**依賴**：
- S1: MambaEncoder、MambaConfig
- S2: MarketEventTokenizer、EventVocabulary
- 資料：歷史 K 線（BTC-USD daily 至少 5 年）

**語義約束**：
- 與 S5/S6/S7 共享：pre-trained checkpoint 的 model state_dict 格式固定
- Pre-train 後凍結 MambaEncoder 的前 N-2 層，只 fine-tune 最後 2 層 + task head

**技術選型**：
- 自回歸語言模型目標（next-event prediction）— 預測下一個 Event Token
- 不用 masked LM — 金融序列是因果的，不用雙向注意力

**成功標準**：
- Training loss 收斂（從初始 ~ln(vocab_size) 下降至少 50%）
- Perplexity < 20（在驗證集上）
- Pre-trained checkpoint 可被 S5/S6/S7 成功載入

### 核心實作要點

#### 1. MambaDataset

從歷史 K 線資料構建訓練集。

```
流程:
1. 載入歷史 bars（從 ParquetDataCatalog 或 CSV）
2. 用 MarketEventTokenizer 將 bars 轉成 token 序列
3. 切成固定長度的 window（seq_len=512）
4. 返回 (input_tokens, target_tokens) pairs
   input:  tokens[0:seq_len]
   target: tokens[1:seq_len+1]
```

支援多資產：不同資產的 token 序列用 SEP token 連接。

#### 2. PretrainTrainer

自監督訓練迴圈。

```
for epoch in epochs:
    for batch in dataloader:
        input_ids, target_ids = batch
        logits, loss = model(input_ids, targets=target_ids)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    val_loss = evaluate(model, val_dataloader)
    save_checkpoint(model, epoch, val_loss)
```

#### 3. 評估指標

- Perplexity = exp(cross_entropy_loss)
- Token prediction accuracy（top-1 和 top-5）
- Event type prediction accuracy（趨勢/波動/成交量/突破 的分類準確度）

### Pseudo Code

```python
class MambaDataset(torch.utils.data.Dataset):
    def __init__(self, token_sequences: list[list[int]], seq_len: int):
        self.sequences = token_sequences
        self.seq_len = seq_len
        self.examples = self._create_examples()

    def _create_examples(self):
        examples = []
        for seq in self.sequences:
            for i in range(0, len(seq) - self.seq_len - 1, self.seq_len // 2):
                chunk = seq[i:i + self.seq_len + 1]
                if len(chunk) == self.seq_len + 1:
                    examples.append(chunk)
        return examples

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        chunk = self.examples[idx]
        input_ids = torch.tensor(chunk[:-1], dtype=torch.long)
        target_ids = torch.tensor(chunk[1:], dtype=torch.long)
        return input_ids, target_ids


class PretrainTrainer:
    def __init__(self, config: MambaConfig, device: str = "cuda"):
        self.config = config
        self.device = device
        self.model = MambaEncoder(config).to(device)
        self.optimizer = self.model.setup_optimizer(
            embedding_lr=1e-3,
            matrix_lr=1e-2,
            unembedding_lr=1e-3,
        )

    def train(self, train_dataset, val_dataset, num_epochs, batch_size):
        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True
        )

        for epoch in range(num_epochs):
            self.model.train()
            total_loss = 0
            for input_ids, target_ids in train_loader:
                input_ids = input_ids.to(self.device)
                target_ids = target_ids.to(self.device)

                _, loss = self.model(input_ids, targets=target_ids)
                loss.backward()

                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                self.optimizer.step()
                self.optimizer.zero_grad()

                total_loss += loss.item()

            avg_loss = total_loss / len(train_loader)
            perplexity = math.exp(min(avg_loss, 20))
            print(f"Epoch {epoch}: loss={avg_loss:.4f}, ppl={perplexity:.2f}")

            val_ppl = self.evaluate(val_dataset, batch_size)
            save_checkpoint(self.model, epoch, avg_loss, val_ppl)

    def evaluate(self, dataset, batch_size):
        self.model.eval()
        loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size)
        total_loss = 0
        with torch.no_grad():
            for input_ids, target_ids in loader:
                input_ids = input_ids.to(self.device)
                target_ids = target_ids.to(self.device)
                _, loss = self.model(input_ids, targets=target_ids)
                total_loss += loss.item()
        avg_loss = total_loss / len(loader)
        return math.exp(min(avg_loss, 20))
```

### 驗證策略

**Example: test_pretrain.py**
- 用合成資料（正弦波 + 雜訊生成 bars）建立小型 dataset
- 跑 10 個 epoch → loss 應下降
- 載入 checkpoint → forward 一次 → 確認輸出形狀正確

**測試計畫**：
- 單元測試：MambaDataset 的 input/target 對齊
- 單元測試：PretrainTrainer 的 loss 計算
- 整合測試：小型資料上的完整訓練迴圈（CPU，2 epoch）

**完成檢查**：
- [ ] MambaDataset 正確產生 (input, target) pairs
- [ ] PretrainTrainer loss 下降
- [ ] Checkpoint 可載入且 forward 正確
- [ ] 驗證集 perplexity 可計算

---

## S4: RL Gym Infrastructure — NT BacktestEngine as Multi-Task Env

### Context

**目標**：建立統一的 RL Gym 環境，封裝 NT BacktestEngine。S5/S6/S7 繼承此基類，只覆寫 reward/observation/action 定義。

**依賴**：
- 外部：`gymnasium`
- NT：`BacktestEngine`、`BacktestEngineConfig`、`Venue`、`CurrencyPair`、`Bar`、`Money`
- S1: MambaConfig（僅用於定義 seq_len）
- S2: MarketEventTokenizer（用於構建 observation）

**語義約束**：
- 與 S5/S6/S7 共享：step() 介面固定為 `(obs, reward, terminated, truncated, info)`
- 與 S1 共享：obs 是 token sequence，shape `(seq_len,)` int tensor
- NT streaming mode 的操作順序固定：`add_data → run(streaming=True) → clear_data`

**基礎設施盤點**：
- NT BacktestEngine streaming mode — 已 POC 驗證（lab/poc_streaming_equity.py, lab/poc_strategy_order.py）
- NT BacktestEngine streaming step latency — 已 benchmark（P50=0.03ms, lab/poc_perf_benchmark.py）
- NT portfolio.equity() — 回傳 `dict[Currency, Money]`，用 `.as_double()` 取 float
- NT ExecAlgorithm — 有完整的 on_order + spawn 機制（nautilus_trader/execution/algorithm.pyx）

**依賴錨點**：
- `NTGymBase` → 定義 `rl/gym/base.py:15` / 消費 `rl/gym/single_asset.py:10`, `rl/gym/allocation.py:10`, `rl/gym/execution.py:10`
- `BacktestEngine.add_data` → 定義 `nautilus_trader/backtest/engine.pyx` / 消費 `rl/gym/base.py:80`
- `portfolio.equity` → 定義 `nautilus_trader/portfolio/portfolio.pyx` / 消費 `rl/gym/base.py:120`

**技術選型**：
- 繼承 `gymnasium.Env` — 標準 RL 介面，相容所有 RL 演算法
- 不用 stable-baselines3 或 ray RLlib — 保持輕量，REINFORCE 自建

**成功標準**：
- NTGymBase 可建立、reset、step
- step() 耗時 < 1ms（已驗證）
- 子類別只需覆寫 `_compute_reward()` 和 `_build_observation()`

### 核心實作要點

#### 1. NTGymBase(gymnasium.Env)

抽象基類。封裝 BacktestEngine 生命週期。

```
核心狀態:
  engine: BacktestEngine
  bars: list[Bar]           — 本 episode 的所有 bars
  current_step: int         — 當前 bar 索引
  tokenizer: MarketEventTokenizer
  token_history: list[int]  — 累積的 token 序列（供 Mamba 用）

gymnasium 介面:
  observation_space: gymnasium.spaces.Box(seq_len,) — token ids
  action_space: 子類別定義

  reset(seed) → obs, info:
    建立 new BacktestEngine + venue + instruments
    reset tokenizer
    return BOS token + padding

  step(action) → obs, reward, terminated, truncated, info:
    1. 執行 action（子類別實作：下單/調倉/拆單）
    2. add_data(current_bar) → run(streaming=True) → clear_data()
    3. tokenize_bar(current_bar) → 加入 token_history
    4. _build_observation() → 取最近 seq_len 個 tokens
    5. _compute_reward() → 子類別實作
    6. 檢查 terminated（episode bars 用完）

抽象方法（子類別必須覆寫）:
  _setup_engine() → BacktestEngine  — 建立引擎、venue、instruments
  _execute_action(action)           — 執行 RL agent 的決策
  _compute_reward() → float         — 計算這一步的 reward
```

#### 2. Episode 管理

```
每個 episode:
  1. reset() 建立新 engine
  2. 隨機選一段歷史期間（如隨機一年的 daily bars）
  3. 逐步 step() 直到 bars 用完
  4. 最終 reward 可以包含 episode-level 指標（Sharpe、max drawdown）
```

### Pseudo Code

```python
class NTGymBase(gymnasium.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, config: GymConfig, tokenizer: MarketEventTokenizer):
        super().__init__()
        self.config = config
        self.tokenizer = tokenizer
        self.seq_len = config.seq_len

        self.observation_space = gymnasium.spaces.Box(
            low=0, high=tokenizer.vocab.size,
            shape=(self.seq_len,), dtype=np.int32
        )
        self.token_history = []
        self.bars = []
        self.current_step = 0
        self.engine = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.tokenizer.reset()
        self.token_history = [self.tokenizer.vocab.BOS]
        self.current_step = 0

        self.bars = self._sample_episode_bars()
        self.engine = self._setup_engine()

        obs = self._build_observation()
        info = {"episode_length": len(self.bars)}
        return obs, info

    def step(self, action):
        self._execute_action(action)

        bar = self.bars[self.current_step]
        self.engine.add_data([bar], validate=False)
        self.engine.run(streaming=True)
        self.engine.clear_data()

        token = self.tokenizer.tokenize_bar(bar)
        self.token_history.append(token)
        self.current_step += 1

        obs = self._build_observation()
        reward = self._compute_reward()
        terminated = self.current_step >= len(self.bars)
        truncated = False
        info = {"step": self.current_step, "reward": reward}

        return obs, reward, terminated, truncated, info

    def _build_observation(self):
        tokens = self.token_history[-self.seq_len:]
        padded = [self.tokenizer.vocab.PAD] * (self.seq_len - len(tokens)) + tokens
        return np.array(padded, dtype=np.int32)

    def _sample_episode_bars(self) -> list[Bar]:
        raise NotImplementedError

    def _setup_engine(self) -> BacktestEngine:
        raise NotImplementedError

    def _execute_action(self, action):
        raise NotImplementedError

    def _compute_reward(self) -> float:
        raise NotImplementedError

    def close(self):
        if self.engine is not None:
            self.engine.end()
```

### 驗證策略

**Example: test_gym_base.py**
- 建立測試子類別（實作所有抽象方法為 no-op）
- reset() → obs 形狀正確
- step(0) → obs/reward/terminated 格式正確
- 跑完整 episode → terminated=True
- 量測 step() latency < 1ms

**測試計畫**：
- 單元測試：_build_observation padding 正確
- 單元測試：episode termination 條件
- 整合測試：搭配真實 BacktestEngine 的完整 episode（使用 lab/poc 程式碼的 pattern）

**完成檢查**：
- [ ] NTGymBase 的 reset/step/close 符合 gymnasium 規範
- [ ] 子類別只需覆寫 4 個抽象方法
- [ ] observation 是合法的 token id sequence
- [ ] Episode 可正常結束

---

## S5: Task C — Single-Asset Mamba Trading Policy

### Context

**目標**：RL fine-tune pre-trained Mamba 做單一資產交易。這是最基礎的任務，驗證 pre-train → RL fine-tune 路線可行。

**UC 引用**：Task C — Mamba-based RL trading agent

**依賴**：
- S1: MambaEncoder（task_head_type="policy"）
- S2: MarketEventTokenizer
- S3: Pre-trained checkpoint
- S4: NTGymBase → NTSingleAssetGym

**語義約束**：
- 與 S6 共享：MambaEncoder 的 forward 介面
- Action space 是連續的 `Box(-1, 1)` → -1 = full short, 0 = flat, 1 = full long
- Reward 是每步的 PnL change

**基礎設施盤點**：
- NT BacktestEngine streaming — 已驗證
- NT Strategy.on_bar + submit_order — 已驗證（lab/poc_strategy_order.py）
- NT portfolio.equity() — 已驗證
- 已有 EP：nt-gym-deepscalper.md（Path E，SAC + MLP），本段是進化版

**依賴錨點**：
- `NTSingleAssetGym` → 定義 `rl/gym/single_asset.py:10` / 消費 `rl/scripts/rl_train.py:30`
- `MambaEncoder` → 定義 `rl/mamba/model.py:15` / 消費 `rl/scripts/rl_train.py:25`

**成功標準**：
- Mamba policy 在 BTC-USD daily bars 上 Sharpe > 1.0
- 對比基線：有 pre-train 的收斂速度 > 無 pre-train 的至少 2x

### 核心實作要點

#### 1. NTSingleAssetGym(NTGymBase)

```
_setup_engine():
  建立 BacktestEngine + SIM venue + BTC-USD instrument
  加入一個 NoOpStrategy（不做任何事，Gym 控制）

action_space: gymnasium.spaces.Box(-1, 1, shape=(1,))
  -1 = 目標持有 -max_position（做空）
   0 = 目標平倉
   1 = 目標持有 +max_position（做多）

_execute_action(action):
  計算目標部位 = action * max_position
  當前部位 = portfolio.net_position(instrument_id)
  delta = 目標部位 - 當前部位
  if delta > 0: submit_order(BUY, delta)
  if delta < 0: submit_order(SELL, abs(delta))

_compute_reward():
  current_equity = portfolio.equity(venue).as_double()
  reward = current_equity - self._prev_equity
  self._prev_equity = current_equity
  return reward
```

#### 2. RLTrainer（沿用在 S1 定義的，此處為 Task C 特化）

```
訓練迴圈（nanochat pattern 改寫）:
1. 載入 pre-trained MambaEncoder（凍結前 N-2 層）
2. 替換 task_head_type="policy"
3. 每個 episode:
   a. obs = env.reset()
   b. 逐步收集 (obs, action, reward) 軌跡
   c. 計算 advantage = reward - mean(rewards)
   d. loss = -(logp * advantage).mean()
   e. backward + update
4. 定期評估 + 儲存 checkpoint
```

#### 3. MambaStrategy(Strategy)

將訓練好的 Mamba policy 接入 NT live/backtest 的 Strategy 介面。

```
on_bar(bar):
  token = tokenizer.tokenize_bar(bar)
  obs = build_observation(token_history)
  action = mamba_policy.forward(obs)
  execute_action(action)  # 同 _execute_action 邏輯
```

### Pseudo Code

```python
class NTSingleAssetGym(NTGymBase):
    def __init__(self, config: GymConfig, tokenizer: MarketEventTokenizer):
        super().__init__(config, tokenizer)
        self.action_space = gymnasium.spaces.Box(
            low=-1.0, high=1.0, shape=(1,), dtype=np.float32
        )
        self.instrument = make_btc_instrument()
        self.max_position = 1.0
        self._prev_equity = 1_000_000.0

    def _setup_engine(self) -> BacktestEngine:
        engine = BacktestEngine(config=BacktestEngineConfig(
            trader_id=TraderId("MAMBA-001")
        ))
        engine.add_venue(
            venue=Venue("SIM"),
            oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN,
            starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
            fee_model=MakerTakerFeeModel(),
        )
        engine.add_instrument(self.instrument)
        return engine

    def _execute_action(self, action):
        target_qty = float(action[0]) * self.max_position
        current_qty = float(self.engine.cache.net_position(
            self.instrument.id
        ))
        delta = target_qty - current_qty

        if abs(delta) < self.instrument.size_increment:
            return

        side = OrderSide.BUY if delta > 0 else OrderSide.SELL
        qty = Quantity(abs(delta), precision=self.instrument.size_precision)
        order = self.engine.trader.generate_order(
            instrument_id=self.instrument.id,
            order_side=side,
            quantity=qty,
        )
        self.engine.trader.submit_order(order)

    def _compute_reward(self) -> float:
        equity_dict = self.engine.portfolio.equity(venue=Venue("SIM"))
        current_equity = float(equity_dict[Currency.from_str("USD")].as_double())
        reward = current_equity - self._prev_equity
        self._prev_equity = current_equity
        return reward
```

> **EP Validate 修正 V3（S5）**：pseudo code 有兩個 API 錯誤需在 /build 時修正：
> 1. `self.engine.cache.net_position(instrument_id)` → 應為 `self.engine.portfolio.net_position(instrument_id)`（定義 `portfolio/portfolio.pyx:1705`，回傳 `Decimal`）。Cache 只有 `positions_open()` 回傳 `list[Position]`，無 `net_position()`。
> 2. `self.engine.trader.generate_order()` + `self.engine.trader.submit_order()` → `Trader` 只有 report 方法（`generate_orders_report`），無訂單創建 API。正確模式：採用 deepscalper EP 的 **RLStrategyBridge(Strategy)** 架構，透過 Strategy 的 `order_factory.market()` + `self.submit_order()` 提交訂單。Gym 的 `_execute_action()` 應呼叫 `strategy.set_action(action)`，由 strategy 在 `on_bar()` 中執行訂單。

### 驗證策略

**Example: test_single_asset_gym.py**
- 建立環境，用 BTC daily bars
- 用 random policy 跑 1 episode → 確認不 crash
- 用 constant action=1.0（永遠做多）跑 1 episode → 確認有 PnL

**Example: test_mamba_policy_train.py**
- 載入 S3 的 pre-trained checkpoint（或隨機初始化）
- 跑 10 個 episode 的 REINFORCE 訓練
- 確認 loss 在更新（不管是否收斂）

**測試計畫**：
- 單元測試：NTSingleAssetGym 的 action 執行和 reward 計算
- 整合測試：完整 episode 的 obs/reward/terminated 格式
- 效能測試：step() latency < 1ms（繼承 NTGymBase 的效能）

**完成檢查**：
- [ ] NTSingleAssetGym 可跑完整 episode
- [ ] Mamba policy 可訓練（loss 更新）
- [ ] Pre-trained → fine-tune 比 from-scratch 收斂快
- [ ] 最終 Sharpe > 1.0（BTC daily，驗證集）

---

## S6: Task A — Multi-Asset Portfolio Allocation

### Context

**目標**：RL fine-tune pre-trained Mamba 做多資產配置。Mamba 的隱藏狀態自動捕捉跨資產相關性。

**UC 引用**：Task A — Mamba-based portfolio allocator

**依賴**：
- S1: MambaEncoder（task_head_type="allocation"）
- S2: MarketEventTokenizer（多資產：SEP token 分隔不同資產的 event sequence）
- S3: Pre-trained checkpoint
- S4: NTGymBase → NTAllocationGym

**語義約束**：
- 與 S5 共享：MambaEncoder 架構、訓練迴圈
- 與 S5 不同：action space 是 N 維 softmax（非 1 維 tanh）
- 與 S5 不同：observation 包含多資產的 token 序列（用 SEP token 連接）

**基礎設施盤點**：
- NT Portfolio API — 有多工具追蹤（_net_positions, equity, unrealized_pnls）
- NT Strategy — 可訂冊多工具訂閱
- NT **沒有**內建 allocation/rebalancing — 這正是 Mamba 要填補的缺口

> **EP Validate 驗證（POC 3）**：3 個 CurrencyPair（BTCUSDT, ETHUSDT, ADAUSDT）共用同一個 MARGIN 帳戶。單一 Strategy 訂閱 3 個 BarType → on_bar 依 instrument_id 區分 → 對 3 個 instrument 各提交 market order → 全部成交 → `portfolio.equity(venue)` 回傳 `dict[Currency, Money]` 自動聚合。3 個部位全部開倉成功。POC 檔案：`lab/poc_multi_asset_streaming.py` ✅

**成功標準**：
- Mamba allocation 的 Sharpe > equal-weight baseline
- Mamba allocation 的 max drawdown < single-asset max drawdown

### 核心實作要點

#### 1. NTAllocationGym(NTGymBase)

```
_setup_engine():
  建立 BacktestEngine + SIM venue + 多個 CurrencyPair（BTC, ETH, SOL）
  N_ASSETS = 3

action_space: gymnasium.spaces.Box(0, 1, shape=(N_ASSETS + 1,))
  [btc_weight, eth_weight, sol_weight, cash_weight]
  softmax 後 sum to 1.0

_execute_action(action):
  weights = softmax(action)
  for each asset:
    target_value = total_equity * weights[asset_idx]
    current_value = position_qty * current_price
    delta_value = target_value - current_value
    delta_qty = delta_value / current_price
    submit_order(BUY/SELL, abs(delta_qty))

_compute_reward():
  current_equity = portfolio.equity(venue).as_double()
  step_return = (current_equity - prev_equity) / prev_equity
  reward = step_return  # 或 risk-adjusted version
```

#### 2. 多資產 Observation

每一步構建的 observation：
```
[BTC_events..., SEP, ETH_events..., SEP, SOL_events..., SEP, portfolio_state]
```

用 SEP token 分隔不同資產的 event history。Mamba 自然學會跨資產的相關性。

#### 3. Reward 設計選項

| Reward | 公式 | 優缺點 |
|--------|------|--------|
| Step return | `(eq_t - eq_{t-1}) / eq_{t-1}` | 簡單，但忽略風險 |
| Sharpe-like | `mean(returns) / std(returns)` | 需要累積，window 設計影響大 |
| Drawdown-penalized | `return - λ × max(0, peak - equity)` | 鼓勵控制回撤 |
| Sortino-like | `mean(returns) / downside_dev` | 只懲罰下行風險 |

預設用 step return + drawdown penalty。

### Pseudo Code

```python
class NTAllocationGym(NTGymBase):
    def __init__(self, config: GymConfig, tokenizer: MarketEventTokenizer):
        super().__init__(config, tokenizer)
        self.n_assets = 3
        self.action_space = gymnasium.spaces.Box(
            low=-5.0, high=5.0,  # logits, apply softmax internally
            shape=(self.n_assets + 1,),  # +1 for cash
            dtype=np.float32
        )
        self.instruments = [make_btc_instrument(), make_eth_instrument(), make_sol_instrument()]
        self._peak_equity = 1_000_000.0

    def _setup_engine(self) -> BacktestEngine:
        engine = BacktestEngine(config=BacktestEngineConfig(
            trader_id=TraderId("ALLOC-001")
        ))
        engine.add_venue(
            venue=Venue("SIM"),
            oms_type=OmsType.NETTING,
            account_type=AccountType.MARGIN,
            starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
            fee_model=MakerTakerFeeModel(),
        )
        for inst in self.instruments:
            engine.add_instrument(inst)
        return engine

    def _execute_action(self, action):
        weights = torch.softmax(torch.tensor(action), dim=0).numpy()

        equity_dict = self.engine.portfolio.equity(venue=Venue("SIM"))
        total_equity = float(equity_dict[Currency.from_str("USD")].as_double())

        for i, inst in enumerate(self.instruments):
            target_value = total_equity * weights[i]
            current_qty = float(self.engine.cache.net_position(inst.id))
            current_price = self._get_current_price(inst)
            current_value = current_qty * current_price
            delta_value = target_value - current_value
            delta_qty = delta_value / current_price if current_price > 0 else 0.0

            if abs(delta_qty) < float(inst.size_increment):
                continue

            side = OrderSide.BUY if delta_qty > 0 else OrderSide.SELL
            qty = Quantity(abs(delta_qty), precision=inst.size_precision)
            order = self.engine.trader.generate_order(
                instrument_id=inst.id, order_side=side, quantity=qty,
            )
            self.engine.trader.submit_order(order)

    def _build_observation(self):
        multi_asset_tokens = []
        for inst in self.instruments:
            asset_tokens = self._get_asset_token_history(inst.id)
            multi_asset_tokens.extend(asset_tokens)
            multi_asset_tokens.append(self.tokenizer.vocab.SEP)

        tokens = multi_asset_tokens[-self.seq_len:]
        padded = [self.tokenizer.vocab.PAD] * (self.seq_len - len(tokens)) + tokens
        return np.array(padded, dtype=np.int32)

    def _compute_reward(self) -> float:
        equity_dict = self.engine.portfolio.equity(venue=Venue("SIM"))
        current_equity = float(equity_dict[Currency.from_str("USD")].as_double())

        step_return = (current_equity - self._prev_equity) / self._prev_equity
        drawdown = max(0, (self._peak_equity - current_equity) / self._peak_equity)
        self._peak_equity = max(self._peak_equity, current_equity)
        self._prev_equity = current_equity

        return step_return - 0.5 * drawdown
```

> **EP Validate 修正 V4（S6）**：pseudo code 有兩個 API 錯誤需在 /build 時修正：
> 1. `self.engine.cache.net_position(inst.id)` → 應為 `self.engine.portfolio.net_position(inst.id)`（同 S5 V3 修正）
> 2. `self.engine.trader.generate_order()` + `self.engine.trader.submit_order()` → 採用 RLStrategyBridge(Strategy) 模式（見 S5 V3 修正）

### 驗證策略

**Example: test_allocation_gym.py**
- 3 資產環境，equal-weight action
- 跑 1 episode → 確認多資產 order 提交成功
- 確認 observation 包含 SEP tokens

**測試計畫**：
- 單元測試：softmax action → 權重 sum to 1.0
- 單元測試：rebalance order 計算正確
- 整合測試：多資產完整 episode
- 對比測試：Mamba allocation vs equal-weight vs single-asset

**完成檢查**：
- [ ] NTAllocationGym 支援多資產
- [ ] Action 經 softmax 後 sum to 1.0
- [ ] Rebalance order 正確提交
- [ ] Sharpe > equal-weight baseline

---

## S7: Task B — Smart Order Execution (MambaExecAlgorithm)

### Context

**目標**：RL fine-tune pre-trained Mamba 做智慧拆單。取代 NT 現有的固定 TWAP，學習市場微結構動態調整拆單策略。

**UC 引用**：Task B — Mamba-based smart execution algorithm

**依賴**：
- S1: MambaEncoder（task_head_type="execution"）
- S2: MarketEventTokenizer
- S3: Pre-trained checkpoint
- S4: NTGymBase → NTExecutionGym

**語義約束**：
- 與 NT ExecAlgorithm 介面對齊：`on_order(primary)` → `spawn_market(limit, qty)`
- Action 是連續的：(qty_fraction, urgency) — 拆多少 + 多急迫
- Reward 是 Implementation Shortfall：benchmark price（arrival price 或 VWAP）vs 實際成交均價

**基礎設施盤點**：
- NT ExecAlgorithm 基類 — 有完整的 on_order + spawn 機制（nautilus_trader/execution/algorithm.pyx）
- NT TWAP 範例 — nautilus_trader/examples/algorithms/twap.py
- NT spawn_market/spawn_limit — 生成子單、自動減少母單數量
- NT BacktestEngine 支援 orderbook 模擬（但本段 MVP 用 bar-level 模擬）

> **EP Validate 驗證（POC 2）**：ExecAlgorithm 完整路由流程驗證。Strategy 提交帶 `exec_algorithm_id` 的母單 → RiskEngine 路由到 MessageBus endpoint → ExecAlgorithm.on_order() 收到母單 → spawn_market() 生成子單（自動繼承 instrument_id, side, strategy_id）→ submit_order() 送出子單 → 子單在 BacktestEngine 成交 → on_order_filled 回調觸發。POC 檔案：`lab/poc_exec_algo_spawn.py` ✅

**依賴錨點**：
- `NTExecutionGym` → 定義 `rl/gym/execution.py:10` / 消費 `rl/scripts/rl_train.py:30`
- `MambaExecAlgorithm` → 定義 `rl/strategies/mamba_exec_algo.py:15` / 繼承 `nautilus_trader/execution/algorithm.pyx:ExecAlgorithm`
- `ExecAlgorithm.spawn_market` → 定義 `nautilus_trader/execution/algorithm.pyx:230` / 消費 `rl/strategies/mamba_exec_algo.py:80`

**成功標準**：
- Mamba exec 的 Implementation Shortfall < fixed TWAP
- 在流動性差的時段自動減小拆單量、在流動性好的時段加大

### 核心實作要點

#### 1. NTExecutionGym(NTGymBase)

與 S5/S6 不同的 Gym 設計。這不是「交易策略」的 Gym，而是「執行演算法」的 Gym。

```
情境:
  - 給定一個大額母單（如買入 10 BTC）
  - 環境是接下來 N 根 bars 的市場狀態
  - Agent 每步決定：拆多少、怎麼下

action_space: gymnasium.spaces.Box(0, 1, shape=(2,))
  action[0] = qty_fraction (0~1)：這一步執行剩餘量的多少比例
  action[1] = urgency (0~1)：0=用 limit order，1=用 market order

_execute_action(action):
  qty_to_execute = remaining_qty * action[0]
  if action[1] > 0.7:
    submit market order（立即成交，可能有滑價）
  else:
    submit limit order（可能不成交）
  remaining_qty -= executed_qty

_compute_reward():
  benchmark = arrival_price（母單到達時的市場價）
  actual = weighted_avg_execution_price
  shortfall = (actual - benchmark) * total_qty
  reward = -shortfall（越小越好）
```

#### 2. MambaExecAlgorithm(ExecAlgorithm)

將訓練好的 Mamba 接入 NT 的 ExecAlgorithm 介面。

```
on_order(primary_order):
  remaining = primary_order.quantity
  tokenizer.reset()

  while remaining > 0 and not timed_out:
    bar = wait_for_next_bar()
    token = tokenizer.tokenize_bar(bar)

    obs = build_observation(token_history)
    action = mamba_policy.forward(obs)

    qty_to_exec = remaining * action[0]
    if action[1] > 0.7:
      child = self.spawn_market(primary_order, Quantity(qty_to_exec))
    else:
      price = compute_limit_price(action[1])
      child = self.spawn_limit(primary_order, Quantity(qty_to_exec), price)

    self.submit_order(child)
    remaining -= qty_to_exec
```

### Pseudo Code

```python
class NTExecutionGym(NTGymBase):
    def __init__(self, config: GymConfig, tokenizer: MarketEventTokenizer):
        super().__init__(config, tokenizer)
        self.action_space = gymnasium.spaces.Box(
            low=0.0, high=1.0, shape=(2,), dtype=np.float32
        )
        self.instrument = make_btc_instrument()
        self.total_qty = 10.0
        self.remaining_qty = self.total_qty
        self.executions = []
        self.arrival_price = None

    def reset(self, seed=None, options=None):
        obs, info = super().reset(seed=seed, options=options)
        self.remaining_qty = self.total_qty
        self.executions = []
        self.arrival_price = float(self.bars[0].close)
        return obs, info

    def _execute_action(self, action):
        qty_fraction = float(action[0])
        urgency = float(action[1])

        qty_to_exec = self.remaining_qty * qty_fraction
        if qty_to_exec < float(self.instrument.size_increment):
            return

        qty = Quantity(qty_to_exec, precision=self.instrument.size_precision)
        side = OrderSide.BUY

        if urgency > 0.7:
            order = self.engine.trader.generate_order(
                instrument_id=self.instrument.id,
                order_side=side, quantity=qty,
            )
        else:
            current_price = float(self.bars[self.current_step].close)
            offset = (1.0 - urgency) * 50.0
            price = Price(current_price + offset, precision=self.instrument.price_precision)
            order = self.engine.trader.generate_order(
                instrument_id=self.instrument.id,
                order_side=side, quantity=qty, price=price,
            )

        self.engine.trader.submit_order(order)
        self.remaining_qty -= qty_to_exec

    def _compute_reward(self) -> float:
        if not self.executions:
            return 0.0

        actual_avg = sum(p * q for p, q in self.executions) / sum(q for _, q in self.executions)
        shortfall = (actual_avg - self.arrival_price) * self.total_qty
        return -shortfall


class MambaExecAlgorithm(ExecAlgorithm):
    def __init__(self, model_path: str, tokenizer: MarketEventTokenizer):
        super().__init__(config=ExecAlgorithmConfig(
            exec_algorithm_id=ExecAlgorithmId("MAMBA_EXEC")
        ))
        self.model = load_mamba_policy(model_path, task="execution")
        self.tokenizer = tokenizer
        self.token_history = []

    def on_start(self):
        self.tokenizer.reset()
        self.token_history = [self.tokenizer.vocab.BOS]

    def on_order(self, order: Order):
        remaining = float(order.quantity)
        instrument = self.cache.instrument(order.instrument_id)

        while remaining > float(instrument.size_increment):
            obs = self._build_obs()
            action = self.model.forward(obs)

            qty_fraction = float(action[0])
            urgency = float(action[1])

            qty = remaining * qty_fraction
            qty = min(qty, remaining)
            exec_qty = Quantity(qty, precision=instrument.size_precision)

            if urgency > 0.7:
                child = self.spawn_market(order, exec_qty)
            else:
                price = self._compute_limit_price(instrument, urgency)
                child = self.spawn_limit(order, exec_qty, price)

            self.submit_order(child)
            remaining -= qty

    def on_bar(self, bar: Bar):
        token = self.tokenizer.tokenize_bar(bar)
        self.token_history.append(token)

    def _build_obs(self):
        tokens = self.token_history[-self.model.config.seq_len:]
        padded = [self.tokenizer.vocab.PAD] * (self.model.config.seq_len - len(tokens)) + tokens
        return torch.tensor([padded], dtype=torch.long)
```

> **EP Validate 修正 V5（S7）**：`MambaExecAlgorithm.on_order()` 的同步 `while remaining > 0` 迴圈會阻塞 NT 事件迴圈。`on_order()` 是 `cpdef void` 回調，**必須立即返回**，不能在其中等待下一根 bar。正確模式（參考 `examples/algorithms/twap.py`）：`on_order()` 只儲存母單和 remaining_qty 到 self 屬性 → `on_bar()` 被呼叫時讀取狀態、執行一次拆單、spawn 子單 → 持續直到 remaining_qty < size_increment。這是標準 NT ExecAlgorithm 的事件驅動模式。

### 驗證策略

**Example: test_execution_gym.py**
- 建立環境，給定 10 BTC 母單
- 用 constant action (0.1, 0.8) 跑 → 類似 TWAP
- 確認 IS 可計算

**Example: test_mamba_exec_algo.py**
- 載入訓練好的模型
- 模擬 NT 的 ExecAlgorithm.on_order 呼叫
- 確認 spawn 出正確的子單

**測試計畫**：
- 單元測試：execution action → qty/urgency 正確
- 單元測試：IS 計算正確
- 整合測試：完整 execution episode
- 對比測試：Mamba exec vs fixed TWAP vs fixed VWAP

**完成檢查**：
- [ ] NTExecutionGym 可跑完整 execution episode
- [ ] IS reward 正確計算
- [ ] MambaExecAlgorithm 正確接入 NT ExecAlgorithm
- [ ] IS < fixed TWAP IS

---

## 整合策略

### 段落間介面合約

| 介面 | 定義段 | 消費段 | 格式 |
|------|--------|--------|------|
| Event Token | S2 | S3, S5, S6, S7 | `int ∈ [0, vocab_size)` |
| Pre-trained checkpoint | S3 | S5, S6, S7 | `model.state_dict()` |
| Gym (obs, action, reward) | S4 | S5, S6, S7 | gymnasium standard |
| MambaEncoder forward | S1 | S5, S6, S7 | `(B, T) → (B, T, d_model)` |

### 訓練流程串接

```bash
S1+S2: pip install mamba-ssm, 建立模型和 tokenizer
S3: python rl/scripts/pretrain.py --data btc_daily.parquet --epochs 50
S5: python rl/scripts/rl_train.py --task trading --pretrained checkpoints/pretrain.pt
S6: python rl/scripts/rl_train.py --task allocation --pretrained checkpoints/pretrain.pt
S7: python rl/scripts/rl_train.py --task execution --pretrained checkpoints/pretrain.pt
```

### 效能預期

| 階段 | 預期時間 | 硬體 |
|------|---------|------|
| S1 開發 + 測試 | 快 | CPU |
| S2 開發 + 測試 | 快 | CPU |
| S3 Pre-train (5yr BTC daily) | 中 | GPU |
| S5 RL fine-tune (100 episodes) | 中 | GPU + NT streaming |
| S6 RL fine-tune (100 episodes) | 中 | GPU + NT streaming |
| S7 RL fine-tune (100 episodes) | 中 | GPU + NT streaming |

---

## 收尾步驟

### 1. USE-CASES.md 更新

本 EP 在 `nautilus_trader/rl/` 目錄下新增 USE-CASES.md：

```markdown
### 📋 D-RL1: Market Event Tokenizer — rl/mamba/tokenizer.py
- **能力**: 將 OHLCV Bar 序列轉換為 Event Token 序列
- **入口**: `MarketEventTokenizer.tokenize_sequence(bars)`

### 📋 D-RL2: Mamba Foundation Pre-train — rl/scripts/pretrain.py
- **能力**: 自監督訓練 Mamba 學習市場動態
- **入口**: CLI `python rl/scripts/pretrain.py`

### 📋 D-RL3: Task C Mamba Trading Policy — rl/gym/single_asset.py
- **能力**: Mamba policy 做單一資產 RL 交易
- **入口**: CLI `python rl/scripts/rl_train.py --task trading`

### 📋 D-RL4: Task A Mamba Asset Allocation — rl/gym/allocation.py
- **能力**: Mamba 做多資產配置
- **入口**: CLI `python rl/scripts/rl_train.py --task allocation`

### 📋 D-RL5: Task B Mamba Smart Execution — rl/gym/execution.py
- **能力**: Mamba 做智慧拆單（替代固定 TWAP）
- **入口**: CLI `python rl/scripts/rl_train.py --task execution`
```

### 2. CLAUDE.md 更新

在 `nautilus_trader/rl/` 目錄下建立 CLAUDE.md，描述：
- 模組架構（Mamba + Gym + Strategies + Data）
- 訓練流程（pre-train → RL fine-tune）
- 與 NT 的整合點（BacktestEngine、Strategy、ExecAlgorithm、Portfolio）

### 3. /audit-test

對所有新增測試執行品質稽核。
