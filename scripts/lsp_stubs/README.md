# LSP Stub 生成工作流(`scripts/lsp_stubs/`)

為 NT Cython 模組(`.pyx`)生成自給自足的 `.pyi`,讓 pyright/LSP 能解析。

## 為什麼需要

NT 核心模組(cache/engine/actor/portfolio)是 `.pyx`,編譯成 `.so` 後對 pyright/LSP **完全失明**(`workspaceSymbol`/`findReferences` 命中不了)。`.pyi` stub 補位讓 LSP 恢復視力——這是「探索 NT 能力時被迫 rg 源碼 → 從資料結構反推能力邊界 → 過度結論」的技術根因解藥。

## 三件工具

| 工具 | 職責 |
|------|------|
| `patch_stubgen_pyx.py` | 修 stubgen-pyx 的 readonly 缺口(預設只抓 `cdef public`,NT 慣例是 `cdef readonly`)。idempotent,`uv sync` 後重跑 |
| `make_self_contained.py` | 後處理 stubgen-pyx 輸出:跨 Cython 模組型別 → `Any`(自給自足)、`cpython.X` → stdlib、None 預設參數加 `\| None` |
| `generate_nt_stubs.py` | 一鍵 orchestrator:patch + stubgen-pyx + 後處理 + 放定位(全 subprocess,不 import 同目錄工具) |

## 何時跑

- NT 版本升級 / rebase upstream 後(重生成所有已覆蓋 stub)
- 某 Cython 模組大改後(重生成該模組)

## 加新模組

```bash
uv run python scripts/lsp_stubs/generate_nt_stubs.py nautilus_trader/<module>/<file>.pyx
uv run pyright nautilus_trader/<module>/<file>.pyi   # 應 0 errors
```

並在消費端 `mosaic_alpha_trading_lab/scripts/sync_nt_stubs.sh` 的 `NT_MODULES[]` 加該 `.pyi`(否則不 sync 到 venv,LSP 拿不到)。

## 已覆蓋模組

- **手寫**(11,維持不動):`model/{data,objects,identifiers}`、`core/correctness`、`trading/strategy`、`persistence/wranglers`、`indicators/{averages,momentum,trend,volatility,volume}`
- **自動生成**(~90,pyright 0 errors):所有其餘 `.pyx` 模組 — cache/actor/engine/portfolio + accounting + model/* + data/execution/common + core/config/risk/persistence/serialization/system/backtest/indicators 其餘
- **gap**:`core/rust/{common,model}.pyx`(stubgen-pyx 對 `cimport` Rust enum 失敗;mosaic 僅用 `LogColor` via sj,PriceType 等已 Any 化 via cache)

## 設計決策

- **stubgen-pyx 讀 `.pyx` 而非 `.so`**:mypy `stubgen` 對 `.so` 只能 runtime introspect,型別全流失;stubgen-pyx 讀 Cython AST,保留完整型別/簽名/屬性/docstring
- **local patch 而非 fork**:雙向門、self-contained。readonly 是一行修復;upstream stubgen-pyx 未收,`uv sync` 會蓋掉故需 patch script。fork/PR upstream 是長期可選
- **自給自足(stub 禁 import 其他 Cython 模組)**:pyright 無法解析 `.pyx` 依賴鏈;跨模組型別用 `Any`,同模組 `.pxd` 定義的 enum 則直接在 stub 定義
- **readonly patch 為何必要**:NT 用 `cdef readonly` 暴露屬性給 Python 讀(`indicator.value`、`cache.has_backing`),未 patch 的 stubgen-pyx 漏掉這些 → 下游讀屬性全報 attr-defined
- **orchestrator 全 subprocess**:`generate_nt_stubs.py` 不 import 同目錄工具(避免 `sys.path.insert` 觸發 pyright `reportMissingImports`),改用 subprocess 呼叫各 CLI,職責清晰、pyright 零警告
