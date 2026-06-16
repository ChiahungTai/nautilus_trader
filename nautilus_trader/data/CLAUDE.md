# Data Engine

Central data routing, subscription management, and bar aggregation. Shared between backtest and live contexts — same `DataEngine` and `BarAggregator` code runs in both. Historical mode uses `TestClock` for deterministic time advancement.

## Architecture

Fan-in fan-out messaging system. The engine does NOT own data — it routes through `MessageBus` via topic-based pub/sub. `Cache` is the stateful layer.

```
DataClient (adapter)  -->  engine.process  -->  Cache + MessageBus publish  -->  Actor/Strategy callbacks
DataClient (adapter)  -->  engine.response -->  historical replay + cleanup
Actor/Strategy        -->  engine.execute  -->  client routing + subscription setup
Actor/Strategy        -->  engine.request  -->  catalog query or client dispatch
```

## Navigation

| Concept | Location |
|---------|----------|
| Central orchestrator | `engine.pyx:DataEngine` |
| Adapter base classes | `client.pyx:DataClient`, `client.pyx:MarketDataClient` |
| OHLCV accumulation + aggregators | `aggregation.pyx:BarBuilder`, `aggregation.pyx:BarAggregator` |
| Data message types | `messages.pyx` (`DataCommand`, `DataResponse`, Subscribe/Unsubscribe types) |
| Engine configuration | `config.py:DataEngineConfig` |
| Topic string construction | `nautilus_trader/common/data_topics.pyx:TopicCache` |

## Client Routing (`_execute_command`)

1. `client_id` in `external_clients` config → publish to bus only (no local client)
2. `BACKTEST` client exists → always route to it
3. Otherwise → route by `venue` via `_routing_map`, fallback to `_default_client`
4. First client without a `venue` becomes default

A single `MarketDataClient` handles multiple venues via `register_venue_routing()`.

## Bar Aggregation Pipeline

Two modes — the distinction matters for adapter implementors:

- **Internal aggregation** (`bar_type.is_internally_aggregated()`): engine subscribes to raw ticks, feeds through aggregator, emits completed bars. Aggregator is subscribed to message bus tick topics (trades for `LAST`, quotes for everything else).
- **External aggregation**: data client provides pre-aggregated bars directly.

Aggregator lifecycle: `SubscribeBars` → `_handle_subscribe_bars` → `_start_bar_aggregator` (conflict check: one aggregator per bar type key) → `_create_bar_aggregator` → `_setup_bar_aggregator` (subscribe to source data). Completed bars recurse through `self.process` → `_handle_data`.

`BarBuilder` handles continuous-future price adjustment (spread or ratio mode). Adjustment is pre-computed at `set_adjustment` so the per-tick hot path is pure C raw math with no Decimal allocation.

## Data Dispatch (`_handle_data`)

`isinstance` chain dispatches by type. Each handler: optionally caches (skipped when `_disable_historical_cache`) → publishes to correct topic via `TopicCache` → triggers side effects (synthetic instrument updates, option chain feeds, order book snapshot timers). Historical data uses separate topics from live data.

## Request/Response Patterns

- **Catalog-first**: check `BaseDataCatalog` before client
- **Long requests**: time-range generators split into sub-requests
- **Request groups**: fan-out to multiple sources, join responses
- **Join requests**: merge catalog + client responses
- **Aggregated bar requests**: create temporary aggregators during historical replay

State tracked per-request in `_request_workflows`, cleaned up on completion.

## Design Decisions

- **No data ownership**: engine routes; `Cache` owns state. Engine can reset without losing cached instruments.
- **Message bus as backbone**: engine never calls actors/strategies directly — all communication through topics.
- **Synthetic instruments**: reverse-index maps (`_synthetic_quote_feeds`, `_synthetic_trade_feeds`) map component instrument IDs to synthetic consumers.
- **Option chains**: `OptionChainManager` (Rust/PyO3) tracks active strikes around ATM, dynamically subscribes/unsubscribes as price moves.
- **Continuous futures**: `ContinuousFutureSubscriptionState` manages segment transitions with backward/ratio adjustments on bar builders.
- **Delta buffering**: when `buffer_deltas` enabled, `OrderBookDelta` objects buffered until `F_LAST` flag set, then batch-published.
- **Late import**: `_is_backtest_client` uses late import from backtest module to avoid circular dependency.

## Module Boundary

This module is the data routing layer. It does NOT:

- Define data model types → `nautilus_trader/model/data/`
- Implement adapter logic for specific exchanges → `nautilus_trader/adapters/`
- Manage persistence catalog API → `nautilus_trader/persistence/`
- Run backtests → `nautilus_trader/backtest/` (provides `BacktestMarketDataClient`)

Dependencies flow inward: adapters depend on `DataClient`/`MarketDataClient`, backtest depends on `DataEngine`. Data module does not import from adapters or backtest (except the one late import).

## Conventions

- All `.pyx`/`.pxd` (Cython). Config is pure Python (`config.py`).
- `cdef` for internal hot paths, `cpdef` for Cython+Python callable methods.
- `Condition` assertions for precondition checks (fail-fast).
- Data objects are value types from `nautilus_trader.model.data` or `nautilus_trader.core.data`.
- `TopicCache` is the single source of truth for topic strings.