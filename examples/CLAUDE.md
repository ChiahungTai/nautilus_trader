# examples/

Runnable example scripts for learning NautilusTrader concepts and adapter integrations.

## Directory Layout

| Directory | Purpose |
|-----------|---------|
| `backtest/` | Backtest engine examples: numbered tutorials + strategy-specific backtests |
| `backtest/notebooks/` | Databento-specific backtest notebooks (Jupyter-flavored .py) |
| `live/` | Per-adapter live trading examples |
| `sandbox/` | Sandbox (live data + simulated execution) examples per adapter |
| `other/` | FSM, minimal reproducible example |
| `utils/` | Shared helpers used by numbered tutorials |

## Conventions

- Numbered tutorials (`example_01` through `example_11`) are self-contained pairs: `run_example.py` (engine setup) + `strategy.py` (strategy logic). Run in order -- each builds on the previous concept.
- `*_data_tester.py` = connect and verify data streaming works. `*_exec_tester.py` = connect and verify order execution works. These are adapter smoke tests.
- All live examples carry the disclaimer: "THIS IS A TEST STRATEGY WITH NO ALPHA ADVANTAGE WHATSOEVER."
- Credentials come from environment variables, never hardcoded.
- `interactive_brokers_v2/` is the newer IB adapter; prefer it over `interactive_brokers/`.

## Navigation: "I want to learn about..."

### Backtest Fundamentals (numbered tutorials, run in order)

| # | Concept |
|---|---------|
| 01 | Loading bars from custom CSV → `backtest/example_01_load_bars_from_custom_csv/` |
| 02 | Clock timers in strategy → `backtest/example_02_use_clock_timer/` |
| 03 | Bar aggregation (1-min into 5-min) → `backtest/example_03_bar_aggregation/` |
| 04 | Querying DataCatalog → `backtest/example_04_using_data_catalog/` |
| 05 | Portfolio state (positions, balances) → `backtest/example_05_using_portfolio/` |
| 06 | Custom objects in Cache → `backtest/example_06_using_cache/` |
| 07 | Built-in indicators → `backtest/example_07_using_indicators/` |
| 08 | Cascaded (chained) indicators → `backtest/example_08_cascaded_indicator/` |
| 09 | Custom Events via MsgBus → `backtest/example_09_messaging_with_msgbus/` |
| 10 | Custom Data via Actors → `backtest/example_10_messaging_with_actor_data/` |
| 11 | Lightweight signal-based messaging → `backtest/example_11_messaging_with_actor_signals/` |

### Strategy Patterns (backtest/)

Notable strategy examples by concept -- filenames are self-descriptive:

- EMA crossover on FX ticks/bars, bracket orders, market making, grid trading, orderbook imbalance, trailing stop, TWAP execution algorithm, config-driven backtest via `BacktestRunConfig`, synthetic data for PnL testing, Polymarket backtesting
- Bracket order examples show internal vs external risk engine: `fx_ema_cross_bracket_gbpusd_bars_internal.py` vs `_external.py`

### Live Trading by Adapter

Each adapter directory under `live/` contains data/exec testers and strategy-specific examples. Available adapters: Binance, Bybit, dYdX, Hyperliquid, Interactive Brokers (v1 + v2), Databento (data only), Deribit, OKX, Kraken, BitMEX, Polymarket, Tardis (replay only), Betfair, Architect AX.

### Sandbox (live data + simulated execution)

Real data feed + simulated order execution for strategy validation without capital risk. One file per adapter under `sandbox/`.

### Other

- FSM usage → `other/state_machine/run_example.py`
- Minimal reproducible backtest template → `other/minimal_reproducible_example/`

## Shared Utilities

- `utils/data_provider.py:prepare_demo_data_eurusd_futures_1min()` -- loads test EURUSD futures 1-min bars. Used by tutorials 02-11.