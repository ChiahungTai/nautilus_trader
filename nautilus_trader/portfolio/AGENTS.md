# nautilus_trader/portfolio/

Portfolio state manager -- tracks positions, account balances, margins, and PnL across all trading activity.

## Architecture

Events flow in via MessageBus subscriptions; Portfolio mutates internal state; consumers query via read-only facade.

```
Events → MessageBus → Portfolio handlers → state update
                                              ↓
RiskEngine / ExecEngine / Strategies ← PortfolioFacade (read-only)
```

## Navigation

| Concept | Location |
|---------|----------|
| Read-only query interface | `base.pyx:PortfolioFacade` |
| Full implementation (Cython) | `portfolio.pyx:Portfolio` |
| Config | `config.py:PortfolioConfig` |
| Rust equivalent + AccountsManager | `crates/portfolio/` |

## Design Decisions

- **Facade pattern** → `base.pyx:PortfolioFacade` -- exposed to RiskEngine and ExecEngine as read-only; only Portfolio's own event handlers mutate state.
- **Pending calculations** -- when price or exchange rate data is missing during init, instruments go into `_pending_calcs`. Each tick/bar update retries pending instruments.
- **Price resolution fallback** -- 3-tier chain: primary price type (bid/ask/mark) → LAST → bar close. Ensures PnL degrades gracefully.
- **Snapshot-based realized PnL** -- incremental caching: tracks processed counts per position, only processes new snapshots, full rebuild on purge detection.
- **Missing price warn-once** -- first occurrence warns, subsequent skips are silent. Instruments removed from tracking when priced again.
- **Multi-account currency safety** -- validates all accounts share same base currency before aggregation. Currency mismatch → error log + `None` return.

## Config Notes

`snapshot_interval_ms` is Rust-only (periodic `PortfolioSnapshot` via timer, stored in 1M-capacity ring buffer). The Cython Portfolio used by Python BacktestEngine and live nodes ignores this field.

## Connections

| Consumer | Interface | Key usage |
|----------|-----------|-----------|
| RiskEngine | `PortfolioFacade` | `is_net_long()`, `is_net_short()` for REDUCING state |
| ExecEngine | `PortfolioFacade` | Position direction for execution algorithms |
| Cache | Read-heavy + writes | Instrument/account/position/price lookups; writes account state |
| MessageBus | Subscriptions | `data.quotes.*`, `data.bars.*`, `events.order.*`, `events.position.*` |