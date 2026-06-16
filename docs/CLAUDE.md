# docs/ — Documentation Root Navigation

> **權威性**: 概念指南 (`concepts/`) 與 API 參考 (`api_reference/`) 之間的差異，以 API 參考為準。

## 導航：「我需要關於 X 的資訊」

| 我需要... | 前往 |
|---|---|
| 理解核心概念（訂單、策略、資料、事件） | `concepts/` → 請參閱 [concepts/CLAUDE.md](concepts/CLAUDE.md) 以獲取概念→文件的映射 |
| 入門 / 執行首次回測 | `getting_started/` |
| 逐步教學 | `tutorials/` — `index.md` 列出了建議順序；Jupytext `.py` 檔案可作為腳本或筆記本運行 |
| 特定任務食譜（載入外部資料、配置即時交易、Rust actor） | `how_to/` |
| 設置交易所/資料適配器以進行即時交易 | `integrations/` — 每個適配器一個 `.md` 檔案 |
| 程式碼貢獻、編碼標準、測試、FFI | `developer_guide/` |
| Python 類別/函數簽名 | `api_reference/` — 自動生成的 Sphinx |
| Rust 基準測試範本 | `dev_templates/` — 政策請參閱 `/BENCHMARKING.md` |

## 文件到程式碼的交叉引用

| 文件 | 原始碼 |
|---|---|
| `concepts/strategies.md` | `nautilus_trader/trading/strategy.pyx` |
| `concepts/orders.md` | `nautilus_trader/model/orders/` |
| `concepts/execution.md` | `nautilus_trader/execution/engine.pyx` |
| `concepts/backtesting.md` | `nautilus_trader/backtest/engine.pyx` |
| `concepts/data.md` | `nautilus_trader/data/engine.pyx` |
| `concepts/value_types.md` | `nautilus_trader/model/objects.pyx` |
| `concepts/order_book.md` | `nautilus_trader/model/book.pyx` |
| `concepts/cache.md` | `nautilus_trader/cache/` |
| `concepts/events.md` | `nautilus_trader/model/events/` |
| `concepts/configuration.md` | `nautilus_trader/config/` |
| `concepts/adapters.md` | `nautilus_trader/adapters/` |
| `concepts/greeks.md` | `nautilus_trader/model/greeks.pyx` |
| `integrations/<venue>.md` | `nautilus_trader/adapters/<venue>/` |
| `developer_guide/ffi.md` | `nautilus_trader/ffi/` + `crates/` FFI 模組 |
| `developer_guide/testing.md` | `tests/` |
| `tutorials/*.py` | `nautilus_trader/examples/` |

## 慣例

- `concepts/` 和 `tutorials/` 中的程式碼範例是**可運行的**，而非偽程式碼
- 所有文件程式碼範例都使用 Python；Rust 對應版本在 `concepts/rust.md` 和 `developer_guide/rust.md` 中
- 適配器 ID（例如 `BYBIT`、`BINANCE`）直接對應到 `nautilus_trader/adapters/<id_lowercase>/`
- `:::note` 和 `:::warning` 區塊標記行為合約和常見陷阱
- `api_reference/` 是從原始碼自動生成的（實際簽名）；`concepts/` 描述預期行為（合約）
