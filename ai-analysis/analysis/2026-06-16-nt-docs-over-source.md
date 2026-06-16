# Flow Feedback — 2026-06-16 — NT docs 優先於源碼推論

## 摩擦（user 原話）
> 「我太晚讀 NT docs」
>
> （redirect 原話）：「你 `/Users/ctai/Github/nautilus_trader/docs/concepts` 有仔細看嗎」

## session 摘要
融資券架構探索（margin trading Phase 2）。為判定「NT 能否在一 venue 下多帳戶 / 區分融資現股部位」，我反覆讀 NT **源碼**（`cache.pyx`、`engine.pyx`、`actor.pyx`）推論，**兩次過度結論**：
1. 從 `cache._index_venue_account: dict[Venue, AccountId]`（1:1）推論「一 venue 一帳戶是硬限制，(b') 多帳戶死路」。
2. 從 `oms_type` per-venue 推論「HEDGING all-or-nothing，不能分現股」。

用戶指引讀 `nautilus_trader/docs/concepts/` 後，**docs 直接推翻兩個結論**：
- `accounting.md:192` 明文「multi-account venues」（一 venue 可多帳戶，account_id scope）。
- `positions.md:175-180` 雙層 OMS 表（strategy × venue 可不同），`execution.md:129-143`「custom position IDs only valid under HEDGING；to partition positions configure HEDGING」。

docs 是權威且更省事，但我全程源碼優先，直到用戶出手。

## type-1 建議（時機）
- **探索第三方框架「能力/概念」時，先讀官方 concepts docs，再用源碼補實作細節** → `source-driven-development` skill
  - 例子：查「NT 一 venue 能否多帳戶」時，我直接 rg `cache.pyx` 的 `_index_venue_account`，從 dict 型別推論「1:1 硬限」。
  - counter-factual：若當時先讀 `docs/concepts/accounting.md`，會看到「multi-account venues」官方說明，直接定案（且 `account_for_venue(venue, account_id)` 的 account_id 參數就在 docs 裡），不會從單一資料結構過度推論、浪費兩輪 + 用戶糾正。

## type-2 建議（設計）—— 強制
- **查證規則缺「framework 官方 docs 優先於源碼推論」指引，且 NT 查證路徑是 source-first** → 規則層（`lsp-navigation` / CLAUDE.md「查證策略」+ NT 模組觸發器）
  - 例子：CLAUDE.md「查證策略」對 NT 是「NT source tree 優先 → stubs/ fallback」；`lsp-navigation` 強調讀 `.venv` source。這對「how is X implemented」（實作細節）正確，但對「does NT support X / what can NT do」（**能力/概念**）會誘導源碼 trawling → 過度結論。我兩次踩中：從 `dict[Venue, AccountId]`（1:1）推「硬限」、從 `oms_type` per-venue 推「all-or-nothing」，都是「**從實作資料結構反推能力邊界**」的謬誤（資料結構是某實作選擇，不是能力上限）。
  - counter-factual：若查證規則（或 NT 段 CLAUDE.md）有「**NT 能力/概念查證：先讀 `nautilus_trader/docs/concepts/`（權威，高水準）；源碼僅補實作細節；禁從單一資料結構推論能力限制**」，我查多帳戶/OMS 時會先讀 docs，看到官方 multi-account + dual-OMS + HEDGING-partition 說明，**一次定案**，省掉兩輪過度結論 + 用戶 redirect。docs 該被列為 NT 查證的**第一層**（在 source 之前），尤其 `docs/concepts/` 這種高品質概念文件。
  - 為何 type-2 而非純時機：`source-driven-development` skill 存在但框架是「context7 線上 library docs」——對 NT 這種**本地 repo 有 docs/concepts/** 的框架沒覆蓋（NT docs 在 `~/Github/nautilus_trader/docs/`，非 context7）。且 CLAUDE.md 的 NT 查證路徑明確 source-first，**主動誘導**我源碼優先。這是規則設計缺口，不只是我沒用 skill。

## tags
`source-driven-development` `lsp-navigation` `CLAUDE.md` `ep-validate` `nt-docs`
