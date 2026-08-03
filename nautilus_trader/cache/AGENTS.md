# nautilus_trader/cache/

In-memory trading state cache with optional database backing. The single source of truth for current orders, positions, instruments, accounts, and market data within a running node.

## Architecture

Layered design: Cython in-memory core with optional database adapter for persistence across restarts.

- Read interface → `base.pyx:CacheFacade` (abstract, consumers type-hint against this)
- Full read/write → `cache.pyx:Cache` (Cython for hot-path performance, cdef/cpdef methods)
- Database abstract → `facade.pyx:CacheDatabaseFacade`
- Redis adapter → `database.pyx:CacheDatabaseAdapter` (Cython wrapping `nautilus_pyo3.RedisCacheDatabase`)
- PostgreSQL adapter → `adapter.py:CachePostgresAdapter` (pure Python wrapping `nautilus_pyo3.PostgresCacheDatabase`)
- Config → `config.py:CacheConfig`

## Key Design Decisions

- **In-memory is always authoritative.** Database writes are fire-and-forget with eventual consistency. Never read from DB to answer a query.
- **Consumers use CacheFacade, not Cache.** The read-only facade is the public interface; `Cache` is internal.
- **transformers.py** bridges the impedance mismatch between Cython model objects and PyO3 objects (needed because the PostgreSQL adapter goes through PyO3 directly, not Cython).

## Database Backing

### Redis (Production-ready)

Activated via `CacheConfig(database=DatabaseConfig(type="redis"))`. Kernel wires automatically during node startup.

- Async writes: pipelined/batched via `buffer_interval_ms` config

### PostgreSQL (WIP -- NOT wired into kernel)

Exists in `adapter.py` and Rust (`crates/infrastructure/src/sql/`) but the kernel only recognizes `type="redis"` and raises `ValueError` for anything else.

- **FK dependency ordering required**: currency must exist before instrument, instrument before order. Violations silently corrupt data.
- Write model: MPSC channel + background thread -- must `await eventually()` to confirm writes
- Stores more than Redis: order_events, position snapshots, signals, market data

## Persistence Context (6 Layers)

The cache is one of six persistence layers. Understanding which layer stores what prevents misconfiguration:

| Layer | Stores | Config Key |
|-------|--------|------------|
| Cache DB | Current state: orders, positions, accounts, instruments | `cache.database` |
| MessageBus DB | Pub/sub messages for cross-process | `message_bus.database` |
| Event Store | Append-only event log (crash recovery) | Injected via Rust builder |
| Data Catalog | Historical market data (backtesting) | `catalogs` |
| Streaming Writer | Live market data with rotation | `streaming` |
| Logger | System logs | `logging` |

**None enabled by default.** Without config, cache is pure in-memory -- all state lost on process exit.

## Non-obvious Defaults

- `snapshot_orders` and `snapshot_positions` default to `False` even when DB is configured -- must explicitly enable
- `drop_instruments_on_reset` defaults to `True` -- instruments cleared from memory on reset
- `tick_capacity` / `bar_capacity` are deque limits (default 10,000), not database limits

## Module Boundaries

- **Upstream**: `model/` (identifiers, orders, positions, events), `core/` (UUID, FSM), `common/` (MessageBus, Clock, Logger)
- **Downstream**: `execution/`, `portfolio/`, `trading/`, `risk/`, `system/` (kernel assembly)
- **Database adapters** depend on `core/nautilus_pyo3` (Rust bindings) and `common/` (MsgSpec serializer)
