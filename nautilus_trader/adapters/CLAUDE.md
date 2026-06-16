# Adapters

Exchange/broker integration layer. Each subdirectory is a self-contained adapter for a specific venue or data provider.

## Architecture: Rust Core + Python Shell

Most adapters split across two layers: Rust crate → PyO3 → Python orchestration.

**Rust-backed adapters** have `crates/adapters/<name>/` providing HTTP/WebSocket clients and venue-specific types, exposed as `nautilus_pyo3.<Name>HttpClient`. Python side in `nautilus_trader/adapters/<name>/` orchestrates into NT's data/execution framework.

**Python-only adapters**: `interactive_brokers_pyo3/` (config wrapper around Rust IB bindings, no data.py/execution.py), `shioaji/` (skeleton, empty).

### Wiring Flow → `nautilus_trader/live/node_builder.py:TradingNodeBuilder`

1. User registers factory: `add_data_client_factory("VENUE", Factory)`
2. `build_data_clients(config)` looks up factory by name → `factory.create(loop, name, config, msgbus, cache, clock)`
3. Factory creates HTTP client (Rust via PyO3) → instrument provider → DataClient/ExecutionClient
4. Client registered with `data_engine` / `exec_engine`

### Structural Variants (WHY they differ)

| Adapter | Structure | Reason |
|---------|-----------|--------|
| `binance/` | `spot/`, `futures/` subdirs with separate HTTP/WS clients | Binance has fundamentally different APIs for spot vs futures |
| `interactive_brokers/` | Full Python: `client/`, `parsing/`, `historical/`, `gateway.py` | IB TWS API is Python-native, no Rust crate |
| `interactive_brokers_pyo3/` | Config-only, re-exports Rust config with `__new__` constructors normalizing param names | Rust live node handles client construction; Python side only needs config |
| `sandbox/` | Execution-only (no data client), factory receives extra `portfolio` param | Simulates fills against portfolio state |
| `tardis/`, `databento/` | Data-only (no execution client) | Historical market data replay only |

## _template/ — New Adapter Starting Point

Skeleton `LiveDataClient`, `LiveMarketDataClient`, `LiveExecutionClient`, `InstrumentProvider` with all abstract methods raising `NotImplementedError`. Copy and implement. Remove all `# pragma: no cover` in implementation.

## Key Patterns

### Shared HTTP Client → `factories.py` in each adapter

`@lru_cache(1)` on HTTP client constructors so data and execution clients share one Rust HTTP client instance. **Constraint**: parameters to the cached function must be hashable (tuples, not lists).

### PyO3 Enum Passthrough

Venue-specific enums defined in Rust, re-exported through `nautilus_trader/core/nautilus_pyo3.py`. Config classes accept these enums directly.

### Instrument Loading Flow

`InstrumentProvider.load_all_async()` → Rust HTTP client → PyO3 instrument structs → `instruments_from_pyo3()` conversion → Nautilus Python model objects → cache.

### WebSocket Callbacks

Data clients create per-product-type WS clients (Rust). Callbacks stream through PyO3 as Python callables → data client translates to Nautilus types → publishes to message bus.

## Conventions

- Adapter names are UPPERCASE strings matching venue (`"BYBIT"`, `"BINANCE"`)
- Adapters never directly import from each other
- `env.py` at this level provides `get_env_key()` / `get_env_key_or()` for API credential env var lookups
- Base classes are Cython: `LiveMarketDataClient`/`LiveDataClient` → `nautilus_trader/live/data_client.pyx`, `LiveExecutionClient` → `nautilus_trader/live/execution_client.pyx`, `InstrumentProvider` → `nautilus_trader/common/providers.pyx`