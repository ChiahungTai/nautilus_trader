# crates/infrastructure/

Database and messaging backends — implements `CacheDatabaseAdapter` and `MessageBusDatabaseAdapter` traits from `nautilus-common`. Concrete persistence layer for trading state (cache) and inter-process messaging.

## Architecture

```
src/
  redis/
    cache.rs      -- RedisCacheDatabase (CacheDatabaseAdapter impl)
    msgbus.rs     -- RedisMessageBusDatabase (MessageBusDatabaseAdapter impl)
    queries.rs    -- DatabaseQueries: stateless read helpers
  sql/
    cache.rs      -- PostgresCacheDatabase (CacheDatabaseAdapter impl)
    pg.rs         -- Connection management, schema bootstrapping
    queries.rs    -- DatabaseQueries: stateless CRUD helpers
    models/       -- sqlx::FromRow newtype wrappers for PostgreSQL rows
  python/         -- PyO3 bindings, mirrors redis/ + sql/ structure
```

Feature flags control compilation: `redis` (default), `postgres`, `python`. The `postgres` feature enables the `sql` module internally.

## Design Decisions

**Dual-connection architecture (Redis)** → `redis/cache.rs:RedisCacheDatabase`
Read connection owned by the struct; write connection owned by a background tokio task. Commands submitted through an unbounded `mpsc` channel. This avoids cross-runtime I/O conflicts — the Nautilus runtime manages the write lifecycle, reads are synchronous from the caller's perspective.

**Buffered write pipeline (both backends)**
Commands accumulate in a `VecDeque`, flushed either immediately (interval=0) or on a timer. `drain_buffer()` batches into a single Redis pipeline or sequential PostgreSQL queries. `Close` command drains remaining buffer before exit.

**Blocking bridge pattern** → `redis/cache.rs` / `sql/cache.rs`
Sync methods bridge to async via `get_runtime().block_on()` or `tokio::task::block_in_place()`. The `blocking_recv()` helper detects whether the caller is on the Nautilus runtime to choose the correct blocking strategy — wrong choice causes deadlock.

**PostgreSQL stores more entity types than Redis**
Redis: accounts, orders, positions, instruments, currencies, general, actors, strategies, health, custom. PostgreSQL adds: quotes, trades, bars, signals, order snapshots, position snapshots. This is because PostgreSQL is the archival/analytical backend; Redis is the low-latency live cache.

**Newtype wrappers for SQL rows** → `sql/models/`
All PostgreSQL row types use newtype wrappers (e.g., `CurrencyModel(pub Currency)`) with custom `sqlx::FromRow` impls. Separates SQL mapping logic from domain types — domain types stay clean of database concerns.

**Timestamp serialization bridge** → `redis/queries.rs`
Redis JSON stores timestamps as RFC3339 strings (human readability); MsgPack keeps them as nanosecond integers. Fields matching `ts_*` or `expire_time_ns` are recursively transformed during serialization/deserialization.

## Non-Obvious Constraints

**PostgreSQL FK ordering** → `sql/queries.rs`
Foreign key dependencies require strict insertion order: trader must exist before order_event, client must exist before order_event, order_initialized must exist before subsequent order events. Tests that truncate tables must respect reverse ordering.

**Redis key naming convention** → `redis/mod.rs:get_stream_key()`
Keys follow `{trader_key}:{collection}:{identifier}`. Index keys use `:index:` delimiter. Custom data keys use `custom:{ts_init_020}:{uuid}`. Stream key construction depends on `MessageBusConfig` settings (prefix, instance ID inclusion) — changing config breaks key compatibility with existing data.

**Redis minimum version 6.2.0** → `redis/mod.rs:create_redis_connection()`
Connection setup validates the server version. Earlier versions lack required commands.

**Schema bootstrapping** → `sql/pg.rs:init_postgres()`
Executes SQL files from `/schema/sql/` in fixed order: `types.sql` → `functions.sql` → `partitions.sql` → `tables.sql`. Uses regex to split plpgsql statements correctly (not naive semicolon splitting).

## Integration

- **Downstream**: `crates/pyo3/` aggregates Python bindings; `crates/cli/` uses `postgres` feature for DB init/drop commands
- **Trait source**: `CacheDatabaseAdapter` and `MessageBusDatabaseAdapter` defined in `nautilus-common`
- **Schema files**: Repository root `/schema/sql/` — not inside this crate
- **Integration tests**: Require external services (PostgreSQL:5432, Redis:6379), Linux-only, use `serial_test` to prevent concurrent access
