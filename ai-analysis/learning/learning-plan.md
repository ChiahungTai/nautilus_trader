# RL Trading 學習計畫

> **起點**: 已熟悉 BERT/CNN（deep learning 基礎），不了解 RL
> **終點**: 能獨立實作 EP `nt-gym-deepscalper.md` 的 S1-S5，並具備往多資產+分批下單擴展的能力
> **資料**: 有自己的資料管線，不需學資料處理
> **執行引擎**: NautilusTrader（需理解其架構）

---

## 學習地圖總覽

```
Phase 0          Phase 1           Phase 2            Phase 3           Phase 4           Phase 5
RL 基礎          Gym 環境          DQN → SAC          NT 架構           EP 實作           多資產擴展
(MDP/Bellman)    (Env API)         (連續控制)          (核心概念)         (S1-S5)           (目標架構)
    │                │                 │                 │                 │                 │
    └──── 先修 ────→ └──── 先修 ────→ ─┘                 │                 │                 │
                                                        └── 先修 ────→ ───┘                 │
                                                                                            ↑ 延伸閱讀
```

- Phase 0-2 是 RL 知識（用 TradeMaster 程式碼當教材）
- Phase 3 是 NT 平台知識（讀原始碼+文件）
- Phase 4 是 EP 實作（融合前面所有知識）
- Phase 5 是延伸方向（朝你的終極目標推進）

---

## Phase 0: RL 基礎 — 從 DL 到 RL 的認知轉換

### 為什麼需要這個 Phase

DL 的學習範式是「給 input-output pair，最小化 loss」。RL 的範式完全不同：沒有標準答案，agent 透過與環境互動獲得 reward，自己發現好策略。這個認知轉換是最大的門檻。

### 核心概念

| 概念 | 一句話解釋 | DL 類比 |
|------|-----------|---------|
| **MDP** (Markov Decision Process) | 環境的形式化描述：state, action, reward, transition | — |
| **Policy π(a\|s)** | 給定狀態，選擇行動的機率分布 | 類似 classifier，但輸出是動作機率 |
| **Value function V(s)** | 處於狀態 s 的預期長期回報 | — |
| **Q-function Q(s,a)** | 在狀態 s 執行動作 a 後的預期長期回報 | — |
| **Bellman Equation** | V/Q 的遞迴定義：當前價值 = 即時 reward + 折扣後的未來價值 | 類似 recursion base case + inductive step |
| **Exploration vs Exploitation** | 嘗試新行動 vs 利用已知好行動的取捨 | DL 無此概念（有監督信號） |
| **On-policy vs Off-policy** | 用自己當前策略收集的資料學習 vs 用舊策略的資料也能學習 | SGD（每批更新） vs Mini-batch（重用舊資料） |

### 必讀資源（建議順序）

1. **Sutton & Barto "Reinforcement Learning: An Introduction"** Chapter 3-4（MDP + DP）
   - 免費線上版：http://incompleteideas.net/book/the-book.html
   - 只需讀懂 Bellman equation 的推導，不需要精通所有 DP 演算法

2. **Spinning Up 的 "Key Concepts"**（OpenAI 出品，極簡潔）
   - https://spinningup.openai.com/en/latest/spinningup/rl_intro.html
   - 搭配 Part 1-3 的交互式圖解

3. **David Silver RL Course Lecture 1-5**（影片）
   - https://www.davidsilver.uk/teaching/
   - Lecture 1（MDP）+ Lecture 5（DQN）最重要，其餘可選讀

### 實作練習

**P0-1: 用 NumPy 實作 Q-Learning on FrozenLake**

```python
# 目標：理解 Q-table update 的本質
# Q(s,a) ← Q(s,a) + α[r + γ·max_a'Q(s',a') - Q(s,a)]
# 不用 PyTorch，純 NumPy，確認你理解 Bellman update
```

- 驗證：agent 學會走到目標不落水
- 對照：`TradeMaster/trademaster/agents/algorithmic_trading/dqn.py` 的 `get_obj_critic()` 就是這個 update 的 PyTorch 版本

### 驗證標準

- [ ] 能解釋 Q(s,a) 和 V(s) 的差異
- [ ] 能手寫 Bellman update 的公式
- [ ] 理解 exploration（ε-greedy）為什麼必要
- [ ] 能指出 TradeMaster DQN agent 中哪些行對應 Q-learning update

---

## Phase 1: Gym 環境設計 — 理解 Env 介面

### 為什麼需要這個 Phase

EP 的 S1 就是建構 Gym 環境。不理解 Gym API，後面的 agent 無法運作。Gym 環境是 RL 系統的「合約」——定義 agent 看到什麼、能做什麼、得到什麼評價。

### 核心概念

| Gym API 元素 | 作用 | EP 對應 |
|-------------|------|---------|
| `reset()` → (obs, info) | 開始新 episode，回傳初始狀態 | S1: 建立新 BacktestEngine |
| `step(action)` → (obs, reward, done, truncated, info) | 執行一步，回傳結果 | S1: 注入 bar → run streaming → 提取狀態 |
| `observation_space` | 狀態的維度和資料型別定義 | S3: ObservationSpec |
| `action_space` | 允許的行動空間 | EP 選用 `Box(0, 1)` continuous |
| `reward` | 即時評價信號 | S1: EquityChangeReward / RiskAwareReward |

### 實作練習

**P1-1: 讀懂 TradeMaster 的環境**

追蹤這個呼叫鏈，理解每一步：

```
tools/algorithmic_trading/train.py
  → build_environment(cfg)     # 建構環境
  → env.reset()                # 初始化
  → agent.explore_env(env)     # 互動收集經驗
```

具體閱讀順序：
1. `trademaster/environments/algorithmic_trading/environment.py` — 完整的 Gym 環境
   - `reset()`: 載入資料、初始化持倉
   - `step(action)`: 執行交易、計算 reward（注意 hindsight reward 的問題！）
   - `_get_observation()`: 組裝 82 維狀態向量
2. `trademaster/environments/custom.py` — 基類 `Environments(gym.Env)`
3. 對照 EP S1 的 `NTEngine` pseudo code — 理解兩者的異同

**P1-2: 寫一個最簡單的 Gym 環境**

```python
import gymnasium
import numpy as np

class SimpleTradingEnv(gymnasium.Env):
    """最簡化的交易環境：1 檔股票，3 個 action（buy/hold/sell）"""
    observation_space = ...
    action_space = ...

    def reset(self, seed=None, options=None): ...
    def step(self, action): ...
```

- 用 random data（np.random 生成的價格序列）
- 不需要 NT，純 Python + NumPy
- 驗證：random agent 能跑完一個 episode 不 crash

### TradeMaster 環境的設計教訓（從 EP 的弱點分析學習）

EP 識別了 DeepScalper 原始環境的 12 個弱點，其中 **5 個是環境設計問題**：

| 弱點 | 原始設計 | EP 改進 | 學習要點 |
|------|---------|---------|---------|
| W3 無滑價 | 假設以收盤價成交 | NT OneTickSlippageFillModel | 環境必須模擬真實撮合 |
| W4 簡化手續費 | flat 0.1% | NT MakerTakerFeeModel | 手續費結構影響策略 |
| W5 未來資訊洩漏 | 用未來 5 天均價算 reward | 真實 Δequity | **最致命的設計缺陷** |
| W6 無風控 | 無停損/最大持倉 | NT RiskEngine | 風控是生產環境的硬需求 |
| W10 無破產終止 | 可以虧到負數 | equity < 10% → done | 終止條件影響學習穩定性 |

> 💡 **核心教訓**：RL 環境的設計直接決定 agent 能學到什麼。一個有 lookahead bias 的環境，agent 會學到「不可能的策略」—— 在真實市場中完全失效。

### 驗證標準

- [ ] 能解釋 Gym 的 `reset/step/done` 生命週期
- [ ] 能指出 TradeMaster 環境的 W5（lookahead bias）具體在哪幾行程式碼
- [ ] 能手寫一個可運行的 Gym 環境（不依賴 NT）
- [ ] 理解為什麼 EP 選擇 continuous `Box(0,1)` 取代 discrete `Discrete(3)`

---

## Phase 2: 從 DQN 到 SAC — 離散到連續的演算法演進

### 為什麼需要這個 Phase

EP 選擇 SAC（Soft Actor-Critic）作為 agent 演算法，而非原始 DeepScalper 的 DQN。你需要理解這條演進路徑：DQN → DDPG → TD3 → SAC，每一步解決了前一個的什麼問題。

### 演算法演進樹

```
Q-Learning (tabular)
  └→ DQN (Deep Q-Network)              ← Phase 0 已學
       │  解決：高維狀態空間
       │  限制：只能處理離散 action
       │
       └→ DDPG (Deep Deterministic PG)  ← 連續 action 的第一步
            │  解決：連續 action space
            │  限制：Q-value overestimate → 訓練不穩定
            │
            ├→ TD3 (Twin Delayed DDPG)
            │    解決：overestimate（twin critic + delayed update）
            │    限制：deterministic policy → exploration 不足
            │
            └→ SAC (Soft Actor-Critic)   ← EP 選擇的演算法
                 解決：所有上述問題
                 優勢：
                 1. 自動 entropy tuning → exploration/exploitation 自動平衡
                 2. Twin critic → 避免 overestimate
                 3. Stochastic policy → 更好的 exploration
                 4. Sample efficiency 好
```

### DQN：你已經有程式碼可以讀

TradeMaster 的 DQN 是最好的學習起點，因為程式碼簡單且完整：

| 元件 | TradeMaster 路徑 | 職責 |
|------|-----------------|------|
| Q-Network | `trademaster/nets/dqn.py:QNet` | MLP: 82→64→32→3，輸出每個 action 的 Q 值 |
| Agent | `trademaster/agents/algorithmic_trading/dqn.py` | explore_env + Q-learning update + soft_update |
| Trainer | `trademaster/trainers/algorithmic_trading/trainer.py` | epoch 迴圈：explore → update → validate |
| Replay Buffer | `trademaster/utils/general_replay_buffer.py` | 儲存 (s, a, r, s', done) tuples |
| Config | `configs/algorithmic_trading/...deepscalper...py` | 所有超參數 |

**閱讀重點**：
- `dqn.py:get_obj_critic()` 的 loss 計算：`F.mse_loss(q_value, target_q_value.detach())`
- `dqn.py:soft_update()` 的 target network 更新（注意 EP 指出 tau=0 的 bug）
- `trainer.py` 的 explore → update 循環

### SAC：EP 的核心演算法

SAC 的核心創新是 **entropy-regularized RL**：在最大化 expected return 的同時，也最大化 policy 的 entropy（隨機性）。這讓 agent 自然地保持 exploration。

SAC 的 loss 有三個：

| Loss | 公式（簡化） | 作用 |
|------|-------------|------|
| **Critic Loss** | `MSE(Q(s,a), r + γ(min(Q̃₁, Q̃₂) - α·log π))` | 學習準確的 Q 值 |
| **Actor Loss** | `E[α·log π(a\|s) - min(Q₁, Q₂)]` | 學習好策略 |
| **Alpha Loss** | `-α·(log π + target_entropy)` | 自動調整 exploration 程度 |

**對照 EP S4 的 pseudo code**：
- `DeepScalperAgent.update()` 中的 `critic_loss`、`actor_loss`、`alpha_loss` 分別對應上面三個 loss
- `_soft_update_targets()` 對應 DQN 的 target network soft update（但修復了 tau=0 的 bug）

### 實作練習

**P2-1: 手動追蹤 DQN 的一次 update**

用紙筆或 Jupyter notebook：
1. 給定一個 transition：(s=82d, a=1, r=0.5, s'=82d, done=False)
2. 計算 Q(s, a)、target Q、loss、梯度更新方向
3. 確認你理解 `target_q.detach()` 為什麼必要（DL 類比：stop gradient）

**P2-2: 理解 continuous action space 的挑戰**

DQN 的 Q(s,a) 對每個 discrete action 都有一個值。但 action 是連續時（如 EP 的 [0, 1]），不可能列舉所有 action。

- DDPG 的解法：用 actor network 直接輸出最佳 action，critic 只評價這個 action
- SAC 的改進：actor 輸出一個分佈（mean + std），從中採樣 action

閱讀 EP S4 的 `SACActorNetwork`：
- `sample_action()`: 從 Normal(mean, std) 採樣 → squashed to [0,1]
- `mean_action()`: 推論時直接用 mean（deterministic）

**P2-3（推薦）: 用 Stable-Baselines3 跑一個 SAC 範例**

```python
# 安裝: pip install stable-baselines3[extra]
import gymnasium
from stable_baselines3 import SAC

env = gymnasium.make("Pendulum-v1")  # 連續控制經典環境
model = SAC("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# 驗證：agent 學會平衡鐘擺
obs, _ = env.reset()
for _ in range(200):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, _ = env.step(action)
    if done or truncated:
        break
```

- 目標：觀察 SAC 的訓練過程（entropy 從高到低、reward 從低到高）
- 不需要自己實作 SAC，先「用」再「造」

### 進階閱讀（Phase 2 完成後再讀）

- **SAC 原始論文**: Haarnoja et al. (2018) "Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL with a Stochastic Actor"
- **Spinning Up SAC 實作**: https://spinningup.openai.com/en/latest/algorithms/sac.html — 有完整的 pseudo code
- **TradeMaster 的 SAC 實作**: `pm/agent/sac/mask_sac.py:AgentMaskSAC` — 帶 maskable representation 的進階版

### 驗證標準

- [ ] 能解釋 DQN 為什麼只能處理離散 action
- [ ] 能解釋 SAC 的三個 loss 各自的角色
- [ ] 理解 entropy regularization 的意義（為什麼「鼓勵隨機性」反而學得更好）
- [ ] 能對照 EP 的 pseudo code 指出 critic loss / actor loss / alpha loss
- [ ] 能用 SB3 的 SAC 訓練一個簡單環境

---

## Phase 3: NautilusTrader 架構理解

### 為什麼需要這個 Phase

EP 的核心價值是「訓練環境 = 生產環境」。不理解 NT 的核心概念，無法正確實作 S1（Gym wrapper）和 S2（Strategy Bridge）。

### 必須理解的 NT 核心概念

| 概念 | NT 類別 | 在 EP 中的角色 |
|------|---------|---------------|
| **BacktestEngine** | `nautilus_trader/backtest/engine.pyx` | S1 的核心引擎，Gym wrapper 包裝它 |
| **Strategy** | `nautilus_trader/trading/strategy.pyx` | S2 的基類，agent 透過它下單 |
| **Portfolio** | `nautilus_trader/portfolio/base.pyx` | 提供 equity/PnL（S1 的 reward 來源） |
| **Cache** | `nautilus_trader/cache/base.pyx` | 提供持倉/訂單查詢（S3 的狀態來源） |
| **Streaming Mode** | `engine.run(streaming=True)` | S1 的 step-by-step 執行關鍵 |
| **FillModel** | `nautilus_trader/backtest/models/fill.pyx` | 撮合模型（滑價模擬，解決 W3） |
| **FeeModel** | `nautilus_trader/backtrack/models/fee.pyx` | 手續費模型（解決 W4） |
| **Bar** | `nautilus_trader/model/data/bar.pyx` | OHLCV 資料（S3 的特徵輸入） |
| **CurrencyPair** | `nautilus_trader/instruments/` | 交易工具定義（S5 的資料載入） |
| **InstrumentId** | `nautilus_trader/model/identifiers.pyx` | 工具識別（如 "BTC-USD.SIM"） |

### NT 的 Streaming Mode（EP 的技術核心）

EP S1 的 `step()` 流程：

```
step(action)
  ├─ strategy.set_action(action)         # 注入 RL agent 的決策
  ├─ engine.add_data([data_point])       # 注入一個 bar 的資料
  ├─ engine.run(streaming=True)          # 執行一個 tick 的模擬
  ├─ engine.clear_data()                 # 清除已處理的資料
  ├─ 提取新狀態 (portfolio.equity, cache.positions)
  ├─ 計算 reward (new_equity - prev_equity)
  └─ 回傳 (obs, reward, done, truncated, info)
```

這是 EP 最精巧的設計：把 NT 的批次回測引擎變成 step-by-step 的 Gym 環境。

### 實作練習

**P3-1: 閱讀 EP 的 POC 驗證結果**

EP 已通過 POC 驗證（S1 和 S2 各有 ✅）。閱讀 EP 中標注的 POC 驗證要點，理解哪些 NT API 被證實可行：

- `portfolio.equity()` 回傳 `dict[Currency, Money]`，需 `.as_double()` 轉 float
- `StrategyConfig` 是 frozen msgspec Struct → EP 用 dataclass 繞過
- `Quantity` 建構子只接受 `(value, precision)`
- `AggregationSource.EXTERNAL` 必須明確指定

**P3-2: 閱讀 NT 的 backtest example**

在 nautilus_trader repo 中找到 backtest 相關的 example（`nautilus_trader/nautilus_trader/examples/` 或文件中的範例），理解：

1. BacktestEngine 如何建立和配置
2. Strategy 如何訂閱資料和提交訂單
3. `on_bar()` / `on_order_filled()` 的回調機制
4. `add_data()` → `run()` 的基本流程

### 驗證標準

- [ ] 能解釋 BacktestEngine 的 streaming mode 和 batch mode 的差異
- [ ] 理解 Strategy 的生命週期（on_start → on_bar → on_order_filled）
- [ ] 能解釋 EP 為什麼選擇 `MARGIN` 帳戶而非 `CASH` 帳戶（F1 修正）
- [ ] 理解 `StrategyConfig` 是 frozen 的限制和 EP 的繞過方式

---

## Phase 4: EP 實作 — S1 到 S5

### 實作順序與依賴

```
S1: NT Gym Environment Core     ← 先做這個（主線）
 ├─ S2: RL Strategy Bridge      ← 可與 S3 平行
 ├─ S3: Feature Engineering     ← 可與 S2 平行
 └──────→ S4: Improved DeepScalper ──→ S5: Training Pipeline
```

### 每個 Segment 的學習焦點

#### S1: NT Gym Environment Core

**你需要已經會的**：Phase 1（Gym API）+ Phase 3（NT 核心概念）

**S1 的核心挑戰**：
- NT BacktestEngine 不是為 step-by-step 設計的 → 用 streaming mode 變通
- `portfolio.equity()` 的型別轉換（dict → float）
- 破產終止條件的閾值選擇

**實作步驟**：
1. 先寫 `NTEngineConfig` dataclass
2. 實作 `reset()`：建立 BacktestEngine + 添加 venue/instrument/strategy
3. 實作 `step()`：add_data → run(streaming=True) → clear_data → 提取狀態
4. 實作 `_check_done()`：破產 + 資料耗盡 + max_steps
5. 實作 `EquityChangeReward` 和 `RiskAwareReward`

**驗證**：
- `examples/minimal_gym_env.py`: reset → step 10 次 → close
- `examples/gym_random_agent.py`: random action 跑完整 episode

#### S2: RL Strategy Bridge

**你需要已經會的**：Phase 3（NT Strategy 基類）

**S2 的核心挑戰**：
- `StrategyConfig` 是 frozen msgspec Struct → 用 `RLStrategyConfig` dataclass 繞過
- Action injection 的同步問題：Gym `step()` 呼叫 `set_action()`，Strategy `on_bar()` 消費 action
- Continuous action → order 的 delta 計算（target_weight → 目標金額 → 買/賣數量）

**關鍵計算**：
```python
target_value = equity * target_weight
delta_value = target_value - current_position_value
# 如果 |delta_value| < 1 個價格單位 → skip（避免過度交易）
# 否則 → 計算 quantity → submit market order
```

#### S3: Feature Engineering Bridge

**你需要已經會的**：Phase 1（observation 設計）

**S3 的核心挑戰**：
- Running normalization（Welford 線上演算法）：避免 lookahead bias
- Lookback window 管理：不足時回傳零向量
- Portfolio features 的歸一化（cash/equity, position/equity）

**TradeMaster 對照**：
- 原始 DeepScalper 用 16 個指標 × 5 天 = 80 維 + 2 維 portfolio = 82 維
- EP 改用更精簡的特徵集（11 個指標 × lookback_window + 2 維 portfolio）
- 兩者都做 z-score，但 EP 改用 running normalization（更正確）

#### S4: Improved DeepScalper Agent

**你需要已經會的**：Phase 2（SAC 演算法）

**S4 的核心是 SAC 實作**，但不是從零開始。建議策略：

1. **先從最簡單的 DQN 開始驗證 S1+S2+S3**：用你已經熟悉的 Q-learning 確認環境和策略橋接正確
2. **確認環境正確後再換 SAC**：避免同時 debug 環境和演算法

**SAC 實作的關鍵檔案**：
```
nautilus_gym/agents/
├── deep_scalper.py    # Agent 主類（store_transition + update + save/load）
├── networks.py        # SACActorNetwork + SACCriticNetwork
└── replay_buffer.py   # PrioritizedReplayBuffer（SumTree）
```

**EP 修復的 12 個弱點中，S4 負責的**：

| 弱點 | 修復方式 | 你需要理解的 |
|------|---------|-------------|
| W1 tau=0 | `tau=0.005` soft update | `_soft_update_targets()` |
| W2 固定 epsilon | Gaussian noise σ 衰減 | `_current_noise_sigma()` |
| W7 無正規化 | RunningMeanStd | FeatureEngine 的 normalizer |
| W9 固定 1 單位 | Continuous action | SACActorNetwork 的 sigmoid output |
| W11 用 return 選模型 | Sharpe ratio | Training pipeline 的 model selection |

#### S5: Training Pipeline + Walk-Forward

**你需要已經會的**：Phase 2（訓練迴圈概念）

**S5 的核心概念**：

- **Walk-forward validation**：滾動窗口，避免 overfitting 到特定時期
  - window 1: [train 1 | val 1 | test 1]
  - window 2: [train 2 | val 2 | test 2]
  - window 3: [train 3 | val 3 | test 3]
- **Model selection by Sharpe ratio**（非 total return）
- **BTC CSV → NT Bar 轉換**

**驗證**：
- `examples/walkforward_btc.py`: 完整 walk-forward 訓練
- Out-of-sample Sharpe > 0（最基本的門檻）

### Phase 4 的學習策略

1. **不要一次寫完再測**。每個 Segment 完成後立即驗證（漸進式驗證）
2. **先用 random agent 測環境**。確認 S1+S2+S3 正確後再接入 SAC
3. **過度擬合是正常的**。第一版 agent 大概率 overfit，關鍵是觀察 train vs val 的差距
4. **Hyperparameter 不用完美**。EP 已給出合理的預設值（lr=3e-4, tau=0.005, gamma=0.99）

---

## Phase 5: 多資產+分批下單 — 朝終極目標推進

> ⚠️ 這是 Phase 4 完成後的延伸方向，不是獨立可學的。先完成 EP 再來這裡。

### 你的終極目標拆解

```
目標: Intraday + 多檔股票 + 分幾次買
         │          │          │
         ↓          ↓          ↓
     頻率問題    選股問題    執行問題
     (日內)    (多資產)   (分批下單)
         │          │          │
         ↓          ↓          ↓
     需要更高     需要       需要
     頻率的資料  Portfolio  Order Execution
                 Management  Agent
```

這是一個**階層式 RL**問題，可以用兩層 agent 解決：

```
上層: Portfolio Management Agent
  - 輸入: 所有候選股票的狀態
  - 輸出: 每檔股票的目標權重 (target_weight_1, ..., target_weight_N)
  - 演算法: 類似 EIIE / SARL（TradeMaster 有實作可參考）
  - 頻率: 較低（如每 30 分鐘決定一次配置）

下層: Order Execution Agent
  - 輸入: 上層給的目標權重 + 當前市場狀態
  - 輸出: 當前這一刻要執行的量（分批買入）
  - 演算法: 類似 PD / ETEO（TradeMaster 有實作可參考）
  - 頻率: 較高（如每 5 分鐘執行一次）
```

### 從 EP 到終極目標的路徑

| 步驟 | 基礎 | 擴展方向 | 可參考 |
|------|------|---------|--------|
| 1 | EP 完成（單資產 BTC + SAC） | — | — |
| 2 | 單資產 → 多資產 | observation 自動擴展，action 維度變成 N | TradeMaster `pm/agent/` |
| 3 | DQN/SAC → Portfolio agent | 選擇演算法（EIIE / SARL / PPO） | TradeMaster `trademaster/agents/portfolio_management/` |
| 4 | 單次下單 → 分批下單 | 加入 execution agent | TradeMaster `trademaster/agents/order_execution/` |
| 5 | 兩層 agent 的協調 | 上層決策 → 下層執行 | TradeMaster PD 的 teacher-student 架構 |

### TradeMaster 中可借鑑的架構

| 你的需求 | TradeMaster 實作 | 路徑 |
|---------|-----------------|------|
| 多資產配置 | EIIE（ensemble method） | `trademaster/agents/portfolio_management/eiie/` |
| 多資產 + attention | SARL（self-attention） | `trademaster/agents/portfolio_management/sarl/` |
| 多資產 + maskable | MaskSAC（EarnMore） | `pm/agent/sac/mask_sac.py` |
| 分批執行 | PD（Price Driven, teacher-student PPO） | `trademaster/agents/order_execution/pd/` |
| 分批執行 | ETEO（End-to-End Order Execution） | `trademaster/agents/order_execution/eteo/` |

### 進階閱讀（Phase 5 準備用）

- **EIIE 論文**: Yu et al. (2019) "A Reinforcement Learning Framework for Portfolio Management"
- **SARL 論文**: Ye et al. (2020) "Reinforcement Learning based Portfolio Management with Attention"
- **PD 論文**: Lin & Beling (2020) "An End-to-End Optimal Trade Execution Framework based on Reinforcement Learning"
- **EarnMore 論文**: Feng et al. (2024) "EarnMore: Portfolio Management with Maskable Stock Representation"

---

## 附錄: 常見問題與除錯指南

### Q1: 訓練時 reward 一直下降怎麼辦？

**診斷順序**：
1. 先用 random agent 跑，確認 reward 不是負無限大（環境 bug）
2. 檢查 reward scaling（Δequity 的量級可能太大或太小）
3. 降低 learning rate（1e-3 → 3e-4）
4. 增加 warmup steps（1000 → 5000）

### Q2: Agent 只會 hold 不交易？

**常見原因**：
- Reward 的交易成本太高（手續費 > 可能的收益）
- Exploration 不足（noise sigma 太小）
- Action 的 dead zone 太大（EP 設 1% 門檻，可能需要調低）

### Q3: SAC 的 alpha 不收斂？

**檢查**：
- `target_entropy = -action_dim`（EP 設為 -1）
- Alpha optimizer 的 learning rate（預設 3e-4 通常 OK）
- 如果 alpha 持續變大 → agent 覺得探索比利用重要 → 可能 reward signal 太弱

### Q4: NT BacktestEngine 記憶體持續增長？

EP S1 的 `reset()` 用建立新 engine instance（而非 `engine.reset()`）來確保乾淨狀態。如果仍有洩漏：
- 檢查 `clear_data()` 是否在每次 step 後被呼叫
- 檢查 Strategy 的 `_fills` list 是否在 `on_reset()` 中被清空

### Q5: Sharpe ratio 計算結果不合理？

EP S5 的 Sharpe 計算：
```python
returns = np.diff(equity_curve) / equity_curve[:-1]
sharpe = np.mean(returns) / (np.std(returns) + 1e-8) * np.sqrt(252)
```
- `np.sqrt(252)` 是年化因子（假設日頻資料）
- 如果 equity_curve 太短（< 10 步），Sharpe 不穩定是正常的
- 確認 equity_curve 是 float list（不是 dict 或其他型別）

---

## 學習時間建議

| Phase | 複雜度 | 核心交付物 |
|-------|--------|-----------|
| Phase 0 | 中 | 理解 Bellman equation + Q-learning |
| Phase 1 | 中 | 手寫簡單 Gym 環境 + 讀懂 TradeMaster 環境 |
| Phase 2 | 高 | 理解 SAC 三個 loss + 用 SB3 跑通範例 |
| Phase 3 | 中 | 理解 NT streaming mode + Strategy 生命週期 |
| Phase 4 | 最高 | 完整實作 EP S1-S5，out-of-sample Sharpe > 0 |
| Phase 5 | 高 | 多資產 + 分批下單的架構設計 |

Phase 0-3 是知識儲備，Phase 4 是核心實作，Phase 5 是延伸方向。
