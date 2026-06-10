# Mamba Foundation Model for Financial RL — 學習計畫

> **起點**: 已熟悉 BERT/CNN（deep learning），有 Transformer 基礎概念
> **終點**: 能獨立實作 EP `mamba-foundation-rl.md` 的 S1-S7，理解 Pre-train → RL fine-tune 全流程
> **與 DeepScalper EP 的關係**: 兩條路線互補 — DeepScalper 是傳統 RL（環境+Agent），Mamba 是 Foundation Model 路線（先學市場再學策略）

---

## 兩條路線的對比

先理解這條路線跟 DeepScalper EP 的本質差異：

| 維度 | DeepScalper EP (nt-gym-deepscalper) | Mamba Foundation EP (本計畫) |
|------|-------------------------------------|----------------------------|
| **範式** | 傳統 RL：環境 + Agent 端對端訓練 | Foundation Model：先 pre-train 再 task-specific fine-tune |
| **模型** | SAC（3 個 loss function） | Mamba SSM（自回歸 + REINFORCE） |
| **輸入** | 手工特徵（82 維 float 向量） | Event Token（離散化市場事件序列） |
| **輸出** | 1 維連續 action（持倉比例） | 視任務切換 task head（交易/配置/拆單） |
| **記憶** | 無（每步獨立） | Mamba 隱藏狀態自帶長序列記憶 |
| **多任務** | 單一任務 | 3 個任務共享 encoder |
| **複雜度** | RL 概念為主 | DL + RL + NLP 概念混合 |

**選擇建議**：
- 如果 RL 基礎不夠 → 先做 DeepScalper EP 的學習計畫
- 如果 DL/Transformer 基礎好 → 本計畫可以更快上手（REINFORCE 比 SAC 簡單）
- 兩條路線最終可以在 NT 環境中對比績效

---

## 學習地圖總覽

```
Phase 0            Phase 1            Phase 2             Phase 3            Phase 4
SSM + Mamba        Event Tokenization  Self-supervised     REINFORCE          NT 多任務 Gym
基礎概念            金融市場的 NLP      Pre-train           Policy Gradient     (Task A/B/C)
    │                   │                  │                  │                  │
    └─── 先修 ────→ ────┘                  │                  │                  │
                                             └── 先修 ────→ ──┘                  │
                                                                                 │
                                                                   Phase 5       │
                                                                   EP 實作 S1-S7 ←┘
```

| Phase | 核心問題 | 學什麼 |
|-------|---------|--------|
| 0 | Mamba 是什麼？為什麼不用 Transformer？ | SSM 數學 + Mamba 架構 |
| 1 | 金融資料怎麼 tokenize？ | 離散化 + Event Token 設計 |
| 2 | 怎麼讓模型「理解」市場？ | 自回歸 pre-train + next-event prediction |
| 3 | 怎麼從「理解」到「決策」？ | REINFORCE + reward shaping |
| 4 | 怎麼把三個任務統一成一個框架？ | NT Gym 基類 + Task Head 設計 |
| 5 | 實作 | EP S1-S7 按依賴順序執行 |

---

## Phase 0: SSM + Mamba 基礎

### 為什麼需要這個 Phase

這個 EP 的核心模型是 Mamba（Selective State Space Model），不是 Transformer。如果你不理解 SSM 和 Mamba 的設計動機，後面讀 EP 的 `MambaBlock` 會像讀天書。

### 核心概念：從 Transformer 到 Mamba 的演化

```
RNN (1990s)          Transformer (2017)         Mamba (2023)
  │                       │                         │
  │ O(1) 推論             │ O(n²) attention         │ O(n) 推論
  │ 無法平行化訓練        │ 可平行化                 │ 可平行化訓練
  │ 長序列梯度消失        │ 固定長度上下文           │ 理論無限長度
  │                       │ (即使是 FlashAttention)  │ 選擇性記憶
  │                       │                         │ 硬體感知優化
```

| 概念 | 一句話解釋 | 與 Transformer 的類比 |
|------|-----------|---------------------|
| **SSM** (State Space Model) | 用隱藏狀態 h(t) 壓縮歷史，h'(t) = Ah(t) + Bx(t) | 類似 RNN 的 hidden state |
| **HiPPO 初始化** | 讓 SSM 的矩陣 A 能記住長期歷史的數學技巧 | Transformer 不需要（attention 直接看全部） |
| **Selective SSM** (Mamba 的創新) | 根據輸入動態決定「記住什麼、忘記什麼」 | 類似 attention 的 selectivity，但 O(n) |
| **d_model** | 特徵維度（EP 預設 256） | 同 Transformer 的 d_model |
| **d_state** | SSM 隱藏狀態維度（EP 預設 16） | N/A（Transformer 無此概念） |
| **d_conv** | 局部卷積寬度（EP 預設 4） | 類似局部 attention window |

### 為什麼 Mamba 適合金融

| 特性 | 金融場景的需求 | Mamba 的對應 |
|------|---------------|-------------|
| **長序列** | 多年日 K（>1000 bars） | O(n) 不會 OOM（Transformer O(n²) 會） |
| **選擇性記憶** | 市場有 regime 切換，不需要記住所有細節 | Selective SSM 自動學會 forget gate |
| **即時推論** | 交易決策要快 | O(1) 單步推論（跟 RNN 一樣快） |
| **多資產序列** | 不同資產的 event 用 SEP token 連接 | SSM 天然處理連續序列，不需要 position encoding |

### 必讀資源

1. **Mamba 原始論文**: Gu & Dao (2023) "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
   - Section 3 是核心（Selective Mechanism 的動機和設計）
   - Section 4（硬體感知）可略讀，理解結論即可

2. **The Annotated SSM** (類似 The Annotated Transformer)
   - https://srush.github.io/annotated-mamba/ 或搜尋 "annotated mamba/h3"
   - 用 JAX 逐步解釋 SSM 的實作

3. **Mamba 官方 repo**: https://github.com/state-ml/mamba
   - `mamba_ssm/modules/mamba_simple.py` — 核心實作
   - 對照 EP S1 的 `MambaBlock`

### 對照 EP S1 的 MambaBlock

EP 的 MambaBlock 結構：

```
Input x
  │
  ├─ → RMSNorm → Mamba(d_model, d_state, d_conv) → + (residual)
  │                                                        │
  └─ → RMSNorm → MLP(d_model → 2*d_model → d_model) → + (residual)
                                                           │
                                                        Output x
```

**與 Transformer Block 的對比**：

| 元件 | Transformer Block | Mamba Block (EP) |
|------|------------------|-----------------|
| Normalization | LayerNorm | RMSNorm（更輕量） |
| 序列處理 | Multi-Head Attention (O(n²)) | Mamba SSM (O(n)) |
| FFN | 通常是 4x 擴展 | 2x 擴展（MLP） |
| Attention mask | 需要 causal mask | 天然 causal（SSM 是因果的） |

### 實作練習

**P0-1: 安裝 mamba-ssm 並跑通基本 forward**

```python
# 安裝: pip install mamba-ssm
# 注意: 需要 CUDA（mamba-ssm 的 GPU kernel 目前不支援 CPU-only）

import torch
from mamba_ssm import Mamba

batch_size = 2
seq_len = 64
d_model = 32

x = torch.randn(batch_size, seq_len, d_model).cuda()
model = Mamba(d_model=d_model, d_state=16, d_conv=4, expand=2).cuda()
y = model(x)

assert y.shape == (batch_size, seq_len, d_model)
print(f"Input: {x.shape} → Output: {y.shape}")
```

**P0-2: 對比 Mamba vs Transformer 的記憶體**

```python
# 觀察 O(n) vs O(n²) 的實際差異
# 序列長度從 128 → 512 → 2048 → 4096
# Mamba 的 GPU 記憶體增長接近線性
# Transformer 的 GPU 記憶體增長接近二次方
```

- 如果沒有 GPU：用 Google Colab（免費 T4 GPU 即可跑 mamba-ssm）
- 觀察：seq_len=4096 時，Mamba 可能只需要 Transformer 一半的記憶體

### 驗證標準

- [ ] 能解釋 SSM 的 h'(t) = Ah(t) + Bx(t) 是什麼意思
- [ ] 能解釋 Mamba 的「選擇性」是什麼（為什麼比普通 SSM 好）
- [ ] 能對照 EP 的 MambaBlock 指出哪裡是 SSM、哪裡是 MLP、哪裡是 residual
- [ ] 能安裝 mamba-ssm 並跑通 forward（形狀正確）
- [ ] 理解為什麼金融序列用 Mamba 比 Transformer 合理

---

## Phase 1: Event Tokenization — 金融市場的 NLP

### 為什麼需要這個 Phase

EP 的核心洞察之一是 **「OHLCV 是原始感測器資料，不是特徵」**。這跟 NLP 的演化完全一致：

```
NLP 的演化:
  原始文字 → 字元 → 子詞 (BPE) → Token → Transformer
                                  ↑ GPT 的核心洞察

金融的演化 (EP 的類比):
  原始 OHLCV → 技術指標 → Event Token → Mamba
                                    ↑ 本 EP 的核心洞察
```

### 核心概念

| 概念 | NLP 類比 | 金融對應 |
|------|---------|---------|
| **Vocabulary** | 字詞表（如 30K tokens） | 市場事件表（如 100 tokens） |
| **Tokenization** | 文字 → token ids | Bar 序列 → event token ids |
| **BOS/EOS/PAD** | 句子開始/結束/填充 | 序列開始/結束/填充（EP 直接沿用） |
| **SEP** | 句子分隔（如 BERT 的 [SEP]） | 資產分隔（多資產序列用） |
| **分箱 (Binning)** | 字頻分箱（BPE） | 特徵值分箱（連續→離散） |

### EP 的 Token 設計解析

EP 將市場狀態拆成幾個維度，每個維度獨立分箱：

```
一個 Bar → 計算特徵 → 各維度分箱 → 組合成一個 Event Token

維度:
  1. 趨勢 (7 states): UP_STRONG / UP / UP_WEAK / FLAT / DOWN_WEAK / DOWN / DOWN_STRONG
  2. 波動率 (3 states): EXPAND / CONTRACT / NORMAL
  3. 成交量 (4 states): SPIKE / DRY / NORMAL / EXPAND
  4. 事件 (8 states): BREAKOUT_UP / BREAKOUT_DOWN / NEW_HIGH / NEW_LOW / ...

組合方式:
  - 預設: "TREND_VOL_VOLUME"（如 "TREND_UP_VOL_NORMAL_V_NORMAL"）
  - 有特殊事件時優先用事件名（如 "BREAKOUT_UP"）
```

**設計關鍵**: 組合後的 token 數量不能太大（否則詞彙表太大，模型難學）。EP 用分類+組合而非笛卡爾積。

### 實作練習

**P1-1: 用合成資料驗證 Tokenizer**

```python
# 建立三種合成 Bar 序列:
# 1. 上升趨勢（close 每步 +1%）
# 2. 下降趨勢（close 每步 -1%）
# 3. 盤整（close 在 MA 附近波動）
#
# Tokenize 後驗證:
# - 上升趨勢的 tokens 應以 TREND_UP 為主
# - 下降趨勢的 tokens 應以 TREND_DOWN 為主
# - 盤整的 tokens 應以 TREND_FLAT + CONSOLIDATION 為主
```

**P1-2: 理解 Token 分佈的重要性**

EP 的成功標準之一是「Token 分佈不極端（任一 token 佔比 < 50%）」。為什麼？

- 如果 90% 的時間都是 TREND_FLAT → 模型學不到有用的模式
- 解決方式：調整分箱閾值，讓各類事件出現頻率相對均衡
- NLP 的類比：如果 90% 的文字都是 "the" → 語言模型學不到語法

**P1-3: 思考 Token 設計的取捨**

EP 的 tokenizer 是手工設計的（hardcoded 分箱閾值）。另一條路是 learnable tokenizer（用 VQ-VAE 或類似方法自動學 token）。思考：

| 方式 | 優點 | 缺點 |
|------|------|------|
| 手工 tokenizer (EP 選擇) | 可解釋、可控、快速實作 | 可能遺漏重要模式 |
| Learnable tokenizer | 可能發現人類沒想到的模式 | 需要額外訓練、難 debug |

### 驗證標準

- [ ] 能解釋為什麼 OHLCV 需要先 tokenize 再進模型
- [ ] 能對照 NLP 的 tokenization 理解 EP 的 Event Token 設計
- [ ] 理解 EP 的 SEP token 在多資產場景的用途
- [ ] 能解釋 token 分佈為什麼不能太極端

---

## Phase 2: Self-Supervised Pre-train

### 為什麼需要這個 Phase

Foundation Model 的核心是「先學通用表示，再學特定任務」。這跟 BERT/GPT 的訓練範式完全一致：

```
NLP:         大量文字 → Pre-train (next-token prediction) → Fine-tune (分類/問答/翻譯)
金融 (EP):   大量 K 線 → Pre-train (next-event prediction) → Fine-tune (交易/配置/拆單)
```

你已經熟悉 BERT 的 masked LM 和 GPT 的 next-token prediction。EP 選擇的是 GPT 路線（自回歸，因果的），因為金融序列是時間序列，未來不能看到過去。

### 核心概念

| 概念 | GPT 類比 | EP 對應 |
|------|---------|---------|
| **Pre-train 目標** | Next-token prediction | Next-event prediction |
| **Loss** | Cross-entropy | Cross-entropy（完全相同） |
| **訓練資料** | 大量文字語料 | 大量歷史 K 線 |
| **評估指標** | Perplexity | Perplexity（完全相同） |
| **Fine-tune 方式** | 加 task head + 少量標註資料 | 加 task head + RL reward |

### 為什麼 pre-train 有價值

EP 的 SM-5 設計了一個對照實驗：有 pre-train vs 無 pre-train。

**理論基礎**：Pre-train 讓模型學會市場的「語法」—— 什麼事件通常跟著什麼事件（如 TREND_UP_STRONG 之後通常是 TREND_UP 或 VOL_EXPAND）。這種通用知識讓 RL fine-tune 不需要從零探索市場結構。

**类比 BERT**: 沒有 pre-train 的 BERT 做情感分類需要大量標註資料；有 pre-train 的 BERT 只需要少量標註資料。同理，沒有 pre-train 的 Mamba 做交易需要大量 RL 探索；有 pre-train 的 Mamba 從「理解市場」開始，只需學「如何決策」。

### EP S3 的 PretrainTrainer 解析

```python
# 訓練迴圈（跟 GPT 訓練幾乎一樣）
for epoch in epochs:
    for batch in dataloader:
        input_ids, target_ids = batch  # 偏移一步的 token 序列
        logits, loss = model(input_ids, targets=target_ids)  # cross-entropy loss
        loss.backward()
        optimizer.step()

    perplexity = exp(avg_loss)  # 評估指標：越低越好
```

**與 GPT 訓練的差異**：
- 序列長度更短（512 vs GPT 的 4096+）
- 詞彙表更小（~100 vs GPT 的 50K+）
- 資料量更少（5 年日 K ≈ 1800 筆 vs GPT 的數十 TB）

**這意味什麼**: 金融 pre-train 計算量很小，可能幾分鐘就能在 GPU 上跑完。不需要分散式訓練。

### 實作練習

**P2-1: 在合成資料上跑通 PretrainTrainer**

```python
# 1. 生成合成 token 序列（用 random + pattern 混合）
# 2. 建立 MambaDataset
# 3. 跑 10 個 epoch
# 4. 觀察:
#    - Loss 從 ~ln(vocab_size) 開始下降
#    - Perplexity 應該逐步下降
#    - 如果 perplexity 不下降 → 檢查 learning rate 或資料
```

**P2-2: 理解 Partial Freezing 策略**

EP 的設計是「凍結前 N-2 層，只 fine-tune 最後 2 層 + task head」：

```
MambaEncoder (8 層):
  Layer 1-6: 凍結 ← pre-train 學到的通用市場知識
  Layer 7-8: 可訓練 ← 適應特定任務
  Task Head: 全新 ← 從零學習任務特定輸出
```

- 為什麼不全部 fine-tune？避免 catastrophic forgetting（忘記 pre-train 學到的通用知識）
- 為什麼不全部凍結？最後幾層需要適應任務特定的模式
- NLP 類比：BERT fine-tune 通常也不凍結，但金融資料少，凍結大部分層更穩定

### 驗證標準

- [ ] 能解釋 next-event prediction 為什麼讓模型學到市場結構
- [ ] 理解 perplexity 作為評估指標的含義
- [ ] 能解釋 partial freezing 的取捨
- [ ] 理解 pre-train 的計算量為什麼很小（vs LLM pre-train）

---

## Phase 3: REINFORCE — 從理解到決策

### 為什麼需要這個 Phase

Pre-train 讓模型「理解」市場（知道什麼事件會跟著什麼事件）。但「理解」不等於「會交易」。REINFORCE 是把理解轉化為決策的方法。

### REINFORCE vs SAC（與 DeepScalper EP 對比）

| 維度 | REINFORCE (Mamba EP) | SAC (DeepScalper EP) |
|------|---------------------|---------------------|
| **類型** | On-policy policy gradient | Off-policy actor-critic |
| **Critic** | 無（不需要 Q-function） | 有（twin critic networks） |
| **Loss** | `-(log π(a\|s) × advantage)` | 3 個 loss（critic + actor + alpha） |
| **資料效率** | 低（不能重用舊資料） | 高（replay buffer 重用舊經驗） |
| **複雜度** | 簡單（~50 行核心程式碼） | 複雜（~200 行核心程式碼） |
| **適合場景** | 已有好的特徵表示（pre-trained） | 從零開始學特徵和策略 |

**EP 選擇 REINFORCE 的理由**：Mamba 已經透過 pre-train 學到了好的市場表示，不需要 complex critic 來學 value function。REINFORCE 夠簡單、夠用。

### REINFORCE 數學（一行公式）

```
∇J(θ) = E[∇log π_θ(a|s) × R]
```

翻譯成白話：
- 「如果某個動作得到了好 reward → 增加選這個動作的機率」
- 「如果某個動作得到了壞 reward → 減少選這個動作的機率」
- `log π(a|s)` 是「選這個動作的機率的 log」
- `R` 是 reward（EP 用 advantage = reward - mean(rewards)）

### EP 的 RLTrainer 實作解析

```python
# 簡化的 REINFORCE 迴圈
for episode in episodes:
    trajectory = []  # 收集 (obs, action, reward)
    obs = env.reset()
    while not done:
        action = model.forward(obs)       # Mamba 輸出動作
        obs, reward, done, _, _ = env.step(action)
        trajectory.append((obs, action, reward))

    # 計算 advantage
    rewards = [r for _, _, r in trajectory]
    advantage = [r - np.mean(rewards) for r in rewards]

    # 更新 policy
    for (obs, action, _), adv in zip(trajectory, advantage):
        log_prob = model.log_prob(obs, action)
        loss -= log_prob * adv  # gradient ascent
    loss.backward()
    optimizer.step()
```

### Reward 設計的三個任務

EP 的三個任務有不同的 reward 設計，理解差異很重要：

| 任務 | Reward | 公式 | 意義 |
|------|--------|------|------|
| **Task C** (單資產交易) | PnL change | `equity[t] - equity[t-1]` | 賺多少 |
| **Task A** (多資產配置) | Risk-adjusted return | `step_return - 0.5 × drawdown` | 賺多少但懲罰回撤 |
| **Task B** (拆單執行) | -Implementation Shortfall | `-(actual_avg - arrival) × qty` | 執行成本多低 |

**Task B 的 reward 最獨特**：不是在問「賺不賺錢」，而是在問「執行得好不好」。一個好的拆單策略可能在一個虧損的交易上仍然做得好（因為它把滑價降到最低）。

### 實作練習

**P3-1: 用 CartPole 驗證 REINFORCE**

```python
# 最簡單的 REINFORCE 驗證
import gymnasium
import torch
import torch.nn as nn

env = gymnasium.make("CartPole-v1")
policy = nn.Sequential(nn.Linear(4, 64), nn.ReLU(), nn.Linear(64, 2), nn.Softmax(dim=-1))
optimizer = torch.optim.Adam(policy.parameters(), lr=1e-2)

for episode in range(500):
    obs, _ = env.reset()
    log_probs, rewards = [], []
    done = False
    while not done:
        probs = policy(torch.FloatTensor(obs))
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        obs, reward, done, truncated, _ = env.step(action.item())
        log_probs.append(dist.log_prob(action))
        rewards.append(reward)
        done = done or truncated

    # REINFORCE update
    returns = torch.FloatTensor(rewards)
    advantage = returns - returns.mean()
    loss = -torch.stack([lp * a for lp, a in zip(log_probs, advantage)]).sum()
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# 驗證: agent 學會平衡桿子（reward > 100）
```

**P3-2: 思考 REINFORCE 的局限性**

- **高方差**: 每次只用一條 trajectory 更新，不同 trajectory 的 reward 差異很大
- EP 的簡化: 用 advantage（減去均值）降低方差
- 進階解法: PPO（限制 policy 更新幅度）、A2C（加 baseline network）
- 為什麼 EP 不用 PPO? 因為 pre-train 已經提供了好的初始化，REINFORCE 就夠了

### 驗證標準

- [ ] 能解釋 REINFORCE 的 `∇log π × R` 是什麼意思
- [ ] 能手寫一個 REINFORCE 訓練迴圈（CartPole 即可）
- [ ] 能對比 REINFORCE vs SAC 的取捨
- [ ] 能解釋三個任務的 reward 設計差異

---

## Phase 4: NT 多任務 Gym — 統一框架

### 為什麼需要這個 Phase

EP 最精巧的設計是 S4（NTGymBase）：一個 Gym 基類，三個任務繼承它只覆寫 4 個方法。理解這個設計模式是實作 S5/S6/S7 的前提。

### Template Method Pattern

EP 的 NTGymBase 使用了經典的 Template Method 設計模式：

```
NTGymBase (抽象基類)
  │
  │  固定的: reset(), step(), _build_observation(), close()
  │  token 管理和 NT streaming 操作
  │
  └── 子類別只需覆寫 4 個方法:
      ├── _setup_engine()      → 建立什麼樣的 BacktestEngine
      ├── _execute_action()    → 怎麼執行 RL agent 的決策
      ├── _compute_reward()    → 用什麼 reward
      └── _sample_episode_bars() → 從哪段歷史訓練
```

**三個子類別的差異**：

| 方法 | Task C (單資產) | Task A (配置) | Task B (拆單) |
|------|----------------|--------------|--------------|
| `_setup_engine` | 1 個 CurrencyPair | 3 個 CurrencyPair | 1 個 CurrencyPair |
| `_execute_action` | 調整持倉比例 | 重新分配權重 | 拆單執行 |
| `_compute_reward` | Δequity | return - drawdown | -IS |
| action_space | Box(-1, 1, (1,)) | Box(-5, 5, (4,)) | Box(0, 1, (2,)) |

### 三個 Task 的 Action Space 設計

**Task C — 單資產交易 (Box(-1, 1, (1,)))**：
```
action[0] = -1.0  → 全做空
action[0] =  0.0  → 平倉
action[0] = +1.0  → 全做多
```
最簡單的設計。對應 DeepScalper EP 的 Box(0, 1) 但擴展到做空。

**Task A — 多資產配置 (Box(-5, 5, (4,)))**：
```
action = [logit_btc, logit_eth, logit_sol, logit_cash]
weights = softmax(action)  → sum to 1.0
```
注意：action 是 logits（不是直接的權重），通過 softmax 轉換。這是因為 RL 的梯度在 softmax 的 logits 上更穩定。

**Task B — 拆單執行 (Box(0, 1, (2,)))**：
```
action[0] = qty_fraction  → 這一步執行剩餘量的多少比例
action[1] = urgency       → 0 = limit order, 1 = market order
```
最獨特的設計。不是決定「要不要交易」，而是「怎麼執行已有的訂單」。

### NT ExecAlgorithm（Task B 的新概念）

Task B 不用 Strategy，而是用 NT 的 ExecAlgorithm。這是一個你可能在 DeepScalper EP 中沒接觸過的 NT 概念：

```
NT 的執行層:
  Strategy → submit_order(大單) → ExecAlgorithm.on_order()
                                          │
                                          ├─ spawn_market(子單1)
                                          ├─ spawn_limit(子單2)
                                          └─ spawn_market(子單3)
                                                  │
                                            BacktestEngine 撮合
```

- `ExecAlgorithm` 是拆單策略的抽象基類
- `on_order(primary)` 收到母單
- `spawn_market() / spawn_limit()` 生成子單
- EP 的 `MambaExecAlgorithm` 就是讓 Mamba policy 決定怎麼拆

### 實作練習

**P4-1: 讀 NT 的 TWAP ExecAlgorithm 範例**

在 nautilus_trader repo 中找到 TWAP 範例（`nautilus_trader/nautilus_trader/examples/algorithms/twap.py` 或相關位置），理解：

1. `ExecAlgorithm.on_order()` 的觸發時機
2. `spawn_market()` / `spawn_limit()` 的用法
3. 母單和子單的關係

**P4-2: 在紙上設計第四個 Task**

EP 已定義 Task A/B/C。嘗試設計 Task D（例如：擇時進出場 + 風控），回答：
- action_space 是什麼？
- reward 怎麼設計？
- 需要哪些 NT API？

### 驗證標準

- [ ] 能解釋 NTGymBase 的 Template Method 設計
- [ ] 能對比三個 Task 的 action_space 差異和設計理由
- [ ] 理解 ExecAlgorithm 與 Strategy 的角色差異
- [ ] 能解釋 Task B 的 Implementation Shortfall reward

---

## Phase 5: EP 實作 — S1 到 S7

### 實作順序與依賴（重複 EP 的依賴圖）

```
S1（基礎設施）→ S2（Tokenizer）→ S3（Pre-train）
                                    ↓
                              S4（RL Gym）
                              ↙    ↓    ↘
                        S5(Task C) S6(Task A) S7(Task B)
```

### 建議的實作策略

#### 先做 S1+S2（不需要 GPU）

```
S1: MambaEncoder + MambaBlock + Task Heads
    - 先測 pre-train mode (task_head_type="none")
    - 再測各 task head 的輸出形狀和範圍

S2: EventVocabulary + MarketEventTokenizer
    - 先用合成資料驗證
    - 再用真實 BTC daily bars 驗證 token 分佈
```

#### S3 需要短暫的 GPU 時間

```
S3: PretrainTrainer
    - BTC 5 年日 K ≈ 1800 筆 → token 序列
    - seq_len=512, batch=32, 50 epochs
    - 預估: 單 GPU 幾分鐘即可完成
    - 驗證: perplexity < 20
```

#### S4 可以在 CPU 上開發

```
S4: NTGymBase
    - NT streaming mode 已 POC 驗證
    - 先用 no-op 子類別測試基類
    - 確認 obs 是合法 token sequence
```

#### S5/S6/S7 平行開發（建議先做 S5）

```
建議順序: S5 → S6 → S7

S5 最簡單（單資產），驗證整個 pre-train → RL fine-tune 路線可行
S6 加入多資產（SEP token、softmax action）
S7 換成 ExecAlgorithm（需要理解 NT ExecAlgorithm 介面）
```

### 各 Segment 的核心挑戰

| Segment | 挑戰 | 降險策略 |
|---------|------|---------|
| S1 | Mamba 的 CUDA kernel 可能不相容某些 GPU 版本 | 先在 Colab T4 驗證 |
| S2 | Token 分佈極端（大部分時間 TREND_FLAT） | 調整分箱閾值，增加細分 |
| S3 | Pre-train loss 不下降 | 檢查 tokenizer 的 token 分佈；降低 lr |
| S4 | NT streaming mode 和 Gym 的同步 | 已有 POC 驗證，照 POC 的模式寫 |
| S5 | REINFORCE 方差太大導致不收斂 | 增加 episode batch（多條 trajectory 取平均） |
| S6 | 多資產 order 的 delta 計算錯誤 | 先用 equal-weight 固定 action 驗證環境 |
| S7 | IS 計算不直觀，容易有 bug | 先用 fixed TWAP action 當 baseline 對照 |

### 最關鍵的實驗：SM-5（有 pre-train vs 無 pre-train）

EP 的 Scenario Matrix 裡 SM-5 是最重要的實驗：

```
實驗設計:
  A: S3 pre-train → S5 RL fine-tune → 量測收斂速度和最終 Sharpe
  B: 直接 S5 RL fine-tune（跳過 S3）→ 量測收斂速度和最終 Sharpe

預期: A 的收斂速度 > B 的至少 2x
如果不符合 → 檢查 tokenizer 設計或 pre-train 充分性
```

這個實驗驗證了整個 Foundation Model 路線的核心價值。如果 pre-train 沒幫助，整個 S2+S3 就是浪費。

---

## 附錄: 與 DeepScalper EP 的知識共享

如果你已經完成（或正在學習）DeepScalper EP 的學習計畫，以下是兩者共享的知識：

### 可以直接從 DeepScalper EP 帶過來的

| 知識 | DeepScalper EP 來源 | Mamba EP 用途 |
|------|--------------------|----|
| NT BacktestEngine streaming mode | Phase 3 + S1 | S4 的 NTGymBase |
| NT Strategy + submit_order | S2 | S5/S6 的 action 執行 |
| NT portfolio.equity() | S1 | S5/S6 的 reward 計算 |
| Gym API (reset/step/done) | Phase 1 | S4 的 NTGymBase |
| Walk-forward validation 概念 | S5 | RL fine-tune 的資料分割 |
| Sharpe ratio 計算 | S5 | 最終績效評估 |

### 需要額外學的（Mamba EP 獨有）

| 知識 | Phase | 為什麼 DeepScalper 不需要 |
|------|-------|------------------------|
| Mamba SSM 架構 | Phase 0 | DeepScalper 用 MLP |
| Event Tokenization | Phase 1 | DeepScalper 用手工特徵 |
| Self-supervised pre-train | Phase 2 | DeepScalper 端對端訓練 |
| REINFORCE policy gradient | Phase 3 | DeepScalper 用 SAC |
| ExecAlgorithm 介面 | Phase 4 | DeepScalper 只用 Strategy |
| Multi-task learning | Phase 5 | DeepScalper 單一任務 |

### 可以互補驗證的

做完兩個 EP 後，可以在同一組 BTC 資料上對比：

```
實驗:
  - DeepScalper (SAC + MLP): 82 維特徵 → QNet → discrete/continuous action
  - Mamba Task C (REINFORCE + SSM): Event Tokens → Mamba → continuous action

對比維度:
  - Out-of-sample Sharpe ratio
  - 訓練收斂速度
  - 記憶體用量
  - 推論延遲
  - 多資產擴展的難易度
```

---

## 附錄: 常見問題

### Q1: Mamba 一定要用 GPU 嗎？

`mamba-ssm` 的核心 SSM kernel 是 CUDA-only。替代方案：
- **Google Colab** (免費 T4) — 最簡單
- **CPU fallback**: 用 `mamba_ssm` 的純 PyTorch 模式（速度慢但可跑）
- **Mac MPS**: 目前 mamba-ssm 不支援 MPS backend

### Q2: Pre-train 的資料量夠嗎？

5 年 BTC daily ≈ 1800 bars → tokenize 後約 1800 tokens。這對語言模型來說極少，但：
- 金融 token 的信息密度比文字高（每個 token 是一個市場狀態）
- Mamba 的參數量比 LLM 小很多（d_model=256, 8 layers）
- 如果 perplexity 不收斂 → 可以加入更多資產的資料（ETH/SOL），用 SEP token 連接

### Q3: REINFORCE 比 SAC 差很多嗎？

理論上 SAC 的 sample efficiency 更好。但：
- REINFORCE 更簡單、更容易 debug
- Pre-trained Mamba 的特徵已經很好，不需要 complex critic
- 如果 REINFORCE 效果不夠 → 可以升級到 PPO（增加 clipping）

### Q4: 三個 Task 一定要全做嗎？

不需要。最小可運行集合是 S1+S2+S3+S4+S5（只做 Task C）。S6 和 S7 可以視需求追加。

### Q5: Tokenizer 的分箱閾值怎麼定？

EP 沒有給出具體數值（如「MA slope > 0.5% 才算 TREND_UP」）。實作時：
- 先用統計分位數（如 top/bottom 25%）
- 觀察 token 分佈，調整到相對均衡
- 這是一個 hyperparameter，可以 grid search
