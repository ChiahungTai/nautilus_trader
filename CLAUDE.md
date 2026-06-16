# NautilusTrader — mosaic_alpha 開發指南

Production-grade algorithmic trading platform。mosaic_alpha 以 Python API 層為主要互動介面，透過自訂 Shioaji adapter 進行台股交易。

## 架構：語言邊界

| 層級 | 語言 | 說明 |
|------|------|------|
| **User API** | Python | mosaic_alpha 唯一直接操作的層 |
| **Bindings** | Cython | `core/rust/*.pxd` 為自動產生，**禁止手動編輯**；pyright 無法解析，需 `.pyi` 補位 |
| **Engine** | Rust | 核心資料模型、order/event、networking 等效能關鍵路徑；透過 `core/rust/*.pxd`（Cython）或 PyO3 綁定暴露。**指標例外：純 Cython** |

## 建置

`make build-debug`（開發）| `make build`（release）| `make pytest` | `make check-code` | `make format`

**關鍵變數**：`HIGH_PRECISION`（預設 128-bit fixed-point）| `PYO3_ONLY`（skip Cython 加速建置）| `BUILD_MODE`

## LSP 支援（pyright + rust-analyzer）

NT 有 `py.typed` marker，pyright 優先從原始碼目錄讀型別（`stubPath` 被忽略）。`.pyi` 直接放在 `nautilus_trader/` 中對應 `.pyx` 旁邊。

**為什麼這樣設計**：Upstream 從未建立 `.pyi`，rebase 零衝突。比起修改 `pyrightconfig.json`（upstream 可能覆蓋），inline stub 更持久。

**Stub 自給自足約束**：禁止 import 其他 Cython 模組（整條依賴鏈都是 .pyx，pyright 無法解析）。用 `Any` 標注跨模組型別。唯一例外：同 package 內已有 `.pyi` 的模組可互相 import。

**已覆蓋模組**：model/objects, model/data, model/identifiers, trading/strategy, core/correctness, persistence/wranglers, indicators/{averages,momentum,trend,volatility,volume}

**巨檔自動生成（stubgen-pyx 工作流）**：cache/cache、common/actor、backtest/engine、portfolio/portfolio 等大模組手寫不現實，用 `scripts/lsp_stubs/generate_nt_stubs.py`（stubgen-pyx + readonly patch + 自給自足後處理）自動生成 `.pyi`。手寫的 11 模組維持不動。詳見 `scripts/lsp_stubs/README.md`。readonly patch 必要：stubgen-pyx 預設只抓 `cdef public`，NT 慣例 `cdef readonly`（`indicator.value`、`cache.has_backing`）會漏。

**Rebase upstream 後流程**：`make build-debug` → `make verify-stubs-diff` → REGRESSION 時更新 `.pyi` → `make update-stubs-baseline`；巨檔模組重跑 `scripts/lsp_stubs/generate_nt_stubs.py`

## 核心模式

### Strategy Pattern — 外層/內層架構

mosaic_alpha 使用雙層 strategy 架構，這是**為了分離日訊號生成與日內執行**：
- **外層** → `DailySignalDispatcher`（mosaic_alpha: `strategies/daily_dispatcher.py`）— 訂閱 bar stream 偵測換日，持有預計算 watchlist，交付 TargetOrder 給內層
- **內層** → `KCMomentumNaive`（mosaic_alpha: `strategies/kc_momentum_naive.py`）— 接收 targets，執行日內 momentum 進出場

**註冊是兩階段的**：constructor 建立配置，`Trader.add_strategy()` 才連接至平台。忘記第二階段 = strategy 不會收到任何事件。

### Backtest/Live 程式碼路徑共用

Backtest 和 Live client 繼承相同基礎類別。Strategy 和 execution engine **不區分** backtest vs live — 這是 NT 的核心價值，mosaic_alpha 所有策略都是同一份程式碼跑兩種模式。

mosaic_alpha 的 4-mode matrix（組合維度：資料來源 × 執行端）：

| | Paper | Live |
|--|-------|------|
| **Direct** | SJ data + Sandbox exec | SJ data + SJ exec |
| **Redis** | External streams + Sandbox exec | External streams + SJ exec |

### 自訂 Adapter Pattern

參考範本：`adapters/interactive_brokers/`（最完整的 pure-Python adapter）。

**關鍵設計**：Factories 使用模組級 dict 快取連線（`GATEWAYS`、`IB_CLIENTS`、`IB_INSTRUMENT_PROVIDERS`），相同連線參數的 data/exec client **共用底層連線**。這不是 NT 文檔說明的，是從 IB adapter 程式碼觀察到的模式。

### Fixed-Point 精度 — 台股陷阱

`Price`/`Quantity`/`Money` 以 raw integers 儲存（非 float）。**台股注意**：
- 股票價格精度因標的而異，construct 時必須指定正確 precision
- 使用 `Price.from_str("1.5000")` 建構最安全，避免 float 中間值
- TWD 非內建貨幣，需 `register_currency()` 註冊

### Composite Bar Types — DataEngine 自動聚合

mosaic_alpha 使用 1-min 基礎 bars，透過 NT DataEngine 自動聚合。格式：`{symbol}.{venue}-{agg}-{type}-{price_type}-{step}-{base_step}`。

**關鍵約定**：DataEngine 配置 `time_bars_interval_type="right-open"` 確保 bar 時間區間一致（mosaic_alpha 在 backtest 配置中設定，見 `BacktestEngineConfig`）。錯誤的 interval type = bar 邊界偏移 = 回測結果不可信。

### Indicator 系統 — 雙軌架構

兩條指標計算路徑，**用途不同不可混用**：

1. **NT streaming indicators**（`indicators/base.pyx:Indicator`）— `register_indicator_for_bars()` 連接 bar 訂閱，bar 到達時自動更新。適合 Strategy 內的即時運算。
2. **Polars batch computation** — 高效能批次計算，用於 feature engineering 和離線分析。

指標實作為純 Cython（`nautilus_trader/indicators/*.pyx`），runtime 載入編譯後的 `.cpython-*.so`（已驗證 `averages` 載入自 `averages.cpython-312-darwin.so`）。平行的 `crates/indicators/` Rust crate（含 PyO3 bindings）存在但**尚未接上 Python API**（ROADMAP v2.0 migration 進行中）— 所以 stub 對照的是 `.pyx`，不是 Rust crate。

### Actor 模式

`Actor` 是 Strategy 的輕量替代（**無 order management**）。mosaic_alpha 用於：信號橋接（`SignalBridgeActor`，mosaic_alpha: `actors/signal_bridge.py`）、狀態快照（`StateSnapshotActor`，mosaic_alpha: `actors/state_snapshot.py`）。

## 模組導覽

僅列出 mosaic_alpha 實際使用或有參考價值的模組。詳細 CLAUDE.md 見各模組目錄。

### 核心交易

- `trading/` → [CLAUDE.md](nautilus_trader/trading/CLAUDE.md) — Strategy base class、Trader orchestrator
- `model/` → [CLAUDE.md](nautilus_trader/model/CLAUDE.md) — Fixed-point types、identifiers、instruments、orders
- `backtest/` → [CLAUDE.md](nautilus_trader/backtest/CLAUDE.md) — BacktestEngine、FeeModel/FillModel
- `execution/` → [CLAUDE.md](nautilus_trader/execution/CLAUDE.md) — ExecutionEngine、order FSM、exec algorithms
- `risk/` → [CLAUDE.md](nautilus_trader/risk/CLAUDE.md) — Pre-trade risk engine
- `portfolio/` → [CLAUDE.md](nautilus_trader/portfolio/CLAUDE.md) — Position tracking、account balances
- `live/` → [CLAUDE.md](nautilus_trader/live/CLAUDE.md) — TradingNode、adapter wiring、reconciliation
- `accounting/` → [CLAUDE.md](nautilus_trader/accounting/CLAUDE.md) — Cash/Margin/Betting accounts

### 基礎設施

- `common/` → [CLAUDE.md](nautilus_trader/common/CLAUDE.md) — Component FSM、Actor、MessageBus、OrderFactory
- `cache/` → [CLAUDE.md](nautilus_trader/cache/CLAUDE.md) — In-memory cache、Redis adapter
- `data/` → [CLAUDE.md](nautilus_trader/data/CLAUDE.md) — Data engine、bar aggregation、subscriptions
- `config/` → [CLAUDE.md](nautilus_trader/config/CLAUDE.md) — Frozen msgspec dataclass configs
- `system/` → [CLAUDE.md](nautilus_trader/system/CLAUDE.md) — Kernel assembly、database wiring

### 資料與分析

- `indicators/` → [CLAUDE.md](nautilus_trader/indicators/CLAUDE.md) — Technical indicators（純 Cython；Rust crate migration 中）
- `persistence/` → [CLAUDE.md](nautilus_trader/persistence/CLAUDE.md) — ParquetDataCatalog、wranglers
- `analysis/` → [CLAUDE.md](nautilus_trader/analysis/CLAUDE.md) — PortfolioAnalyzer、tearsheet

### Adapter 參考

- `adapters/interactive_brokers/` — Shioaji adapter 的設計範本
- `adapters/sandbox/` — Paper trading 模擬成交（mosaic_alpha 直接使用）
- `adapters/_template/` — Adapter skeleton

## 機構級增強路線圖

目前 mosaic_alpha 的風控全在 strategy 層（`RiskEngineConfig(bypass=True)`），position tracking 只在 strategy 內部 dict。

### 建議增強（按優先級）

| 增強方向 | 為什麼重要 |
|---------|-----------|
| **啟用 Risk Engine** | 防止超額下單；目前風控單點故障在 strategy 層 |
| **ExecAlgorithm（TWAP/VWAP）** | 最小化市場衝擊 |
| **StopOrder + LimitOrder** | 自動化停損不需 quote tick polling；降低滑點 |
| **Startup + 定期 Reconciliation** | 防止 ghost positions（NT 內部狀態 vs broker 狀態不一致） |
| **自訂 SlippageModel** | 預設 FillModel 太理想化，回測高估實際績效 |
| **跨 Strategy Portfolio API** | 目前跨 strategy 無法協調 position |
| **OrderEmulator** | broker 端看不到未觸發的 stop orders |

### 未來可考慮

- **Event Sourcing**（`crates/event_store/`）— redb backend，crash recovery + snapshot/replay
- **Margin Accounting** — 期貨保證金管理
- **Multi-venue Support** — 多 broker 分散流動性風險

## 學習資源

- `docs/concepts/` — API 行為契約（必讀，NT 的行為規範）
- `docs/developer_guide/` — 編碼標準、FFI、設計原則
- `examples/` — Backtest demos、per-adapter live examples
