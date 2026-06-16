# docs/concepts/ — Concept Documentation Index

Authoritative guides for NautilusTrader's core components. These docs describe **intended behavior and API contracts** — if discrepancies exist with `docs/api_reference/`, the API reference is correct.

## Concept Navigation

### Core Architecture

| Concept | File | Non-derivable knowledge |
|---------|------|------------------------|
| Platform overview | `overview.md` | Main features, intended use cases |
| Architecture | `architecture.md` | Design principles, structural decisions |
| Configuration | `configuration.md` | `T` vs `Option<T>` convention, builder patterns, adapter/engine common fields |
| Rust | `rust.md` | Writing actors/strategies in pure Rust, running backtests/live from `crates/` directly |

### Trading & Strategy

| Concept | File | Non-derivable knowledge |
|---------|------|------------------------|
| Actors | `actors.md` | Actor capabilities, data subscription lifecycle |
| Strategies | `strategies.md` | Event handler contracts, lifecycle guarantees |
| Orders | `orders.md` | **Emulated orders** (local stop/conditional simulation), 12 order types |
| Positions | `positions.md` | Aggregation from fills, PnL calculation, netting OMS snapshotting |
| Execution | `execution.md` | Multi-venue command/event flow, routing |
| Accounting | `accounting.md` | Per-instrument vs account-wide scopes, margin models |
| Portfolio | `portfolio.md` | Cross-strategy position tracking |
| Reports | `reports.md` | Backtest post-run analysis |

### Market Data & Instruments

| Concept | File | Non-derivable knowledge |
|---------|------|------------------------|
| Instruments | `instruments.md` | 18 instrument types, tick schemes |
| Value Types | `value_types.md` | Fixed-point precision behavior, immutability constraints — **common bug source** |
| Data | `data.md` | Bar aggregation pipeline, custom data |
| Custom Data | `custom_data.md` | Registration, persistence, Arrow encoding, runtime routing |
| Order Book | `order_book.md` | L1/L2/L3 book types, own order tracking, filtered views |
| Options | `options.md` | Option chain subscriptions, strike filtering |
| Greeks | `greeks.md` | Two paths: venue-provided real-time Greeks (PyO3) vs local `GreeksCalculator` (Black-Scholes), shock scenarios |
| Synthetics | `synthetics.md` | User-defined instruments from component prices |
| Continuous Futures | `continuous_futures.md` | Splicing via roll table, four adjustment modes, roll boundary policy |

### Infrastructure

| Concept | File | Non-derivable knowledge |
|---------|------|------------------------|
| Events | `events.md` | Causal chain (fill → position event), handler dispatch order, tracing orders to positions |
| Cache | `cache.md` | Central in-memory store, query patterns |
| Message Bus | `message_bus.md` | Point-to-point, pub/sub, request/response patterns, topic wildcards |
| Logging | `logging.md` | Rust-backed high-performance logging |
| Backtesting | `backtesting.md` | Simulation engine, fill/fee/latency models |
| Live Trading | `live.md` | Differences from backtesting, node configuration |
| Adapters | `adapters.md` | Requirements and patterns for exchange/data adapters |
| DST | `dst.md` | Deterministic Simulation Testing: seed-replayable execution, source-level seams |
| Visualization | `visualization.md` | Interactive tearsheets, extensible chart registry |

## Source Code Mapping

| Concept doc | Source module |
|-------------|--------------|
| `strategies.md` | `nautilus_trader/trading/strategy.pyx` |
| `actors.md` | `nautilus_trader/common/actor.pyx` |
| `orders.md` | `nautilus_trader/model/orders/` |
| `execution.md` | `nautilus_trader/execution/engine.pyx` |
| `backtesting.md` | `nautilus_trader/backtest/engine.pyx` |
| `order_book.md` | `nautilus_trader/model/book.pyx` |
| `value_types.md` | `nautilus_trader/model/objects.pyx` |
| `instruments.md` | `nautilus_trader/model/instruments/` |
| `data.md` | `nautilus_trader/data/engine.pyx` |
| `cache.md` | `nautilus_trader/cache/` |
| `message_bus.md` | `nautilus_trader/common/component.pyx` |
| `events.md` | `nautilus_trader/model/events/` |
| `greeks.md` | `nautilus_trader/model/greeks.pyx` |
| `configuration.md` | `nautilus_trader/config/` |
| `adapters.md` | `nautilus_trader/adapters/` |
| `dst.md` | `crates/testkit/` + test infrastructure |

## Conventions

- Code examples use Python (not pseudocode) — runnable as-is
- `:::note` and `:::warning` blocks highlight behavioral contracts and common pitfalls
- Related sections: `docs/developer_guide/` (coding standards, testing, FFI), `docs/how_to/` (task walkthroughs)