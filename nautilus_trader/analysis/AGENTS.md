# nautilus_trader/analysis/

Portfolio performance analysis and backtest visualization. Two concerns: (1) computing statistics from positions/returns, (2) rendering interactive tearsheets via Plotly.

## Python/Rust Split for Statistics

Performance statistics (Sharpe, CAGR, MaxDrawdown, WinRate, etc.) live in Rust (`nautilus_pyo3`) — imported from `core.nautilus_pyo3` as classes like `SharpeRatio`, `CalmarRatio`. The Python `PortfolioStatistic` base class in `statistic.py` exists for user-defined custom statistics. `analyzer.py:PortfolioAnalyzer` detects which kind it is via `_is_pyo3_statistic()` and adapts the calling convention: PyO3 stats receive `list[float]` / `dict[int, float]`, Python stats receive `pd.Series`.

**Why both exist**: Rust stats are fast and consistent with the rest of the platform. Python `PortfolioStatistic` is the extension point for custom metrics without recompiling.

## Dual Returns Series

`PortfolioAnalyzer` maintains two independent returns series that serve different purposes:

- **Position returns** (`_position_returns`): aggregated from per-position `realized_return` at close time. Available for any backtest.
- **Portfolio returns** (`_portfolio_returns`): computed from account balance snapshots via `_calculate_portfolio_returns()`. Only available for single-currency accounts with >= 2 balance events. Multi-currency or sparse data silently falls back to position returns.

The `_returns` alias points to portfolio returns when available, otherwise position returns. The `_sync_returns_alias()` method keeps this up-to-date after every mutation. Consumer code should use `returns()` (the alias) unless it explicitly needs one series or the other.

## Report Generation

`reporter.py:ReportProvider` is a stateless utility (all static methods) that converts NT domain objects to `pd.DataFrame`. Four report types: orders, order fills, fills (per fill event), positions, account state. The fills report flattens `OrderFilled` events from within orders — each fill gets its own row.

## Tearsheet System

Plotly-based visualization with optional dependency (`nautilus_trader[visualization]`). The `PLOTLY_AVAILABLE` flag guards every public function — `ImportError` raised at call time, not import time.

### Two-Level API

- **High level**: `tearsheet.py:create_tearsheet(engine)` — extracts everything from a `BacktestEngine` and delegates to the stats-first API.
- **Low level**: `tearsheet.py:create_tearsheet_from_stats(...)` — accepts pre-computed stats dicts + returns series. For offline analysis without an engine.

### Returns Resolution for Tearsheets

`_resolve_tearsheet_returns()` picks the best series in priority order:
1. `analyzer.portfolio_returns()` — single-venue account daily returns
2. `_calculate_account_returns()` — aggregates across ALL cached accounts (needed because `engine.pyx` recalculates analyzer per venue)
3. `analyzer.returns()` — per-position returns as last resort

**Why step 2 exists**: The engine's analyzer is per-venue, but tearsheets need a combined view. `_calculate_account_returns()` walks every cached account and sums balances before computing daily returns.

### Pluggable Registries

Two registries enable extension without modifying source:

- **Chart registry** (`_CHART_REGISTRY`): `register_chart(name, func)` / `@register_chart(name)` decorator. Used by standalone chart functions (e.g., `create_equity_curve` is registered as `"equity"`).
- **Tearsheet chart specs** (`_TEARSHEET_CHART_SPECS`): `_register_tearsheet_chart()` maps names to subplot renderers. Controls grid position and data flow within the tearsheet figure.

`TearsheetCustomChart` bridges the two — it references a registered chart name and forwards `args` as kwargs to the renderer.

### Theme System

`themes.py` manages a `_THEMES` dict of `{template, colors}` configs. Built-in themes: `plotly_white`, `plotly_dark`, `nautilus`, `nautilus_dark`. `register_theme()` validates required color keys. `_normalize_theme_config()` backfills table-specific colors for themes registered before those keys existed.

## Config

`config.py:TearsheetConfig` (frozen msgspec struct) controls tearsheet layout: chart list, theme, grid dimensions, benchmark settings. Default charts: run_info, stats_table, equity, drawdown, monthly_returns, distribution, rolling_sharpe, yearly_returns. `GridLayout` controls subplot dimensions.

## Navigation

| File | Core Class/Function | Role |
|------|-------------------|------|
| `analyzer.py` | `PortfolioAnalyzer` | Accumulates positions/returns, delegates to registered statistics |
| `analyzer.py` | `_is_pyo3_statistic()` | Detects Rust vs Python statistic by module path |
| `statistic.py` | `PortfolioStatistic` | Base class for custom Python statistics |
| `reporter.py` | `ReportProvider` | Static methods: NT objects → DataFrames |
| `tearsheet.py` | `create_tearsheet()`, `create_tearsheet_from_stats()` | High/low level tearsheet entry points |
| `tearsheet.py` | `register_chart()`, `_register_tearsheet_chart()` | Chart registries (standalone + tearsheet subplot) |
| `tearsheet.py` | `_resolve_tearsheet_returns()` | Multi-venue returns aggregation |
| `config.py` | `TearsheetConfig`, `GridLayout` | Frozen config structs |
| `themes.py` | `get_theme()`, `register_theme()` | Theme registry and validation |

## Module Boundaries

- **Upstream**: `model/` (Position, Order, AccountState), `accounting/` (Account balances), `backtest/` (BacktestEngine for tearsheet), `core/nautilus_pyo3` (Rust statistics)
- **Downstream**: consumed by backtest runners (footer stats), user analysis scripts
- **Does NOT**: define trading domain types, execute trades, manage positions, or depend on any specific adapter

## Conventions

- Annualization uses 252 trading days (`TRADING_DAYS_PER_YEAR`)
- Static image export (`.png`, `.svg`, etc.) requires Kaleido (`nautilus_trader[visualization]`)
- All reports use `client_order_id` or `position_id` as DataFrame index, sorted chronologically
- `_write_figure()` dispatches on file extension: HTML via Plotly native, static via Kaleido
