# Backtest Engine

Historical simulation engine that replays market data through the same strategy/execution code path used in live trading.

## Core Simulation Loop

engine.pyx:`BacktestEngine.run()` drives a single-pass loop over time-sorted data:

1. Advance `TestClock` to next data timestamp, draining scheduled timers via Rust `TimeEventAccumulator`
2. Route data point to matching `SimulatedExchange` by venue (quotes/trades/bars/deltas)
3. `_process_and_settle_venues` -- drain pending trading commands, iterate `OrderMatchingEngine`s for fills, run `SimulationModule`s
4. Feed data into `DataEngine.process()` for strategy callbacks (on_bar, on_quote_tick, etc.)
5. Strategies react, submit orders through `BacktestExecClient` -> `SimulatedExchange` message queue

**Design intent**: `BacktestDataClient` and `BacktestExecClient` extend the same base classes as live clients (`DataClient`, `ExecutionClient`). Strategies and the execution engine cannot distinguish backtest from live. This is NT's primary code-path sharing mechanism.

## Architecture

`BacktestEngine` (engine.pyx) owns a `NautilusKernel` and drives time. Per-venue `SimulatedExchange` owns per-instrument `OrderMatchingEngine`s (created lazily). `BacktestExecClient` (execution_client.pyx) is a thin pass-through forwarding commands to the exchange. `BacktestDataClient` (data_client.pyx) routes subscribe/request to the engine via msgbus.

### Key Components

- **SimulatedExchange** → engine.pyx:`SimulatedExchange` -- one per venue. Holds `OrderMatchingEngine` per instrument (created lazily when data arrives), message queue for latency simulation, `SimulationModule` list for extensible venue-level simulation.
- **OrderMatchingEngine** → engine.pyx:`OrderMatchingEngine` -- wraps shared `MatchingCore` (from execution/matching_core.pyx). Adds per-instrument order book, fill determination, order lifecycle events, option exercise/expiry settlement, queue position tracking, bar-to-tick decomposition.
- **BacktestDataIterator** → engine.pyx:`BacktestDataIterator` -- heap-based k-way merge of multiple sorted data streams. Single-stream fast path bypasses heap. Priority system controls ordering for same-timestamp data.

## Simulation Models

All pluggable via `BacktestVenueConfig`:

| Model | Purpose | Key Variants |
|-------|---------|-------------|
| FillModel → models/fill.pyx | Fill probability and slippage | `BestPriceFillModel`, `ProbabilisticFillModel`, `CompetitionAwareFillModel` |
| FeeModel → models/fee.pyx | Commission per fill | `MakerTakeFeeModel`, `FixedFeeModel`, `PerContractFeeModel` |
| LatencyModel → models/latency.pyx | Command processing delay | `base_latency + operation_latency` via inflight queue; no model = immediate processing |

## Language Boundaries

| Layer | Language | Why |
|-------|----------|-----|
| Timer scheduling, matching core, price/quantity primitives | Rust | Performance-critical path shared with live trading |
| Simulation loop, order matching, fill/fee calculation | Cython (engine.pyx, data_client.pyx, execution_client.pyx, modules.pyx, models/*.pyx) | Hot loop with `cdef`/`cpdef` for speed |
| Configuration, orchestration, results | Pure Python (config.py, node.py, node_builder.py, results.py) | Not performance-critical |

## Entry Points

1. **Direct API**: Create `BacktestEngine`, call `add_venue()` / `add_instrument()` / `add_data()` / `add_strategy()`, then `run()`
2. **Config-driven**: Create `BacktestRunConfig` (with `BacktestVenueConfig` + `BacktestDataConfig`), pass to `BacktestNode`. Node creates engines, loads data from `ParquetDataCatalog`, runs, collects `BacktestResult`.

Config-driven path supports `chunk_size` for streaming large datasets, multiple runs per node, and live data client integration for hybrid download+backtest workflows.

## Timer and Clock

`TestClock` is set statically (not real-time) during backtest. `TimeEventAccumulator` (Rust) collects scheduled timers. `_advance_time` pops timers in timestamp order, executing callbacks. Chained timers (callback schedules another timer) are handled by re-advancing after each callback.

## Conventions

- All data must be sorted by `ts_init` before `run()`. Use `add_data(..., sort=True)` or call `sort_data()` explicitly.
- `SimulatedExchange` lazily creates `OrderMatchingEngine` when data for a new instrument arrives.
- `BacktestDataClient` subscribe methods are mostly no-ops (data is pre-loaded). `BacktestMarketDataClient` forwards subscriptions to the engine endpoint for catalog queries.
- Option exercise/expiry is handled inside `OrderMatchingEngine` -- supports cash settlement, physical delivery, and OTM expiry.
- `FORCE_STOP` flag allows early termination from any callback; checked at every loop iteration.
- `streaming=True` mode pauses at data exhaustion without finalizing, enabling batch-by-batch loading for out-of-memory datasets.
