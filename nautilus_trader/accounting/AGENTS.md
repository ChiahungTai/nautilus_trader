# nautilus_trader/accounting/

金融會計層：餘額、鎖定資金、佣金、保證金、損益實現。**此 fork 的 runtime 走 Cython**（`accounts/{cash,margin,base,betting}.pyx`、`manager.pyx`、`margin_models.pyx`），但 **Rust `crates/model/src/accounts/` 有等價實作**（`cash.rs`/`margin.rs` 的 `calculate_pnls`、`margin_model.rs` 的 `Standard/LeveragedMarginModel`）——是 PyO3 路徑（未來 Rust-native runtime），**不被 Cython `Portfolio` 執行**。兩層邏輯相同；runtime 查證讀 `.pyx`，詳見 nt-query `account-model.md` Layer 段。

## 設計決策

- **事件溯源狀態**：帳戶維護 `AccountState` 事件的列表。狀態是從事件歷史中重建的，而非就地更新。
- **`CashAccount` 中的優雅降級**：如果鎖定金額超過總餘額，會將可用餘額限制為零，而不是崩潰。這是這裡的一個關鍵哲學偏離了 NT 其他部分的快速失敗崩潰設計。
- **`MarginAccount` 工具類型分支**：高級工具（期權）在每次成交時將名義金額實現為現金流；其他工具僅在頭寸減少時實現損益。這種分支行為是這裡最不顯而易見的邏輯。
- **基於發行商的工廠**：`AccountFactory.create()` 從 `AccountState` 事件資料分派給子類別。透過 `register_account_type()` 註冊自訂帳戶類型，而無需修改工廠。

## 模組邊界

會計模組不會：
- 計算投資組合層級的指標（這是 `Portfolio` 的工作）
- 持有交易狀態（這是 `Portfolio` 的工作）
- 管理訂單生命週期

## 連接

- **Portfolio** 擁有 `AccountsManager` → 將所有餘額/保證金計算委託給它
- **Cache** 提供 `CacheFacade`（唯讀）用於帳戶管理器內部的工具/頭寸查找
- **Model** 提供 `AccountState`、`OrderFilled`、`Money`、`Currency`、`AccountBalance`、`MarginBalance`

## 導航

| 概念 | 位置 |
|---------|----------|
| 帳戶類型層級 | `accounts/base.pyx:Account` → `accounts/cash.pyx:CashAccount` → `accounts/betting.pyx:BettingAccount`；`accounts/margin.pyx:MarginAccount` |
| 帳戶協調器（Portfolio 消費者） | `manager.pyx:AccountsManager` |
| 保證金計算策略 | `margin_models.pyx:MarginModel` / `LeveragedMarginModel` |
| 隔夜 FX 展期利息 | `calculators.pyx:RolloverInterestCalculator` |
| 帳戶錯誤類型 | `error.py:AccountError`、`AccountBalanceNegative`、`AccountMarginExceeded` |
