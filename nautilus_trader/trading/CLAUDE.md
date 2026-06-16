# 交易模組

策略 API 和交易員編排。使用者繼承 `Strategy` 來實作交易邏輯；`Trader` 在執行時連接策略、引擎和基礎設施。

## 語言邊界

| 檔案 | 語言 | 為何 |
|------|----------|-----|
| `strategy.pyx` / `strategy.pxd` | Cython | 效能關鍵的事件分派迴圈：`handle_event` 對每個事件執行 `isinstance` 鏈，涵蓋約 18 種訂單事件類型 + 3 種持倉事件類型。交易命令（提交/修改/取消）也需要速度。 |
| `strategy.pyi` | Python 存根 | 內聯類型存根用於 pyright。自給自足 -- 使用 `Any` 表示跨模組類型，`strategy.pyi` 中禁止 `import` Cython 模組。 |
| `config.py` / `trader.py` / `controller.py` / `filters.py` / `messages.py` | Python | 沒有熱路徑 -- 編排、配置反序列化、命令分派、新聞過濾。 |

## 關鍵設計決策

### 兩階段初始化 → `strategy.pyx:register()`

`Strategy.__init__` 不會將策略連接到平台。`register()`（由 `Trader.add_strategy()` 呼叫）連接 `MessageBus`、`Cache`、`Portfolio`、`Clock`，並建立 `OrderFactory` + `OrderManager`。在註冊前呼叫交易指令會引發條件錯誤。這是故意的：配置驅動的工廠建立必須與執行時期的連接分開。

### 雙回調事件分派 → `strategy.pyx:handle_event()`

每個事件都分派到一個類型特定的處理器（例如 `on_order_filled`）和一個通用處理器（`on_order_event` 或 `on_position_event`）。類型特定的處理器首先觸發。

### 三向訂單路由 → `strategy.pyx:submit_order()`

1. **模擬器** -- `order.emulation_trigger != NO_TRIGGER`（模擬停止/限價訂單）
2. **執行演算法** -- `order.exec_algorithm_id is not None`（`TWAP`、`ICEBERG` 等）
3. **風險引擎** -- 預設路徑（透過風險檢查直接執行）

路由決策在 `Strategy` 內部做出，而不是由中央路由器。這在 `cancel_order` 和 `modify_order` 中被映射。

### 市場退出：迭代式優雅關閉 → `strategy.pyx:market_exit()`

取消所有訂單，關閉所有持倉，以可配置的間隔輪詢，直到所有進行中的訂單解決且持倉關閉。有最大嘗試次數保護。在退出期間，新的非減少訂單會被拒絕（`_is_exiting` 旗標）。當 `manage_stop=True` 時，`stop()` 首先觸發市場退出，然後在退出完成後最終停止。

### 每組件時鐘 → `trader.py`

交易員為每個 `Actor`、`Strategy` 和 `ExecAlgorithm` 建立一個單獨的 `Clock`。在回測中，所有時鐘在啟動組件之前同步。防止組件之間的時鐘干擾。

### 交易員繼承 → `trader.py:Trader`

交易員直接繼承 `Component`（不是 `Actor`），因為它管理一個組件艦隊，而不是作為一個組件。

## 模組關係

- **依賴**：`common/`（`Actor`、`Component`、`MessageBus`、`Clock`、`Logger`）、`model/`（訂單、事件、識別符、物件）、`execution/`（`OrderManager`、執行訊息）、`cache/`（`CacheFacade`）、`portfolio/`（`PortfolioFacade`）
- **被...消費**：`backtest/node.py`、`live/node.py`（`TradingNode` 建構和配置 `Trader`）、使用者程式碼（子類別 `Strategy`）
- **兄弟模組**：`common/actor.pyx` 是 `Strategy` 的直接父類別；`Actor` 提供所有資料訂閱/請求方法

## 修改慣例

**`strategy.pyx`**：使用 `cdef` 表示內部方法，`cpdef` 表示可從 `Cython` + `Python` 呼叫的方法。事件處理器是 `cpdef void` -- 它們絕不能阻塞，例外在 `handle_event` 層級被捕獲。`PendingUpdate`/`PendingCancel` 事件由 `Strategy` 樂觀生成，在指令到達引擎之前 -- 這是為了狀態一致性而設計的。前置條件檢查使用 `Condition`（不是 `Python` 斷言）-- 引發 `ValueError` 並帶有描述性訊息。

**`trader.py`**：在 `__init__` 內部導入 `ExecutionEngine` 以避免循環導入（執行引擎導入策略類型）。`order_id_tag` 的唯一性在 `Trader` 中的所有策略中強制執行。將組件添加到正在執行的 `Trader` 會被阻擋，除非 `has_controller=True`。

**`config.py`**：`StrategyConfig` 是一個凍結的 `msgspec` 模型；所有欄位都有預設值。`ImportableStrategyConfig` 儲存完全限定的類別路徑，用於 `TradingNode` 配置驅動的設定。