# nautilus_trader/indicators/

技術指標 — 純粹的 Cython (.pyx/.pxd) 實作。沒有 Rust，沒有純 Python 指標。

## 為什麼全部是 Cython

指標在熱的交易循環中運行 — 每個報價/交易都會呼叫它們。Cython 提供 C 級分發，無需 FFI 邊界穿越。`.pxd` 檔案宣告 C 級類別介面；`.pyx` 檔案包含實作。**兩者必須同步修改** — 更改一個而不更改另一個會導致難以除錯的 C 級不匹配。

## 架構：三條更新路徑

所有指標都繼承自 `base.pyx:Indicator`。基類別定義了三條可選的更新路徑，子類別可以覆寫：

- `handle_quote_tick` — 買賣價指標 (BollingerBands, DonchianChannel, SpreadAnalyzer)
- `handle_trade_tick` — 最新成交價指標 (多數移動平均線, MACD)
- `handle_bar` — K 線指標 (大多數)

每條 `handle_*` 都委託給 `update_raw(...)` — 這是規範的計算路徑。原始簽名因指標而異（單值、H/L/C 等）。**約定**：`handle_*` 解包市場資料物件，然後呼叫 `update_raw`；所有實際計算都發生在 `update_raw` 中。

生命週期：`has_inputs` 在第一次更新時變為 True，`initialized` 在預熱期過後變為 True。在策略邏輯中，使用值之前檢查 `indicator.initialized`。

## 策略整合

透過 `common/actor.pyx` 的 `register_indicator_for_{quote_ticks,trade_ticks,bars}()` 進行註冊。註冊導致 Actor 在呼叫使用者的 `on_*` 回呼之前自動將資料輸入到指標中。具體方法請參見 `nautilus_trader/trading/strategy.pyx`。

## 組合模式

許多指標在內部組合了其他指標。這意味著在重置或初始化檢查時必須傳播到內部指標：

- `averages.pyx:AdaptiveMovingAverage` 使用內部 `EfficiencyRatio`
- `averages.pyx:VariableIndexDynamicAverage` 使用內部 `CMO`
- `volatility.pyx:KeltnerChannel` 組合了 `MovingAverage` + `ATR`
- `volatility.pyx:KeltnerPosition` 封裝了一個完整的 `KeltnerChannel`
- `volume.pyx:Pressure` 封裝了 `ATR` + `MovingAverage`

大多數需要移動平均的指標都接受 `MovingAverageType` 列舉，並使用 `averages.pyx:MovingAverageFactory.create()` 來實例化它。更改 MA 型別是一個配置更改，而不是程式碼更改。

## 內部依賴鏈

`averages.pyx` 幾乎被所有其他檔案使用（透過 `MovingAverageFactory` 和 `MovingAverageType`）。`momentum.pyx` 被 `averages.pyx` 使用 (EfficiencyRatio 用於 AMA, CMO 用於 VIDYA)。`volatility.pyx` 被 `volume.pyx` 使用 (ATR 用於 Pressure)。這建立了：**base -> averages -> momentum -> volatility -> volume**。新增指標時請尊重這個順序 — 向後依賴會在 Cython 級別中斷。

## 導航：指標到檔案

| 檔案 | 指標（關鍵範例） |
|------|------------------------------|
| `averages.pyx` | SMA, EMA, DEMA, WMA, HMA, AMA (Kaufman), Wilder, VIDYA — 全部都繼承自 `MovingAverage` |
| `momentum.pyx` | RSI, CMO, Stochastics, CCI, EfficiencyRatio, ROC |
| `trend.pyx` | MACD, IchimokuCloud, AroonOscillator, DI, AMAT, LinearRegression, Swings |
| `volatility.pyx` | ATR, BollingerBands, DonchianChannel, KeltnerChannel/Position |
| `volume.pyx` | OBV, VWAP (daily reset), KVO, Pressure |
| `fuzzy_candlesticks.pyx` | FuzzyCandlesticks — 將 K 線資料簡化為模糊語言標籤 |
| `spread_analyzer.pyx` | SpreadAnalyzer — 僅限報價跳動，這是唯一不基於 K 線的指標 |

`MovingAverageType` 列舉：`averages.pyx` (SIMPLE, EXPONENTIAL, DOUBLE_EXPONENTIAL, WILDER, HULL, ADAPTIVE, WEIGHTED, VARIABLE_INDEX_DYNAMIC)。

## 新增新指標時的注意事項

1. 子類別 `base.pyx:Indicator` — 實作 `_reset()`（強制）
2. `update_raw(...)` 是規範路徑；`handle_*` 方法解包並委託給它
3. 在第一次更新時呼叫 `_set_has_inputs(True)`，預熱完成後呼叫 `_set_initialized(True)`
4. 如果接受 MA 型別，使用 `MovingAverageFactory.create()`
5. **更新 `.pxd`** 以宣告 C 級介面（經常被遺忘，導致建構中斷）
6. 在 `__init__.py` 中註冊 (import + `__all__`)

## 模組邊界

- **上游**：`model/` (Bar, QuoteTick, TradeTick, Price)，`core/` (Condition, PriceType, fast_mean, fast_std_with_mean, fast_mad_with_mean)
- **下游**：`common/actor.pyx` (註冊), `trading/strategy.pyx` (使用者策略)
- **不適用**：沒有外部資料獲取，沒有持久性，沒有直接使用 Rust。指標純粹是計算性的。
