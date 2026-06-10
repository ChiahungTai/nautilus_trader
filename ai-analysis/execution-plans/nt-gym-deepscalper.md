# EP: NT Gym Environment + Improved DeepScalper

## 實作總覽

**目標**：建構 NautilusTrader 的 Gym wrapper（Path E），讓 RL agent 能在 NT 的真實模擬環境中訓練。以 DeepScalper 為第一個接入的 agent，同時修復其 12 個已識別弱點。

**核心價值**：訓練環境 = 生產環境。RL agent 在訓練時就體驗真實的撮合、手續費、滑價、風控，消除 sim-to-real gap。

**領域**：Algorithmic Trading（單一資產，日 K 頻率）。先在 BTC 上驗證，再擴展。

> **EP Review 修正（套件位置 H8）**：`nautilus_gym/` 是獨立於 `nautilus_trader/` 的 Python 套件，透過 pip install -e 安裝，位於 nautilus_trader repo 根目錄的 `nautilus_gym/` 子目錄（gitignore）。不修改 nautilus_trader 本身。需建立 `nautilus_gym/pyproject.toml`，依賴 `nautilus_trader`、`gymnasium>=0.29`、`torch>=2.0`、`numpy`、`pandas`。

> **EP Review 修正（Action Space 統一 C1/L16）**：全專案統一使用 **continuous action space** `Box(0, 1)` 表示目標持倉比例。S2 的 discrete 分支標記為 Phase 2 擴展點，不實作。ActionProtocol 定義為 `Action = np.ndarray  # shape=(1,), dtype=float32, values in [0, 1]`。

---

## UC 盤點

### 掃描範圍
- 無既有 USE-CASES.md（新專案）
- 本次變更建立全新能力，全部為新增 UC

### 新增 UC

| UC ID | 狀態 | 簡述 | 實作路徑 |
|-------|------|------|---------|
| E-01 | 📋 | NT Gym Environment core（step/reset 介面） | `nautilus_gym/env.py` |
| E-02 | 📋 | RL Strategy Bridge（Gym env → NT 訂單） | `nautilus_gym/strategy.py` |
| E-03 | 📋 | Feature Engineering Bridge（NT 資料 → observation） | `nautilus_gym/features.py` |
| E-04 | 📋 | Improved DeepScalper Agent（修復 12 項弱點） | `nautilus_gym/agents/deep_scalper.py` |
| E-05 | 📋 | Walk-Forward Training Pipeline | `nautilus_gym/training.py` |

---

## Scenario Matrix

| # | 場景 | 觸發 | 預期行為 | Checkpoint | 對應 UC |
|---|------|------|---------|------------|---------|
| SM-1 | 完整訓練 happy path | `python train.py --config btc.yaml` | 訓練完成，模型存檔，out-of-sample Sharpe > 0 | 無 | E-04, E-05 |
| SM-2 | 單一步進除錯 | `env.step(action)` 手動呼叫 | 回傳 (obs, reward, done, info)，狀態正確更新 | 無 | E-01 |
| SM-3 | 破產終止 | 現金 + 持倉價值 < 初始 10% | done=True，info 包含破產原因 | 無 | E-01 |
| SM-4 | 訂單被風控拒絕 | 超過 max_notional | 訂單不成交，agent 狀態反映無變化 | 無 | E-02 |
| SM-5 | 滑價發生 | 市價單 + OneTickSlippage | 成交價偏離 1 tick，reward 反映真實成本 | 無 | E-01 |
| SM-6 | 多資產擴展 | `instruments=["BTC","ETH"]` | observation 維度自動擴展，action space 對應調整 | 無 | E-03 |
| SM-7 | Walk-forward 時段切換 | 訓練自動切換 window | 模型在每個 window 獨立訓練，結果可比 | 上一 window 最佳模型 | E-05 |
| SM-8 | 空資料（假日） | BTC 資料中假日無資料 | 環境跳過無資料日，不產生空 step | 無 | E-01 |
| SM-9 | 模型匯出 + NT live 接軌 | 訓練完成 → 匯出 TorchScript | 同一個 Strategy 類在 live 模式載入模型運行 | 最後 checkpoint | E-02, E-04 |

---

## DeepScalper 弱點分析與改進方案

### 已識別的 12 個弱點

| # | 弱點 | 嚴重度 | 改進方案 | NT 功能支援 |
|---|------|--------|---------|------------|
| W1 | Target network 永不更新（tau=0） | 🔴 Critical | tau=0.005 soft update | — |
| W2 | 固定 epsilon（無 decay） | 🟡 High | 線性衰減 1.0→0.05 | — |
| W3 | 無滑價模型 | 🔴 Critical | NT OneTickSlippageFillModel | ✅ |
| W4 | 簡化手續費（flat 0.1%） | 🟡 High | NT MakerTakerFeeModel | ✅ |
| W5 | Reward 包含未來資訊 | 🔴 Critical | 改用真實 Δequity | ✅ |
| W6 | 無風控（停損、最大持倉、MDD） | 🔴 Critical | NT RiskEngine + 自定義 reward shaping | ✅ |
| W7 | State 無正規化（raw price + z-score 混合） | 🟡 High | RunningMeanStd normalization layer | — |
| W8 | 單一資產 | 🟡 Medium | 架構支援多資產（observation 自動擴展） | ✅ |
| W9 | 固定 1 單位下單 | 🟡 Medium | Continuous action space（連續持倉比例） | ✅ |
| W10 | 無破產終止 | 🟡 High | equity < 10% initial → done=True | ✅ |
| W11 | 驗證集選模型用 total return | 🟡 Medium | 改用 Sharpe ratio | — |
| W12 | 無延遲模型 | 🟢 Low | NT LatencyModel（可選開啟） | ✅ |

### 改進前後對照

| 維度 | 原始 DeepScalper | 改進後 |
|------|-----------------|--------|
| State | 82 維，raw + z-score 混合 | 82+ 維，running-normalized |
| Action | Discrete(3) = {sell, hold, buy} | Box(0, 1) = 目標持倉比例 |
| Reward | future-leaking PnL | 真實 Δequity - transaction_cost |
| Execution | 無滑價、flat 0.1% fee | NT realistic fill + maker/taker fee |
| Risk | 無 | NT RiskEngine + MDD termination |
| Target net | 永不更新 | tau=0.005 soft update |
| Epsilon | 固定 0.25 | 線性衰減 1.0→0.05 |
| Model selection | Total return | Sharpe ratio |

---

## 段落劃分原則

- 垂直切片：每段完成後可獨立驗證
- S1 → S2 → S3 可平行開發（S1 是主線，S2/S3 是獨立元件）
- S4 依賴 S1+S2+S3
- S5 依賴 S4

```
S1: NT Gym Environment Core
 ├─ S2: RL Strategy Bridge ─────┐
 └─ S3: Feature Engineering ────┼──→ S4: Improved DeepScalper ──→ S5: Training Pipeline
```

---

## Segment 1: NT Gym Environment Core

### Context

**目標**：建構 `NTEngine(gymnasium.Env)` —— 核心的 Gym 包裝器，將 NT 的 BacktestEngine 暴露為標準 Gym 介面。

**UC 引用**：實作 E-01

**依賴關係**：無外部段落依賴。依賴 nautilus_trader 套件。

**語義約束**：
- 與 S2 共享：action → order 的轉換介面（`ActionProtocol`）
- 與 S3 共享：observation 的維度和正規化方法（`ObservationSpec`）
- 與 S4 共享：reward 計算公式（`RewardFn` protocol）

**基礎設施盤點**：
- `BacktestEngine` → 定義 `nautilus_trader/backtest/engine.pyx`
- `BacktestEngine.run(streaming=True)` → 單批次執行，資料耗盡後返回
- `BacktestEngine.add_data()` → 注入資料點
- `BacktestEngine.reset()` → 重置所有引擎狀態
- `PortfolioFacade` → 定義 `nautilus_trader/portfolio/base.pyx:24`，提供 equity/balances/PnL
- `CacheFacade` → 定義 `nautilus_trader/cache/base.pyx`，提供 positions/orders 查詢
- `TestClock` → 定義 `nautilus_trader/core/time.pyx`，backtest 靜態時鐘
- `FillModel` → 定義 `nautilus_trader/backtest/models/fill.pyx`，10+ 填充模型
- `MakerTakerFeeModel` → 定義 `nautilus_trader/backtest/models/fee.pyx`

**依賴錨點**：
- `BacktestEngine` → 定義 `nautilus_trader/backtest/engine.pyx:1586`（主迴圈）/ 消費 `nautilus_gym/env.py`（Gym wrapper 呼叫）
- `BacktestEngine.run(streaming=True)` → 定義 `engine.pyx:1311`（docstring） / 消費 `nautilus_gym/env.py:NTEngine.step()`
- `PortfolioFacade.equity()` → 定義 `portfolio/base.pyx:24` / 消費 `nautilus_gym/env.py:NTEngine._get_observation()`

**技術選型**：
- Gymnasium（gym 的後繼，API 更穩定）
- 使用 NT 的 streaming mode 實現 step-by-step 執行
- 使用 NT 的 portfolio/cache API 提取狀態

**成功標準**：
- `env.reset()` 正確初始化 NT BacktestEngine
- `env.step(action)` 推進一個 bar，回傳正確的 (obs, reward, done, info)
- 連續 1000 步不 crash，記憶體不洩漏

> **EP Validate 驗證**：POC 1 ✅ + POC 2 ✅ — streaming mode (add_data→run(streaming=True)→clear_data) 循環完全可行；CurrencyPair + MARGIN 帳戶正確設置；equity() 回傳 dict[Currency, Money]，.as_double() 正確取得 float；Strategy 子類繞過 frozen config 可行；訂單在 streaming 中正確撮合，equity 含手續費和未實現損益。**POC 4 ✅** — Strategy bridge 完整流程驗證：set_action → add_data → run(streaming=True) → on_bar 執行訂單 → fill 回調。⚠️ **Engine 重用修正（V6）**：`reset()` 不能建新 BacktestEngine（Rust logger singleton 限制），必須在 `__init__` 建一次並重用。見 pseudo code 後的 V6 修正。

### 核心實作要點

1. **Streaming Mode Step-by-Step**：每次 `step()` 注入一個 bar 資料點到 BacktestEngine，呼叫 `run(streaming=True)`，然後 `clear_data()`
2. **State Extraction**：從 `portfolio.equity()`、`cache.positions_open()`、`cache.account_for_venue()` 提取狀態
3. **Reward from Real Equity Change**：`reward = equity[t] - equity[t-1]`，不使用未來資訊
4. **Termination Conditions**：資料耗盡 / 破產（equity < 10% initial）/ 達到 max_steps
5. **Configurable Simulation**：FillModel、FeeModel、LatencyModel 可透過 config 切換

### Pseudo Code

```
nautilus_gym/
├── __init__.py
├── env.py                    # NTEngine(gymnasium.Env) — 核心 Gym wrapper
├── config.py                 # NTEngineConfig dataclass
├── reward.py                 # RewardFn protocol + 具體實作
├── types.py                  # ActionProtocol, ObservationSpec
├── strategy.py               # S2
├── features.py               # S3
├── agents/                   # S4
└── training.py               # S5
```

```python
class NTEngineConfig:
    venue: Venue = Venue("SIM")
    oms_type: OmsType = OmsType.NETTING
    account_type: AccountType = AccountType.MARGIN  # EP Review 修正 F1：CASH + base_currency 無法持有 CurrencyPair
    base_currency: Currency | None = None  # EP Review 修正 F1：MARGIN 帳戶不需單一 base_currency
    starting_balance: float = 1_000_000
    instruments: list[Instrument]  # 必須由使用者提供
    data: list[Bar | QuoteTick | TradeTick]  # 排序後的歷史資料
    fill_model: FillModel = OneTickSlippageFillModel()
    fee_model: FeeModel = MakerTakerFeeModel()
    latency_model: LatencyModel | None = None
    reward_fn: RewardFn = EquityChangeReward()
    bankruptcy_threshold: float = 0.1  # equity < 10% initial → done
    max_steps: int | None = None
```

```python
class NTEngine(gymnasium.Env):
    metadata = {"render_modes": ["human", "log"]}

    def __init__(self, config: NTEngineConfig):
        self.config = config
        self.action_space = spaces.Box(0.0, 1.0, shape=(1,), dtype=np.float32)  # EP Review 修正 C1：統一 continuous
        self.observation_space = ... # 由 ObservationSpec.dim 決定

        self._data_index = 0
        self._initial_equity = config.starting_balance
        self._prev_equity = config.starting_balance
        self._strategy: RLStrategyBridge | None = None
        self._engine: BacktestEngine | None = None

    def reset(self, seed=None, options=None):
        """建立全新的 BacktestEngine 實例（非 engine.reset()）。
        EP Review 修正 F6：engine.reset() 保留 data/instruments，
        用 new instance 確保完全乾淨狀態。"""
        super().reset(seed=seed)

        self._data_index = 0
        self._prev_equity = self._initial_equity

        self._engine = BacktestEngine(config=BacktestEngineConfig())
        self._engine.add_venue(
            venue=self.config.venue,
            oms_type=self.config.oms_type,
            account_type=self.config.account_type,
            starting_balances=[Money(self.config.starting_balance, USD)],
            fill_model=self.config.fill_model,
        )
        for inst in self.config.instruments:
            self._engine.add_instrument(inst)

        self._strategy = RLStrategyBridge(
            config=RLStrategyConfig(action_space=self.action_space),
            action_callback=self._on_strategy_ready,
        )
        self._engine.add_strategy(self._strategy)

        obs = self._get_observation()
        info = self._get_info()
        return obs, info

    def step(self, action):
        """注入一個 bar，讓 NT 處理，回傳結果。"""
        if self._data_index >= len(self.config.data):
            raise RuntimeError("Episode ended. Call reset().")

        current_equity = self._get_equity()

        self._strategy.set_action(action)

        data_point = self.config.data[self._data_index]
        self._engine.add_data([data_point], validate=False)
        self._engine.run(streaming=True)
        self._engine.clear_data()

        self._data_index += 1

        new_equity = self._get_equity()
        reward = self.config.reward_fn(current_equity, new_equity, self._get_trades_info())

        obs = self._get_observation()
        done = self._check_done()
        truncated = False
        info = self._get_info()

        self._prev_equity = new_equity
        return obs, reward, done, truncated, info

    def _get_equity(self) -> float:
        # EP Review 修正 F4/C2：用 portfolio.equity() 取得含未實現損益的權益
        equity_dict = self._engine.portfolio.equity(venue=self.config.venue)
        currency = list(equity_dict.keys())[0]
        return float(equity_dict[currency].as_double())

    def _get_observation(self) -> np.ndarray:
        raise NotImplementedError("由 S3（Feature Engineering）實作")

    def _check_done(self) -> bool:
        equity = self._get_equity()
        bankrupt = equity < self._initial_equity * self.config.bankruptcy_threshold
        data_exhausted = self._data_index >= len(self.config.data)
        max_steps_reached = (
            self.config.max_steps is not None
            and self._data_index >= self.config.max_steps
        )
        # EP Review 修正 H6：加入 max_steps 終止條件
        return bankrupt or data_exhausted or max_steps_reached

    def _get_info(self) -> dict:
        return {
            "equity": self._get_equity(),
            "positions": [str(p) for p in self._engine.cache.positions_open()],
            "step": self._data_index,
        }

    def _on_strategy_ready(self, strategy):
        self._strategy = strategy

    def close(self):
        if self._engine:
            self._engine.end()
            self._engine = None
```

> **EP Validate 修正 V6（S1 Engine 生命週期）**：`reset()` 不能建立新 BacktestEngine。POC 4 (`lab/poc_gym_step_loop.py`) 驗證：
> - ✅ Strategy bridge + 單 bar streaming + action 注入完整流程正確（4 orders / 4 fills）
> - ✅ 5 個 episode 重用同一個 engine，equity 正確追蹤不同資料
> - ✅ 多個 BacktestEngine 可同時共存
> - ❌ `engine.dispose()` 清除 Rust logger singleton → 之後無法建新 engine（`thread panicked at crates/common/src/ffi/logging.rs:146`）
> - **修正架構**：`__init__` 建一次 BacktestEngine（含 venue / instruments / strategy bridge），`reset()` 只重置 `_data_index`、`_prev_equity`、strategy 內部狀態（clear fills 等），`close()` 才呼叫 `end()` + `dispose()`。
> - ** `_get_equity()` fallback**：`portfolio.equity(venue)` 在第一個 bar 處理前回傳空 dict，需 fallback 到 `account.balance_total(currency)`。

```python
class EquityChangeReward:
    """真實權益變動 reward，無未來資訊洩漏。"""
    def __call__(self, prev_equity, new_equity, trades_info) -> float:
        return new_equity - prev_equity


# EP Review 修正 H5：實作 W6 risk-aware reward shaping
class RiskAwareReward:
    """權益變動 + drawdown 懲罰 + 交易成本懲罰。"""
    def __init__(self, drawdown_penalty: float = 2.0, transaction_penalty: float = 0.001):
        self.drawdown_penalty = drawdown_penalty
        self.transaction_penalty = transaction_penalty
        self._peak_equity = 0.0

    def reset(self, initial_equity: float):
        self._peak_equity = initial_equity

    def __call__(self, prev_equity, new_equity, trades_info) -> float:
        self._peak_equity = max(self._peak_equity, new_equity)
        drawdown = (self._peak_equity - new_equity) / max(self._peak_equity, 1.0)
        equity_change = new_equity - prev_equity
        n_trades = trades_info.get("num_trades", 0)
        return equity_change - self.drawdown_penalty * drawdown - self.transaction_penalty * n_trades
```

### 驗證策略

**Example 設計**：
- `examples/minimal_gym_env.py`：建立 env → reset → step 10 次 → close
- `examples/gym_random_agent.py`：random action 跑完整 episode，驗證不 crash

**測試計畫**：
- 單元測試：reset 正確初始化所有狀態、step 推進 data_index、done 條件正確觸發
- 整合測試：完整 episode 從 reset 到 done，equity 變化合理
- 邊界案例：空資料、單一 bar、破產場景
- 已知未覆蓋：多 venue、多幣種（Phase 2 範圍）

---

## Segment 2: RL Strategy Bridge

### Context

**目標**：建構 `RLStrategyBridge(Strategy)` —— NT Strategy 子類，作為 Gym env 和 NT 訂單系統之間的橋樑。Gym env 透過此 bridge 注入 action，bridge 轉換為 NT 訂單。

**UC 引用**：實作 E-02

**依賴關係**：依賴 S1（NTEngine 在 reset 時建立此 strategy）

**語義約束**：
- 與 S1 共享：action → order 的轉換介面（`Action = np.ndarray`，shape=(1,), values in [0,1]）
- 與 S4 共享：action space 定義（continuous only）

**基礎設施盤點**：
- `Strategy` → 定義 `nautilus_trader/trading/strategy.pyx`，核心基類
- `Strategy.submit_order()` → 定義 `strategy.pyx:805`，訂單提交入口
- `OrderFactory.market()` → 定義 `nautilus_trader/common/factories.pyx`，市價單工廠
- `Strategy.on_bar()` → 定義 `common/actor.pyx:575`，bar 回調（繼承自 Actor）
- `Strategy.on_order_filled()` → 定義 `strategy.pyx`，成交回調

**依賴錨點**：
- `Strategy.submit_order()` → 定義 `trading/strategy.pyx:805` / 消費 `nautilus_gym/strategy.py:RLStrategyBridge.execute_action()`
- `OrderFactory.market()` → 定義 `common/factories.pyx` / 消費 `nautilus_gym/strategy.py:RLStrategyBridge._action_to_orders()`

**技術選型**：直接繼承 NT 的 Strategy 類

> **EP Review 修正 C4**：NT 的 `StrategyConfig` 是 frozen msgspec Struct，不接受 `gymnasium.spaces.Space` 等非 msgspec 型別。改用一般 Python dataclass 作為 `RLStrategyConfig`，在 `__init__` 中手動呼叫 `Strategy.__init__()` 而非透過 config 系統。

**成功標準**：
- action 注入後能正確產生 NT 訂單
- 訂單在 BacktestEngine 中正確撮合
- on_order_filled 回調正確觸發

> **EP Validate 驗證**：POC 2 ✅ — Strategy 子類用自訂 __init__(StrategyConfig(order_id_tag=...)) 繞過 frozen config 成功；subscribe_bars(BarType) 在 streaming 中正確觸發 on_bar；submit_order 在 streaming 中撮合成功；on_order_filled 回調正確觸發；equity 變化反映真實成本（手續費 + 未實現損益）。另發現 Quantity 建構子不接受 instrument_id（已修正 V2）

1. **Action Injection**：Gym env 的 `step()` 呼叫 `strategy.set_action(action)`，strategy 在 `on_bar()` 中讀取並執行
2. **Action → Order 轉換**：支援兩種模式
   - Discrete mode：action = {sell, hold, buy}，轉換為固定數量的市價單
   - Continuous mode：action = target_weight (0~1)，計算 delta → 產生對應的買/賣單
3. **Trade Logging**：記錄所有成交，供 reward 計算和 info 使用

### Pseudo Code

```
nautilus_gym/strategy.py
```

```python
# EP Review 修正 C4：不繼承 StrategyConfig（frozen msgspec），用一般 dataclass
@dataclass
class RLStrategyConfig:
    bar_type: BarType        # EP Review 修正 F3：明確傳入要訂閱的 BarType
    instrument_id: InstrumentId
    order_id_tag: str = "RL"

class RLStrategyBridge(Strategy):
    # EP Review 修正 C4：繞過 msgspec config，用 custom __init__

    def __init__(self, config: RLStrategyConfig):
        strategy_config = StrategyConfig(order_id_tag=config.order_id_tag)
        super().__init__(config=strategy_config)
        self._rl_config = config
        self._pending_action = None
        self._action_consumed = True
        self._fills: list[OrderFilled] = []

    def set_action(self, action):
        self._pending_action = action
        self._action_consumed = False

    def on_start(self):
        # EP Review 修正 F3：用 config 中明確的 bar_type
        self.subscribe_bars(self._rl_config.bar_type)

    def on_bar(self, bar: Bar):
        if self._action_consumed or self._pending_action is None:
            return

        self.execute_action(self._pending_action, bar)
        self._action_consumed = True

    def execute_action(self, action, bar: Bar):
        orders = self._action_to_orders(action, bar)
        for order in orders:
            self.submit_order(order)

    def _action_to_orders(self, action, bar) -> list[Order]:
        # EP Review 修正 L16：移除 discrete 分支，只保留 continuous
        instrument_id = bar.bar_type.instrument_id
        instrument = self.cache.instrument(instrument_id)
        return self._continuous_action_to_orders(action, instrument, bar)

    def _continuous_action_to_orders(self, action, instrument, bar) -> list[Order]:
        target_weight = float(np.clip(action, 0.0, 1.0))
        current_equity = self._get_equity()
        target_value = current_equity * target_weight

        account = self.cache.account_for_venue(instrument.id.venue)
        current_position_value = self._get_position_value(instrument.id)

        delta_value = target_value - current_position_value
        current_price = float(bar.close)

        if abs(delta_value) < current_price * 0.01:
            return []

        quantity_abs = abs(delta_value) / current_price
        quantity = Quantity(quantity_abs, precision=instrument.size_precision)  # EP Validate 修正 V2：Quantity 只接受 (value, precision)，不接受 instrument_id

        if delta_value > 0:
            return [self.order_factory.market(instrument.id, OrderSide.BUY, quantity)]
        else:
            return [self.order_factory.market(instrument.id, OrderSide.SELL, quantity)]

    def on_order_filled(self, event: OrderFilled):
        self._fills.append(event)

    def get_fills_since(self, since_index: int) -> list[OrderFilled]:
        return self._fills[since_index:]

    def on_reset(self):
        self._pending_action = None
        self._action_consumed = True
        self._fills.clear()

    def _get_equity(self) -> float:
        ...
    def _get_position_value(self, instrument_id) -> float:
        ...
```

### 驗證策略

**Example 設計**：
- `examples/strategy_discrete.py`：離散 action 測試
- `examples/strategy_continuous.py`：連續 action（target weight）測試

**測試計畫**：
- 單元測試：action → order 轉換正確（buy/sell/hold 三種）
- 單元測試：continuous mode 的 delta 計算正確
- 整合測試：order 在 BacktestEngine 中成交，fill 回調觸發
- 邊界案例：餘額不足買入、空持倉賣出

---

## Segment 3: Feature Engineering Bridge

### Context

**目標**：建構觀察建構層，解決 DeepScalper 的 state scaling 問題。提供統一的特徵計算介面，確保訓練和推論使用完全相同的 observation。

**UC 引用**：實作 E-03

**依賴關係**：依賴 S1（NTEngine 呼叫 `_get_observation()`）

**語義約束**：
- 與 S1 共享：observation 的維度（`ObservationSpec`）
- 與 S4 共享：特徵列表和正規化方法

**基礎設施盤點**：
- NT `Bar` 型別 → 包含 open/high/low/close/volume
- NT `cache.positions_open()` → 持倉資訊
- NT `cache.account_for_venue()` → 帳戶餘額
- TradeMaster 的特徵列表（16 指標）→ 參考用，不直接依賴

**依賴錨點**：
- `Bar` → 定義 `nautilus_trader/model/data/bar.pyx` / 消費 `nautilus_gym/features.py:FeatureEngine.extract()`
- `CacheFacade.positions_open()` → 定義 `cache/base.pyx` / 消費 `nautilus_gym/features.py:PortfolioFeatures.extract()`

**技術選型**：
- 使用 running mean/std 正規化（線上計算，不需預先統計）
- 支援自定義特徵列表（向下相容 DeepScalper 的 16 指標）

**成功標準**：
- 觀察值維度正確（82+ 維）
- 正規化後所有特徵在 [-3, 3] 範圍內
- 同一筆資料兩次呼叫結果一致

### 核心實作要點

1. **MarketFeatures**：從 NT Bar 歷史計算技術指標（收盤價相關、報酬率相關）
2. **PortfolioFeatures**：從 NT cache 提取持倉和現金狀態
3. **RunningNormalization**：線上更新 mean/std，避免 lookahead bias
4. **LookbackWindow**：維護滑動窗口，提供 N 日回顧

### Pseudo Code

```
nautilus_gym/features.py
```

```python
class ObservationSpec:
    market_features: list[str]
    lookback_window: int
    include_portfolio: bool
    normalize: bool

    @property
    def dim(self) -> int:
        portfolio_dim = 2 if self.include_portfolio else 0
        return len(self.market_features) * self.lookback_window + portfolio_dim


class RunningMeanStd:
    """線上 Welford 統計，用於觀察正規化。"""
    def __init__(self, shape: tuple):
        self.mean = np.zeros(shape)
        self.var = np.ones(shape)
        self.count = 0

    def update(self, x: np.ndarray):
        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self.var += delta * delta2

    def normalize(self, x: np.ndarray) -> np.ndarray:
        if self.count < 2:
            return x
        std = np.sqrt(self.var / max(self.count, 1))
        return (x - self.mean) / (std + 1e-8)


class FeatureEngine:
    DEFAULT_FEATURES = [
        "zopen", "zhigh", "zlow", "zclose",
        "return_1d", "return_5d", "return_10d", "return_20d",
        "volatility_5d", "volatility_20d",
        "volume_ratio",
    ]

    def __init__(self, spec: ObservationSpec):
        self.spec = spec
        self._bar_history: deque[Bar] = deque(maxlen=spec.lookback_window + 30)
        self._normalizer = RunningMeanStd(shape=(spec.dim,)) if spec.normalize else None

    def update(self, bar: Bar):
        self._bar_history.append(bar)

    def extract(self, portfolio_state: dict) -> np.ndarray:
        market = self._extract_market_features()
        if self.spec.include_portfolio:
            portfolio = self._extract_portfolio_features(portfolio_state)
            obs = np.concatenate([market, portfolio])
        else:
            obs = market

        if self._normalizer:
            if self._normalizer.count > 100:
                obs = self._normalizer.normalize(obs)
            self._normalizer.update(obs)

        return obs.astype(np.float32)

    def _extract_market_features(self) -> np.ndarray:
        if len(self._bar_history) < self.spec.lookback_window:
            return np.zeros(len(self.spec.market_features) * self.spec.lookback_window)

        features = []
        bars = list(self._bar_history)[-self.spec.lookback_window:]
        closes = np.array([float(b.close) for b in bars])

        for bar in bars:
            close = float(bar.close)
            open_ = float(bar.open)
            high = float(bar.high)
            low = float(bar.low)
            volume = float(bar.volume)

            bar_features = {
                "zopen": (open_ - close) / close,
                "zhigh": (high - close) / close,
                "zlow": (low - close) / close,
                "zclose": 0.0,
                "return_1d": 0.0,
                "return_5d": 0.0,
                "return_10d": 0.0,
                "return_20d": 0.0,
                "volatility_5d": 0.0,
                "volatility_20d": 0.0,
                "volume_ratio": 1.0,
            }
            features.extend([bar_features[f] for f in self.spec.market_features])

        return np.array(features)

    def _extract_portfolio_features(self, state: dict) -> np.ndarray:
        equity = state["equity"]
        position_value = state["position_value"]
        cash = state["cash"]
        return np.array([
            cash / max(equity, 1.0),
            position_value / max(equity, 1.0),
        ])
```

### 驗證策略

**Example 設計**：
- `examples/feature_extraction.py`：載入 BTC 資料，extract 觀察，印出統計

**測試計畫**：
- 單元測試：RunningMeanStd 收斂到正確值
- 單元測試：market features 正確計算（對照手算值）
- 單元測試：portfolio features 正確歸一化
- 邊界案例：不足 lookback window 時回傳零向量
- 已知未覆蓋：高頻特徵（tick-level）、LOB 特徵

---

## Segment 4: Improved DeepScalper Agent

### Context

**目標**：重寫 DeepScalper agent，修復全部 12 個弱點。使用 PyTorch（不依賴 TradeMaster 的 mmcv/mmengine），可直接在 NT Gym 環境中訓練。

**UC 引用**：實作 E-04

**依賴關係**：依賴 S1（NTEngine）、S2（action 介面）、S3（observation 介面）

**語義約束**：
- 與 S1 共享：reward 計算（使用 EquityChangeReward，不使用 future info）
- 與 S2 共共享：action space 定義（continuous Box(0,1)）
- 與 S3 共享：observation 維度和正規化

**基礎設施盤點**：
- TradeMaster DQN agent → 參考 `trademaster/agents/algorithmic_trading/dqn.py`（參考，不直接依賴）
- PyTorch → 主要依賴
- NTEngine → 來自 S1，訓練環境

**依賴錨點**：
- `NTEngine` → 定義 `nautilus_gym/env.py` / 消費 `nautilus_gym/agents/deep_scalper.py:DeepScalperAgent.train()`
- `ObservationSpec` → 定義 `nautilus_gym/features.py` / 消費 `nautilus_gym/agents/deep_scalper.py:DeepScalperAgent.__init__()`

**技術選型**：
- PyTorch（不使用 TradeMaster 的 registry/config）
- Continuous action space → 使用 DDPG/TD3（更適合連續控制）或 SAC
- 選擇 SAC：sample efficiency 好、自動 entropy tuning、不需要 target policy smoothing

**成功標準**：
- 在 NT Gym 環境中完整訓練 20 epochs
- Out-of-sample Sharpe > 0（BTC 日 K）
- 訓練過程 reward 曲線上升

### 核心實作要點

1. **SAC Agent**：替代 DQN，適合連續 action space
2. **Target Network Soft Update**：tau=0.005（修復 W1）
3. **Epsilon/Gaussian Noise Decay**：σ 從 0.5 線性衰減到 0.05（修復 W2）
4. **Risk-Aware Reward Shaping**：基礎 reward = Δequity，附加 drawdown penalty（修復 W6）
5. **Running Normalization**：observation 在 agent 端再次正規化（修復 W7）
6. **Continuous Action**：target_weight ∈ [0, 1]（修復 W9）
7. **Sharpe-based Model Selection**（修復 W11）
8. **Bankruptcy Termination**：由 NTEngine 處理（修復 W10）

### Pseudo Code

```
nautilus_gym/agents/
├── __init__.py
├── deep_scalper.py           # 改進版 DeepScalper（SAC-based）
├── networks.py               # Actor/Critic networks
└── replay_buffer.py          # Prioritized replay buffer
```

```python
class DeepScalperConfig:
    observation_dim: int
    action_dim: int = 1
    hidden_dims: list[int] = [128, 64]
    lr_actor: float = 3e-4
    lr_critic: float = 3e-4
    gamma: float = 0.99
    tau: float = 0.005
    alpha: float = 0.2
    buffer_size: int = 1_000_000
    batch_size: int = 256
    warmup_steps: int = 1000
    noise_sigma_start: float = 0.5
    noise_sigma_end: float = 0.05
    noise_decay_steps: int = 50_000


class DeepScalperAgent:
    def __init__(self, config: DeepScalperConfig):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.actor = SACActorNetwork(config).to(self.device)
        self.critic1 = SACCriticNetwork(config).to(self.device)
        self.critic2 = SACCriticNetwork(config).to(self.device)
        self.critic1_target = copy.deepcopy(self.critic1)
        self.critic2_target = copy.deepcopy(self.critic2)

        self.actor_optimizer = Adam(self.actor.parameters(), lr=config.lr_actor)
        self.critic_optimizer = Adam(
            list(self.critic1.parameters()) + list(self.critic2.parameters()),
            lr=config.lr_critic,
        )

        self.log_alpha = torch.zeros(1, requires_grad=True, device=self.device)
        self.alpha_optimizer = Adam([self.log_alpha], lr=config.lr_actor)
        self.target_entropy = -config.action_dim

        self.buffer = PrioritizedReplayBuffer(config.buffer_size, config.observation_dim, config.action_dim)
        self._total_steps = 0

    def select_action(self, obs: np.ndarray, deterministic: bool = False) -> np.ndarray:
        state = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
        with torch.no_grad():
            if deterministic:
                action = self.actor.mean_action(state)
            else:
                action, _ = self.actor.sample_action(state)
                sigma = self._current_noise_sigma()
                action = action + sigma * torch.randn_like(action)
                action = torch.clamp(action, 0.0, 1.0)
        return action.cpu().numpy()[0]

    def store_transition(self, obs, action, reward, next_obs, done):
        self.buffer.add(obs, action, reward, next_obs, done)
        self._total_steps += 1

    def update(self) -> dict:
        if len(self.buffer) < self.config.batch_size:
            return {}

        batch = self.buffer.sample(self.config.batch_size)
        obs, action, reward, next_obs, done = [x.to(self.device) for x in batch]

        with torch.no_grad():
            next_action, next_log_prob = self.actor.sample_action(next_obs)
            next_q1 = self.critic1_target(next_obs, next_action)
            next_q2 = self.critic2_target(next_obs, next_action)
            next_q = torch.min(next_q1, next_q2) - self.alpha * next_log_prob
            target_q = reward + (1 - done) * self.config.gamma * next_q

        critic1_loss = F.mse_loss(self.critic1(obs, action), target_q)
        critic2_loss = F.mse_loss(self.critic2(obs, action), target_q)
        critic_loss = critic1_loss + critic2_loss

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        torch.nn.utils.clip_grad_norm_(
            list(self.critic1.parameters()) + list(self.critic2.parameters()), 1.0
        )
        self.critic_optimizer.step()

        new_action, log_prob = self.actor.sample_action(obs)
        q1 = self.critic1(obs, new_action)
        q2 = self.critic2(obs, new_action)
        actor_loss = (self.alpha * log_prob - torch.min(q1, q2)).mean()

        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        alpha_loss = -(self.log_alpha * (log_prob + self.target_entropy).detach()).mean()
        self.alpha_optimizer.zero_grad()
        alpha_loss.backward()
        self.alpha_optimizer.step()
        self.alpha = self.log_alpha.exp()

        self._soft_update_targets()

        return {
            "critic_loss": critic_loss.item(),
            "actor_loss": actor_loss.item(),
            "alpha": self.alpha.item(),
        }

    def _soft_update_targets(self):
        tau = self.config.tau
        for target, source in [
            (self.critic1_target, self.critic1),
            (self.critic2_target, self.critic2),
        ]:
            for t, s in zip(target.parameters(), source.parameters()):
                t.data.copy_(tau * s.data + (1 - tau) * t.data)

    def _current_noise_sigma(self) -> float:
        if self._total_steps >= self.config.noise_decay_steps:
            return self.config.noise_sigma_end
        progress = self._total_steps / self.config.noise_decay_steps
        return self.config.noise_sigma_start + progress * (
            self.config.noise_sigma_end - self.config.noise_sigma_start
        )

    def save(self, path: str):
        torch.save({
            "actor": self.actor.state_dict(),
            "critic1": self.critic1.state_dict(),
            "critic2": self.critic2.state_dict(),
            "log_alpha": self.log_alpha.item(),
            "total_steps": self._total_steps,
        }, path)

    def load(self, path: str):
        checkpoint = torch.load(path, map_location=self.device)
        self.actor.load_state_dict(checkpoint["actor"])
        self.critic1.load_state_dict(checkpoint["critic1"])
        self.critic2.load_state_dict(checkpoint["critic2"])
        self.log_alpha.data.fill_(checkpoint["log_alpha"])
        self._total_steps = checkpoint["total_steps"]
```

> **EP Review 修正 H7**：`nautilus_gym/agents/networks.py` 包含 `SACActorNetwork`、`SACCriticNetwork`、`build_mlp()` helper（上面 pseudo code 中 inline 定義的類別，實作時抽出至此檔案）。`nautilus_gym/agents/replay_buffer.py` 包含 `PrioritizedReplayBuffer`（標準 PER 實作，使用 `torch.Tensor` 儲存 state/action/reward/next_state/done，優先級取樣用 sum-tree 結構）。

> **EP Review 修正 M11**：`nautilus_gym/types.py` 定義共享介面：
> - `Action = np.ndarray  # shape=(1,), dtype=float32, values in [0, 1]`
> - `ObservationSpec`（由 S3 實作，提供 `dim` 屬性和 `features` 列表）
> - `RewardFn = Callable[[float, float, dict], float]  # (prev_equity, new_equity, trades_info) -> reward`

```python
class SACActorNetwork(nn.Module):
    def __init__(self, config: DeepScalperConfig):
        super().__init__()
        self.net = build_mlp([config.observation_dim, *config.hidden_dims])
        self.mean_head = nn.Linear(config.hidden_dims[-1], config.action_dim)
        self.log_std_head = nn.Linear(config.hidden_dims[-1], config.action_dim)

    def forward(self, obs):
        x = self.net(obs)
        mean = torch.sigmoid(self.mean_head(x))
        log_std = torch.clamp(self.log_std_head(x), -20, 2)
        return mean, log_std

    def sample_action(self, obs):
        mean, log_std = self.forward(obs)
        std = log_std.exp()
        normal = torch.distributions.Normal(mean, std)
        x_t = normal.rsample()
        action = torch.clamp(x_t, 0.0, 1.0)
        log_prob = normal.log_prob(x_t).sum(dim=-1)
        return action, log_prob

    def mean_action(self, obs):
        mean, _ = self.forward(obs)
        return torch.clamp(mean, 0.0, 1.0)


class SACCriticNetwork(nn.Module):
    def __init__(self, config: DeepScalperConfig):
        super().__init__()
        self.net = build_mlp([config.observation_dim + config.action_dim, *config.hidden_dims, 1])

    def forward(self, obs, action):
        return self.net(torch.cat([obs, action], dim=-1))
```

### 驗證策略

**Example 設計**：
- `examples/train_btc.py`：在 BTC 日 K 上完整訓練

**測試計畫**：
- 單元測試：SAC actor 輸出在 [0, 1] 範圍內
- 單元測試：soft update 正確修改 target 參數（tau=0.005 時，參數移動 0.5%）
- 單元測試：noise sigma 隨步數正確衰減
- 單元測試：replay buffer add/sample 正確
- 整合測試：agent + NTEngine 互動 100 步，reward 合理
- 已知未覆蓋：多 GPU 訓練、分散式訓練

---

## Segment 5: Training Pipeline + Walk-Forward Validation

### Context

**目標**：建立完整的訓練管線，包含 walk-forward validation 和模型選擇。

**UC 引用**：實作 E-05

**依賴關係**：依賴 S4（完整 agent）

**語義約束**：
- 與 S4 共享：模型儲存/載入格式
- 與 S1 共享：NTEngineConfig 的資料分割方式

**基礎設施盤點**：
- NTEngine → 來自 S1
- DeepScalperAgent → 來自 S4
- TradeMaster 的 BTC 資料 → `TradeMaster/data/algorithmic_trading/BTC/`（CSV 格式，需轉換為 NT Bar）

**依賴錨點**：
- `NTEngine` → 定義 `nautilus_gym/env.py` / 消費 `nautilus_gym/training.py:WalkForwardTrainer._create_env()`
- `DeepScalperAgent` → 定義 `nautilus_gym/agents/deep_scalper.py` / 消費 `nautilus_gym/training.py:WalkForwardTrainer.train_window()`

**技術選型**：
- Walk-forward：滾動窗口，每個 window 獨立訓練
- 模型選擇：Sharpe ratio（非 total return）
- 資料轉換：BTC CSV → NT Bar 物件

**成功標準**：
- Walk-forward 3 個 window 完成
- Out-of-sample Sharpe > 0
- 訓練曲線合理（reward 上升 → 收斂）

> **EP Validate 驗證**：POC 1 ✅ — BTCDataLoader 的 CurrencyPair 建構子參數名已修正（V1: id→instrument_id）；Bar 建構和 add_data 在 streaming 中正確運作；Import 路徑修正（V3: AggregationSource/PriceType/BarAggregation 來自 nautilus_trader.model.enums）

### 核心實作要點

1. **資料載入器**：BTC CSV → NT Bar 物件列表（按 ts_init 排序）
2. **Walk-Forward 分割**：train_ratio=0.6, val_ratio=0.2, test_ratio=0.2，滾動步進
3. **訓練迴圈**：epoch → explore (N steps) → update (M batches) → validate → 選最佳
4. **模型選擇**：validation Sharpe ratio 最高者
5. **結果彙整**：所有 window 的 out-of-sample 績效比較

### Pseudo Code

```
nautilus_gym/training.py
nautilus_gym/data_loader.py
```

```python
class WalkForwardConfig:
    data_path: str
    instrument_id: str
    train_ratio: float = 0.6
    val_ratio: float = 0.2
    test_ratio: float = 0.2
    num_windows: int = 3
    epochs_per_window: int = 20
    steps_per_epoch: int = 2000
    eval_steps: int = 500
    save_dir: str = "checkpoints/"


class BTCDataLoader:
    # EP Review 修正 L17：提供 BTC instrument 建構範例
    @staticmethod
    def make_btc_instrument(instrument_id: str = "BTC-USD.SIM") -> CurrencyPair:
        return CurrencyPair(
            instrument_id=InstrumentId.from_str(instrument_id),  # EP Validate 修正 V1：參數名是 instrument_id 不是 id
            raw_symbol=Symbol("BTCUSD"),
            base_currency=BTC,
            quote_currency=USD,
            price_precision=2,
            size_precision=6,
            price_increment=Price.from_str("0.01"),
            size_increment=Quantity.from_str("0.000001"),
            lot_size=None,
            max_quantity=Quantity.from_str("1000000"),
            min_quantity=Quantity.from_str("0.000001"),
            max_notional=None,
            min_notional=None,
            margin_init=Decimal("0.5"),
            margin_maint=Decimal("0.25"),
            maker_fee=Decimal("0.001"),
            taker_fee=Decimal("0.002"),
            ts_event=0,
            ts_init=0,
        )

    def load_bars(self, csv_path: str, instrument_id: str = "BTC-USD.SIM") -> list[Bar]:
        df = pd.read_csv(csv_path)
        inst_id = InstrumentId.from_str(instrument_id)
        # EP Review 修正 F2：必須指定 AggregationSource.EXTERNAL
        bar_type = BarType(
            inst_id,
            BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
            AggregationSource.EXTERNAL,
        )
        bars = []
        for _, row in df.iterrows():
            # EP Review 修正 F5：實作日期 → Unix nanoseconds 轉換
            ts = int(pd.Timestamp(row["date"], tz="UTC").value)
            bar = Bar(
                bar_type=bar_type,
                open=Price.from_str(str(row["open"])),
                high=Price.from_str(str(row["high"])),
                low=Price.from_str(str(row["low"])),
                close=Price.from_str(str(row["close"])),
                volume=Quantity.from_str(str(int(row.get("volume", 0)))),
                ts_event=ts,
                ts_init=ts,
            )
            bars.append(bar)
        return bars


class WalkForwardTrainer:
    def __init__(self, config: WalkForwardConfig):
        self.config = config
        self.loader = BTCDataLoader()

    def run(self):
        all_bars = self.loader.load_bars(self.config.data_path, self.config.instrument_id)
        window_size = len(all_bars) // self.config.num_windows
        results = []

        for window_idx in range(self.config.num_windows):
            start = window_idx * window_size
            end = min(start + window_size, len(all_bars))
            window_bars = all_bars[start:end]

            n = len(window_bars)
            train_end = int(n * self.config.train_ratio)
            val_end = int(n * (self.config.train_ratio + self.config.val_ratio))

            train_bars = window_bars[:train_end]
            val_bars = window_bars[train_end:val_end]
            test_bars = window_bars[val_end:]

            result = self.train_window(
                window_idx, train_bars, val_bars, test_bars
            )
            results.append(result)
            print(f"Window {window_idx}: test Sharpe = {result['test_sharpe']:.2f}")

        self._summarize(results)
        return results

    def train_window(self, window_idx, train_bars, val_bars, test_bars):
        train_env = self._create_env(train_bars)
        val_env = self._create_env(val_bars)
        test_env = self._create_env(test_bars)

        obs_dim = train_env.observation_space.shape[0]
        agent = DeepScalperAgent(DeepScalperConfig(observation_dim=obs_dim))

        best_val_sharpe = -np.inf
        best_checkpoint = None

        for epoch in range(self.config.epochs_per_window):
            train_metrics = self._train_epoch(agent, train_env)
            val_metrics = self._evaluate(agent, val_env)

            if val_metrics["sharpe"] > best_val_sharpe:
                best_val_sharpe = val_metrics["sharpe"]
                path = f"{self.config.save_dir}/window{window_idx}_best.pt"
                agent.save(path)
                best_checkpoint = path

            print(f"  Epoch {epoch}: train_reward={train_metrics['mean_reward']:.4f}, "
                  f"val_sharpe={val_metrics['sharpe']:.2f}")

        agent.load(best_checkpoint)
        test_metrics = self._evaluate(agent, test_env)

        return {
            "window": window_idx,
            "best_val_sharpe": best_val_sharpe,
            "test_sharpe": test_metrics["sharpe"],
            "test_return": test_metrics["total_return"],
            "test_max_drawdown": test_metrics["max_drawdown"],
            "checkpoint": best_checkpoint,
        }

    def _train_epoch(self, agent, env):
        obs, _ = env.reset()
        total_reward = 0
        steps = 0

        for _ in range(self.config.steps_per_epoch):
            action = agent.select_action(obs)
            next_obs, reward, done, truncated, info = env.step(action)
            agent.store_transition(obs, action, reward, next_obs, done)
            agent.update()
            total_reward += reward
            steps += 1
            obs = next_obs

            if done or truncated:
                obs, _ = env.reset()

        return {"mean_reward": total_reward / max(steps, 1)}

    def _evaluate(self, agent, env):
        obs, _ = env.reset()
        equity_curve = []  # EP Review 修正 L15：從 info dict 取 equity，不呼叫私有方法
        done = False

        while not done:
            action = agent.select_action(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            equity_curve.append(info["equity"])
            if truncated:
                break

        returns = np.diff(equity_curve) / equity_curve[:-1]
        sharpe = np.mean(returns) / (np.std(returns) + 1e-8) * np.sqrt(252)
        peak = np.maximum.accumulate(equity_curve)
        drawdown = (peak - equity_curve) / peak
        total_return = (equity_curve[-1] - equity_curve[0]) / equity_curve[0]

        return {
            "sharpe": sharpe,
            "total_return": total_return,
            "max_drawdown": np.max(drawdown),
            "equity_curve": equity_curve,
        }

    def _create_env(self, bars) -> NTEngine:
        ...

    def _summarize(self, results):
        ...
```

### 驗證策略

**Example 設計**：
- `examples/walkforward_btc.py`：完整 walk-forward 訓練 + 結果輸出

**測試計畫**：
- 單元測試：BTC CSV → Bar 轉換正確（對照原始資料）
- 單元測試：walk-forward 分割邊界正確（無 overlap、無 gap）
- 單元測試：Sharpe 計算對照已知值
- 整合測試：1 個 window × 2 epochs 的端到端訓練（smoke test）
- 已知未覆蓋：GPU 訓練、大規模資料（>10 年日 K）

---

## 收尾步驟

### 1. USE-CASES.md 更新
- 建立新的 `nautilus_gym/USE-CASES.md`
- 所有 UC（E-01 ~ E-05）狀態從 📋 更新為 ✅
- 從 Scenario Matrix 提煉「消費場景」欄位

### 2. CLAUDE.md 更新
- 建立 `nautilus_gym/CLAUDE.md`，包含：
  - 架構總覽（NT Gym Wrapper + Agent 層）
  - Module Navigation Map
  - 與 NT 的依賴關係
  - 與 TradeMaster 的關係（獨立但相容）

### 3. /audit-test
- 對所有新增測試執行品質稽核
- 確認無反模式（no mock abuse、no flaky assertions）
- 覆蓋對稱性檢查

---

## 整合策略

### 段落間整合順序

```
S1 獨立驗證 → S2 整合到 S1 → S3 整合到 S1 → S4 整合 S1+S2+S3 → S5 整合全部
```

每個整合點的驗證：

| 整合點 | 驗證方式 |
|--------|---------|
| S1 + S2 | 手動 step(action) → 觀察 NT 訂單成交 |
| S1 + S3 | 手動 step → 觀察 observation 維度和值域正確 |
| S1 + S2 + S3 + S4 | Random agent 跑完整 episode |
| 全部（S5）| Walk-forward 訓練 + out-of-sample Sharpe > 0 |

### Sim-to-Real 驗證

S5 完成後的最終驗證：
1. 訓練好的 agent 匯出 TorchScript
2. NT Strategy（live 模式）載入同一個模型
3. 同一組歷史資料，比較 Gym 環境推論 vs NT Strategy 推論的 action 是否一致
4. 確認 **zero sim-to-real gap**

> **EP Review 修正預留**：EP Review 回饋將以 `> **EP Review 修正**：[修正內容]` 格式嵌入各段落。
