# 即時交易執行環境

## 架構概述

`live/` 子包實作了**即時交易執行環境** — `backtest/` 的生產環境對應物。所有即時引擎和客戶端運行在一個共享的 `asyncio` 事件循環（預設使用 `uvloop`）上，使用非同步佇列將傳入的場所訊息與內部處理解耦。

**與回測的主要差異**：回測核心使用 `TestClock` 和同步的順序處理。即時核心使用 `LiveClock`（掛鐘時間）、基於非同步佇列的引擎，並且必須處理斷開連線、重連、對帳和遺失事件。

## 模組邊界

| 邊界 | 描述 |
|----------|-------------|
| `live/` 負責 | 即時特定的引擎實作、客戶端基礎類別、對帳、節點編排器 |
| `live/` 不負責 | 基礎引擎介面（由 `data/`、`execution/`、`risk/` 負責）、具體適配器客戶端（由適配器包如 `adapters/bybit/` 負責）、配置型別定義（由 `config/` 負責） |
| 與 `system/` 的關係 | `NautilusKernel` 建立即時引擎並連接它們；`TradingNode` 包裝核心並新增建構器/客戶端建立階段 |

## 關鍵檔案

| 檔案 | 職責 |
|------|---------------|
| `node.py` | `TradingNode` — 頂層編排器。封裝 `NautilusKernel`，持有 `TradingNodeBuilder`，管理生命週期（建構 -> 運行 -> 停止 -> 銷毀）。CLI 入口點 (`__main__.py`) |
| `node_builder.py` | `TradingNodeBuilder` — 工廠連接。註冊資料/執行客戶端工廠，從配置建構客戶端，將它們註冊到引擎，包含場所路由 |
| `data_engine.py` | `LiveDataEngine` — 基於非同步佇列的資料路由。四個佇列（cmd、req、res、data），透過哨兵值關閉。繼承 `DataEngine` |
| `execution_engine.py` | `LiveExecutionEngine` — 基於非同步佇列的訂單路由與對帳。兩個佇列（cmd、evt）以及持續對帳迴圈。繼承 `ExecutionEngine`。這是包中最大且最複雜的檔案 |
| `risk_engine.py` | `LiveRiskEngine` — 基於非同步佇列的交易前風險檢查。兩個佇列（cmd、evt）。繼承 `RiskEngine` |
| `data_client.py` | `LiveDataClient`、`LiveMarketDataClient` — 即時資料適配器客戶端的基礎類別。提供 `create_task()` 用於安全的非同步協程管理，包含錯誤處理和完成回呼 |
| `execution_client.py` | `LiveExecutionClient` — 即時執行適配器客戶端的基礎類別。相同的任務管理模式，以及對帳報告產生方法 |
| `config.py` | 所有即時特定的配置型別：`LiveDataEngineConfig`、`LiveRiskEngineConfig`、`LiveExecEngineConfig`、`TradingNodeConfig`、`RoutingConfig` |
| `enqueue.py` | `ThrottledEnqueuer[T]` — 通用的佇列入隊器，具有容量感知的節流日誌記錄。由所有三個即時引擎共享 |
| `reconciliation.py` | 用於在對帳期間建立合成訂單事件的純函式。由 `LiveExecutionEngine` 使用 |
| `factories.py` | `LiveDataClientFactory`、`LiveExecClientFactory` — 適配器包必須子類別化的抽象工廠基礎類別 |
| `cancellation.py` | `cancel_tasks_with_timeout()` — 所有即時客戶端使用的安全任務清理工具程式 |
| `retry.py` | 用於重連/重試邏輯的帶抖動的指數退避 |

## 節點連線流程

```
TradingNodeConfig
  -> TradingNode(config)
     -> NautilusKernel(config, loop)
       -> 建立 LiveDataEngine、LiveExecutionEngine、LiveRiskEngine
     -> TradingNodeBuilder(kernel 元件)
  -> node.add_data_client_factory(name, factory)
  -> node.add_exec_client_factory(name, factory)
  -> node.build()
     -> builder.build_data_clients(config.data_clients)
        -> factory.create() -> engine.register_client()
     -> builder.build_exec_clients(config.exec_clients)
        -> factory.create() -> engine.register_client()
  -> node.run()
     -> kernel.start_async()
        -> engines._on_start() -> 建立佇列任務
     -> asyncio.gather(所有佇列任務)
```

**客戶端名稱路由**：配置鍵，例如 `"BINANCE-FUTURES"` 透過 `-` 分割以提取工廠名稱 (`"BINANCE"`)。同一個工廠可以服務多個配置條目。`RoutingConfig` 控制預設和場所特定的路由。

## 引擎佇列架構

所有三個即時引擎共享相同的模式：

1. **入隊** 透過 `ThrottledEnqueuer` — 當佇列有容量時非阻塞，當佇列滿時回退到非同步 `put()`（帶有節流警告日誌）
2. **處理** — 每個佇列一個專用的 `asyncio.Task`，透過 `await queue.get()` 進行無限迴圈排空
3. **關閉** — 透過 `call_soon_threadsafe` 將哨兵值 (`None`) 放置在所有佇列上，任務乾淨地退出。`kill()` 會立即取消任務
4. **異常處理** — 可透過 `graceful_shutdown_on_exception` 進行配置：要麼優雅地關閉，要麼 `os._exit(1)`（僅崩潰模式）

**佇列計數**：`LiveDataEngine` 有 4 個佇列（cmd、req、res、data）。`LiveExecutionEngine` 和 `LiveRiskEngine` 各有 2 個佇列（cmd、evt）。

## 對帳系統

`LiveExecutionEngine` 運行一個**持續對帳迴圈** (`_continuous_reconciliation_loop`)，定期檢查三個維度：

1. **在途訂單檢查** — 超過閾值停留在中間狀態（SUBMITTED、PENDING_UPDATE、PENDING_CANCEL）的訂單會被查詢並最終強制解決
2. **未結訂單一致性** — 將快取的未結訂單與場所訂單狀態報告進行比較，對帳差異
3. **持倉一致性** — 將快取的持倉與場所持倉報告進行比較，查詢缺失的成交，並在 `generate_missing_orders=True` 時產生合成對帳訂單

**啟動對帳**：啟動時，`reconcile_execution_state()` 會執行一次完整的批次狀態對帳（訂單 + 成交 + 持倉），來自所有執行客戶端。持續迴圈會等待此操作完成後再開始定期檢查。

**對帳模式**：支援淨額模式（每個工具一個淨持倉）和淨額模式（每個 venue_position_id 一個持倉）。交叉零持倉對帳分為兩次成交（平倉 + 重新開倉）。

## 客戶端任務管理模式

`LiveDataClient`/`LiveMarketDataClient` 和 `LiveExecutionClient` 都使用相同的模式：

- `create_task(coro, log_msg, actions, success_msg)` — 透過 `_on_task_completed` 回呼封裝 `loop.create_task()` 並進行錯誤處理
- 任務在 `WeakSet[asyncio.Task]` 中追蹤以便清理
- `cancel_pending_tasks(timeout_secs)` — 取消並等待所有已追蹤的任務
- 子類別實作非同步協程（`_connect`、`_disconnect`、`_submit_order` 等），這些協程透過 `create_task` 啟動

## 約定

- **時鐘**：始終是 `LiveClock`（掛鐘時間） — 絕不是 `TestClock`
- **佇列大小**：預設 100,000；可透過配置中的 `qsize` 為每個引擎配置
- **訊號處理**：`TradingNode` 向核心註冊 `_loop_sig_handler`，以在 `SIGINT`/`SIGTERM` 時優雅地關閉
- **外部訊息流**：可選；當配置了 `message_bus.external_streams` 時，一個流任務從 `msgbus` 資料庫讀取並發布給內部訂閱者
- **配置解析**：`TradingNodeConfig.__post_init__` 使用 `msgspec` 自動將原始字典解析為 `ImportableConfig` 或型別化的客戶端配置