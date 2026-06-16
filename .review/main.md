## Code Review Findings — main

> Changeset: LSP stubgen-pyx workflow — 4 generated `.pyi` (cache/actor/engine/portfolio), orchestrator + 2 helper scripts + README, CLAUDE.md doc update, 1 flow-feedback note.
> Reviewed: 2026-06-16 · Followup-verified: 2026-06-17 · Reviewer: /code-review → /followup-review

| ID | 嚴重度 | 檔案:行 | 問題 | 建議 | 狀態 | 決策 |
|----|--------|---------|------|------|------|------|
| F1 | 🔴 critical → ✅ | `scripts/lsp_stubs/generate_nt_stubs.sh` (gitignored) | 文件記載的 orchestrator 被 `.gitignore:85 *.sh` 吞掉，未被 tracked | ✅ 採納 Option B：改寫為 `generate_nt_stubs.py`（subprocess orchestrator，非 gitignored） | **verified** | 採納 Option B。DEPTH-SAMPLE 驗證：regenerate portfolio.pyi byte-identical（SHA256 相同）；pyright 0 errors、ruff clean、faithful+improved port（tempfile + try/finally + check=True） |
| F2 | 🟠 important → ✅ | `CLAUDE.md` 「已覆蓋模組」 | (a) 缺 5 indicator stubs；(b) cache/cache 重複出現、engine/actor/portfolio 只在段落 | ✅ 採納：「已覆蓋模組」補 indicators、移除 cache/cache；generated 4 模組集中段落；README 同步 `.sh→.py` | **verified** | 全部修正。README 另新增「orchestrator 全 subprocess」設計決策（high-signal：避免 sys.path.insert 觸發 reportMissingImports） |
| F3 | 🟠 important → ⏸ | 消費端 `mosaic_alpha_trading_lab/scripts/sync_nt_stubs.sh` | 4 個新 generated stubs 需加入 lab `NT_MODULES[]` 才會 sync 到 lab venv | 跨 repo follow-up（本 repo 無法完成） | **open** | 跨 repo pending action。README:29 已記載此要求，作 ship 前確認項追蹤；不阻塞本 repo commit |

### 追加：本 review 週期額外採納的 Suggestion（非 finding，僅記錄）
- S1 C901（make_self_contained 過複雜）→ ✅ 抽出 `_merge_typing_and_drop_imports()` helper，ruff clean
- S3 `open()` 無 encoding → ✅ 改 `Path.read_text/write_text(encoding="utf-8")`
- D213 docstring → ✅ ruff clean
- N1（new, Suggestion）：orphaned `generate_nt_stubs.sh` 仍存於工作目錄（gitignored、dead — README/CLAUDE.md 已改指 `.py`）。建議刪除避免雙 orchestrator 混淆。未持久化（Suggestion 級）
