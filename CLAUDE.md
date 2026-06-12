# NautilusTrader — mosaic_alpha 開發指南

Production-grade algorithmic trading platform。mosaic_alpha 以 Python API 層為主要互動介面，透過自訂 Shioaji adapter 進行台股交易。

## 架構：mosaic_alpha 互動層級

| 層級 | 語言 | mosaic_alpha 使用方式 |
|------|------|---------------------|
| **User API** | Python | Strategy 撰寫、BacktestEngine/TradingNode 配置、Model types、Indicators |
| **Bindings** | Cython | 不直接操作；`core/rust/*.pxd` 為自動產生，禁止手動編輯 |
| **Engine** | Rust | 不直接操作；指標計算和效能關鍵路徑在此執行 |

## 建置與開發

### 前置需求

Rust toolchain (stable), Python 3.12-3.14, `uv` package manager

### 常用指令

| 指令 | 用途 |
|------|------|
| `make build-debug` | Debug 模式建置（開發推薦） |
| `make build` | Release 模式建置 |
| `make pytest` | 跑 Python 測試 |
| `make check-code` | clippy (Rust) + ruff (Python) |
| `make format` | 格式化 Rust + Python |

### 建置環境變數

| 變數 | 預設值 | 用途 |
|------|--------|------|
| `BUILD_MODE` | `release` | `release` / `debug` / `debug-pyo3` |
| `HIGH_PRECISION` | `true` | 128-bit fixed-point（false = 64-bit，編譯時決定） |
| `PYO3_ONLY` | empty | Skip Cython extensions（PyO3-only 工作時加速建置） |

### LSP 支援（pyright + rust-analyzer）

**啟用狀態**: pyright-lsp enabled · rust-analyzer-lsp enabled

**Inline stub 方案**：NT 有 `py.typed` marker，pyright 優先從原始碼目錄讀型別（`stubPath` 被忽略）。`.pyi` 直接放在 `nautilus_trader/` 中對應 `.pyx` 旁邊。Upstream 從未建立這些 `.pyi`，rebase 零衝突。

**Stub 自給自足約束**：禁止 import 其他 Cython 模組（整條依賴鏈都是 .pyx，pyright 無法解析）。用 `Any` 標注跨模組型別。例外：已有 inline .pyi 的同 package 模組可以互相 import（如 strategy.pyi 可 import model.data 的 Bar）。

**已覆蓋模組**：model/objects, model/data, model/identifiers, trading/strategy, core/correctness, persistence/wranglers

| 指令 | 用途 |
|------|------|
| `make verify-stubs` | 驗證 completeness baseline |
| `make verify-stubs-diff` | 只檢查 rebase 後受影響的模組 |
| `make update-stubs-baseline` | 更新 baseline（修改 stub 後） |

**Rebase upstream 後**：`make build-debug` → `make verify-stubs-diff`。如有 REGRESSION：更新 `nautilus_trader/` 中的 `.pyi` → `make update-stubs-baseline`。

## 學習資源

| 資源 | 路徑 | 用途 |
|------|------|------|
| 概念指南 | `docs/concepts/` | 所有 API 的行為契約和正確用法（33 docs） |
| 開發者指南 | `docs/developer_guide/` | 編碼標準、測試、FFI、設計原則 |
| 教程 | `docs/tutorials/` | 入門教學 |
| 範例 | `examples/` | Backtest demos、per-adapter live examples、utility scripts |
| Adapter 範本 | `nautilus_trader/adapters/_template/` | Skeleton for new adapters |

## 模組導覽

以下僅列出 mosaic_alpha 實際使用或有參考價值的模組：

### 核心交易

| 模組 | 用途 | CLAUDE.md |
|------|------|-----------|
| `nautilus_trader/trading/` | Strategy base class、Trader orchestrator | [CLAUDE.md](nautilus_trader/trading/CLAUDE.md) |
| `nautilus_trader/model/` | Price/Quantity/Money (fixed-point)、identifiers、instruments、orders、events | [CLAUDE.md](nautilus_trader/model/CLAUDE.md) |
| `nautilus_trader/backtest/` | BacktestEngine、SimulatedExchange、FeeModel/FillModel | [CLAUDE.md](nautilus_trader/backtest/CLAUDE.md) |
| `nautilus_trader/execution/` | ExecutionEngine、command routing、order FSM、exec algorithms | [CLAUDE.md](nautilus_trader/execution/CLAUDE.md) |
| `nautilus_trader/risk/` | Pre-trade risk engine：order validation、position sizing | [CLAUDE.md](nautilus_trader/risk/CLAUDE.md) |
| `nautilus_trader/portfolio/` | Portfolio state：position tracking、account balances、margin | [CLAUDE.md](nautilus_trader/portfolio/CLAUDE.md) |
| `nautilus_trader/live/` | TradingNode、live engines、adapter wiring、reconciliation | [CLAUDE.md](nautilus_trader/live/CLAUDE.md) |
| `nautilus_trader/accounting/` | CashAccount、MarginAccount、BettingAccount | [CLAUDE.md](nautilus_trader/accounting/CLAUDE.md) |

### 基礎設施

| 模組 | 用途 | CLAUDE.md |
|------|------|-----------|
| `nautilus_trader/common/` | Component FSM、Actor、MessageBus、Clock、Logger、OrderFactory | [CLAUDE.md](nautilus_trader/common/CLAUDE.md) |
| `nautilus_trader/cache/` | In-memory state cache、Redis database adapter | [CLAUDE.md](nautilus_trader/cache/CLAUDE.md) |
| `nautilus_trader/data/` | Data engine：aggregation、bar building、subscriptions | [CLAUDE.md](nautilus_trader/data/CLAUDE.md) |
| `nautilus_trader/config/` | Frozen msgspec dataclass configs | [CLAUDE.md](nautilus_trader/config/CLAUDE.md) |
| `nautilus_trader/system/` | Kernel assembly、config defaults、database wiring | [CLAUDE.md](nautilus_trader/system/CLAUDE.md) |

### 資料與分析

| 模組 | 用途 | CLAUDE.md |
|------|------|-----------|
| `nautilus_trader/indicators/` | Technical indicators：average、momentum、volatility | [CLAUDE.md](nautilus_trader/indicators/CLAUDE.md) |
| `nautilus_trader/persistence/` | ParquetDataCatalog、loaders、wranglers | [CLAUDE.md](nautilus_trader/persistence/CLAUDE.md) |
| `nautilus_trader/analysis/` | PortfolioAnalyzer、tearsheet visualization | [CLAUDE.md](nautilus_trader/analysis/CLAUDE.md) |

### Adapter 參考

| 參考對象 | 用途 |
|---------|------|
| `nautilus_trader/adapters/interactive_brokers/` | Shioaji adapter 的設計範本（最完整的 pure-Python adapter） |
| `nautilus_trader/adapters/sandbox/` | Paper trading 用（mosaic_alpha 直接使用） |
| `nautilus_trader/adapters/_template/` | Adapter skeleton |

## 核心模式

### Strategy Pattern — 外層/內層架構

mosaic_alpha 使用雙層 strategy 架構：
- **外層 DailySignalDispatcher** → `strategies/daily_dispatcher.py:DailySignalDispatcher` — 訂閱 bar stream 偵測換日，持有預計算 watchlist，交付 TargetOrder 給內層
- **內層 KCMomentumNaive** → `strategies/kc_momentum_naive.py:KCMomentumNaive` — 接收 targets，執行日內 momentum 進出場

繼承鏈：`Component`（lifecycle FSM）→ `Actor`（data subscriptions）→ `Strategy`（order management）。註冊是兩階段的：constructor 建立配置，`Trader.add_strategy()` 連接至平台。

**Event handlers（mosaic_alpha 使用的）**：
- `on_start()` — 訂閱 bars、quote ticks、warmup from Parquet
- `on_bar()` — 進出場邏輯
- `on_quote_tick()` — 即時風控（bid/ask spread、trailing stop）
- `on_position_closed()` — 記錄交易、取消訂閱 quote ticks
- `on_stop()` — 清理 quote tick 訂閱

### 自訂 Adapter Pattern（Shioaji 範本）

每個 adapter 遵循一致結構，參考 `adapters/interactive_brokers/`：
- `config.py` — frozen dataclass configs → `InteractiveBrokersDataClientConfig`
- `factories.py` — cached client factories → `InteractiveBrokersLiveDataClientFactory`
- `data.py` — market data client（extends `LiveMarketDataClient`）
- `execution.py` — execution client（extends `LiveExecutionClient`）
- `providers.py` — instrument loading → `InteractiveBrokersInstrumentProvider`
- `client/` — 低層 API wrapper
- `parsing/` — format converters（instruments、execution、data、price_conversion）

Factories 使用模組級 dict 快取連線（`GATEWAYS`、`IB_CLIENTS`、`IB_INSTRUMENT_PROVIDERS`），相同連線參數的 data/exec client 共用底層連線。

### Backtest/Live 程式碼路徑共用

`BacktestDataClient` 和 `BacktestExecClient` 繼承與 live client 相同的基礎類別。Strategy 和 execution engine 不區分 backtest vs live — 這是 NautilusTrader 的核心價值。

mosaic_alpha 的 4-mode matrix：

| | Paper | Live |
|--|-------|------|
| **Direct** | SJ data + Sandbox exec | SJ data + SJ exec |
| **Redis** | External streams + Sandbox exec | External streams + SJ exec |

### Fixed-Point 精度

`Price`、`Quantity`、`Money` 以 raw integers 儲存（非 float）。`HIGH_PRECISION` flag 控制 128-bit 或 64-bit。所有算術直接操作 raw integers。

**台股注意**：股票價格精度（小數位數）因標的而異，construct 時必須指定正確 precision。使用 `Price.from_str("1.5000")` 建構最安全，避免 float 中間值。TWD 非內建貨幣，需 `register_currency()` 註冊。

### Composite Bar Types

mosaic_alpha 使用 1-min 基礎 bars，透過 NT DataEngine 自動聚合。BarType 格式：`{symbol}.{venue}-{agg}-{type}-{price_type}-{step}-{base_step}`。

支援的聚合方式：
- 標準：1-MINUTE、5-MINUTE 等
- 複合：5-MINUTE@1-MINUTE（1-min 基礎自動聚合成 5-min，mosaic_alpha 主要使用此模式）
- Volume/Tick basis

DataEngine 配置 `time_bars_interval_type="right-open"` 確保 bar 時間區間一致（mosaic_alpha 在 `venues/tw/backtest.py` 設定）。

### Indicator 系統 — 雙軌架構

mosaic_alpha 有兩條指標計算路徑：

1. **NT streaming indicators**：繼承 `nautilus_trader.indicators.base.Indicator`，透過 `register_indicator_for_bars(bar_type, indicator)` 連接 bar 訂閱，bar 到達時自動更新。適合 Strategy 內的即時運算。
2. **Polars batch computation**：高效能批次計算，用於 feature engineering 和離線分析。

NT 內建指標（mosaic_alpha 使用的）：EMA、SMA、WMA、DEMA、HMA、Wilder MA、AMA、VIDYA、MACD、RSI、ATR、Bollinger、Donchian、Keltner、VWAP、Pressure、Linear Regression、CMO、Archer MA Trends。

指標在 `crates/nautilus-indicators/` 以 Rust 實作，透過 Cython 或 PyO3 綁定暴露至 Python。

### Actor 模式

`Actor` 是 Strategy 的輕量替代（無 order management），適合：
- 跨組件信號橋接 → `SignalBridgeActor`
- 定期狀態快照 → `StateSnapshotActor`
- 外部 stream 處理

繼承鏈：`Component` → `Actor`。註冊方式：`TradingNode.add_actor()` 或 `TradingNodeBuilder` config。

### Configuration 系統

`nautilus_trader/config/` 中的 frozen msgspec-based dataclasses。每個組件都有對應的 config class。`Importable*Config` variants 存 fully-qualified class paths，支援 config-driven instantiation。

mosaic_alpha 常用 configs：
- `BacktestEngineConfig` — logging、cache、risk bypass（`RiskEngineConfig(bypass=True)`）、data engine 設定
- `TradingNodeConfig` — live/paper 交易節點，包含 data/exec client factories
- `CacheConfig` — 記憶體快取（`database=DatabaseConfig(type="redis")` 支援跨 process 共享）
- `MessageBusConfig` — external streams 設定（`external_streams=["mosaic"]`）

## 機構級量化交易功能路線圖

### ✅ 已使用

| 功能 | NT 模組 | mosaic_alpha 使用方式 |
|------|---------|---------------------|
| Strategy framework | `trading/` | 外層/內層雙層架構（DailySignalDispatcher + KCMomentumNaive） |
| BacktestEngine | `backtest/` | 台股回測，含自訂 `TaiwanStockFeeModel` 和 `TaiwanFuturesFeeModel` |
| TradingNode (live) | `live/` | 4-mode matrix：paper/live × direct/redis |
| Custom adapter | `adapters/` | Shioaji adapter（data + execution），參考 IB adapter pattern |
| Sandbox adapter | `adapters/sandbox/` | Paper trading 模擬成交 |
| Model types | `model/` | Price、Quantity、Money、Bar、QuoteTick、InstrumentId |
| Indicators | `indicators/` | 透過 Indicator bridge 使用 NT streaming indicators |
| Parquet catalog | `persistence/` | `ParquetDataCatalog` + `BarDataWrangler` 歷史資料存取 |
| Cache API | `cache/` | Redis-backed cache 跨 process 共享狀態 |
| Analysis | `analysis/` | PortfolioAnalyzer stats、`create_tearsheet_from_stats()` |
| Actor framework | `common/` | SignalBridgeActor、StateSnapshotActor |
| Config system | `config/` | BacktestEngineConfig、TradingNodeConfig、CacheConfig |

### 📋 建議增強（邁向機構級）

| 功能 | NT 模組 | 增強方向 | 為什麼重要 |
|------|---------|---------|-----------|
| **Risk Engine** | `risk/` | 停用 bypass，啟用 pre-trade risk checks（position limits、exposure limits、order rate limits） | 機構級必須防止超額下單；目前所有風控在 strategy 層，單點故障風險高 |
| **Execution Algorithms** | `execution/` | 使用 `ExecAlgorithm` 實作 TWAP/VWAP | 機構級下單需要最小化市場衝擊，避免一次大單造成不利價格 |
| **Order Types** | `model/orders/` | 加入 LimitOrder（降低衝擊）、StopOrder（自動停損）、OrderList（bracket orders） | MarketOnly 在流動性不足時滑點大；StopOrder 可自動化停損不需 quote tick polling |
| **Reconciliation** | `live/` | 強化 startup reconciliation、加入定期 reconciliation | 確保 NT 內部狀態與實際 broker 狀態一致，防止 ghost positions |
| **Slippage Models** | `backtest/` | 自訂 SlippageModel（market impact model） | 預設 FillModel 太理想化，回測結果高估實際績效 |
| **Latency Models** | `backtest/` | 自訂 LatencyModel | 模擬下單延遲對日內策略的影響 |
| **Portfolio Management** | `portfolio/` | 使用 NT Portfolio API 做跨 strategy position tracking | 目前 position tracking 只在 strategy 內部 dict，跨 strategy 無法協調 |
| **Order Emulator** | `execution/` | 用 NT 內建 OrderEmulator 模擬 stop/limit 觸發 | 減少實際掛單量，broker 端看不到未觸發的 stop orders |

### 🔍 未來可考慮

| 功能 | NT 模組 | 說明 |
|------|---------|------|
| **Event Sourcing** | `crates/event_store/` | 完整事件審計軌跡（合規需求）。NT 內建 redb backend，支援 crash recovery 和 snapshot/replay |
| **Margin Accounting** | `accounting/` | 期貨保證金管理（MarginAccount），跨貨幣 margin 計算 |
| **Multi-venue Support** | `adapters/` | 同時連接多個 broker（如 SJ + IB），分散流動性風險 |
| **Advanced Serialization** | `serialization/` | Arrow 格式高效序列化，適合大量歷史資料處理 |
| **Data Quality Monitoring** | `data/` | 自動化 bar completeness/timeliness 驗證，偵測資料斷點 |

## 尋找功能：快速參考

| 「在哪裡...」 | 看哪裡 |
|--------------|--------|
| Strategy event handlers | `nautilus_trader/trading/strategy.pyx` |
| Order type 實作 | `nautilus_trader/model/orders/{type}.pyx` |
| Instrument type 實作 | `nautilus_trader/model/instruments/{type}.pyx` |
| BacktestEngine 配置 | `nautilus_trader/backtest/engine.pyx` |
| TradingNode 配置 | `nautilus_trader/live/node.pyx` |
| 最完整的 adapter 範本 | `nautilus_trader/adapters/interactive_brokers/` |
| Adapter skeleton | `nautilus_trader/adapters/_template/` |
| NT indicator base class | `nautilus_trader/indicators/base.pyx` |
| 指標 Rust 實作 | `crates/nautilus-indicators/src/` |
| Parquet catalog API | `nautilus_trader/persistence/catalog.py` |
| BarDataWrangler | `nautilus_trader/persistence/wranglers.py` |
| PortfolioAnalyzer | `nautilus_trader/analysis/` |
| FeeModel / FillModel | `nautilus_trader/backtest/models.pyx` |
| ExecAlgorithm | `nautilus_trader/execution/` |
| RiskEngine 配置 | `nautilus_trader/risk/` |
| Cache API | `nautilus_trader/cache/cache.pyx` |
| MessageBus | `nautilus_trader/common/message_bus.pyx` |
| Actor base class | `nautilus_trader/common/actor.pyx` |
| Config 基礎類別 | `nautilus_trader/config/` |
| Logger | `nautilus_trader/common/component.pyx` |
| PyCondition（validation） | `nautilus_trader/core/correctness.pyx` |
| 建置配置 | `build.py`、`Makefile`、`pyproject.toml` |
| IB adapter live examples | `examples/live/interactive_brokers/` |
| IB adapter historical download | `nautilus_trader/adapters/interactive_brokers/historical/client.py` |
| Sandbox adapter | `nautilus_trader/adapters/sandbox/` |
