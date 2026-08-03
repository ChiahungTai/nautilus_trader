# nautilus_trader/common/

Component/Actor/MessageBus foundation -- the platform's infrastructure layer that all trading components build on.

## Architecture

Inheritance chain: `Component` (FSM lifecycle) → `Actor` (data subscriptions) → `Strategy` (in `trading/`). Everything here is Cython (.pyx/.pxd) for performance-critical paths, with pure Python for utilities and configuration.

## Rust/Cython/Python Boundary

- **Rust (FFI)**: Clock timer internals, logging subsystem, `ComponentState`/`ComponentTrigger` enums, topic pattern matching. Defined in `nautilus_trader/core/rust/common.pxd` -- auto-generated, never edit.
- **Cython (.pyx)**: `Component`, `Actor`, `MessageBus`, `Clock`, `Logger`, `OrderFactory`, ID generators, `Throttler`. These are the hot paths.
- **Pure Python (.py)**: `InstrumentProvider`, `ActorExecutor`, `SecureString`, `TopicCache`, config dataclasses.

**Dual logging path**: `LOGGING_PYO3` flag causes `Logger` to check which runtime (Cython FFI vs PyO3) initialized the system on every log call.

## Component Lifecycle FSM

`Component` → `component.pyx:Component` owns a `FiniteStateMachine` with hardcoded `_COMPONENT_STATE_TABLE`. All public lifecycle methods (`start`, `stop`, `resume`, `reset`, `dispose`, `degrade`, `fault`) are non-overridable template methods that: trigger FSM transition → call user-overridable hook (`_start`, `_stop`, etc.) → complete transition → publish `ComponentStateChanged` event.

**Key invariants**:
- Hook exceptions are logged and re-raised, leaving the component stuck in the transitory state (not rolled back).
- `DISPOSED` and `FAULTED` are terminal one-way doors. `FAULTED` is idempotent.
- Initialization is implicit: passing a `MessageBus` to constructor triggers `_initialize()` immediately; otherwise component sits in `PRE_INITIALIZED` until `_change_msgbus()` is called during trader registration.

## Clock System

Two concrete clocks backed by Rust:
- **`TestClock`** → `component.pyx:TestClock`: Deterministic, manually advanced. `advance_time()` returns sorted `TimeEventHandler` list for synchronous backtest processing.
- **`LiveClock`** → `component.pyx:LiveClock`: Monotonically increasing system time. Timer callbacks fire via Rust-held `PyObject*` pointers.

**GC cycle risk**: Rust holds `PyObject*` references invisible to Python GC. `cancel_default_handler()`, `cancel_callbacks()`, `cancel_timers()` exist explicitly to break these cycles during disposal.

**Global registry**: `_COMPONENT_CLOCKS` maps `UUID4` instance IDs to clock lists, used by `BacktestEngine` to advance all component clocks in sync.

## Actor

`Actor` → `actor.pyx:Actor` extends `Component` with data subscriptions, handlers, request/response pattern, state persistence (`on_save`/`on_load`), and executor integration (`run_in_executor`).

**Convention**: When adding a new data subscription type to `Actor`, you must also add the corresponding topic generator in `TopicCache` → `data_topics.pyx:TopicCache`. Topic strings follow `{historical.}data.{type}.{venue}.{symbol}` pattern.

The `handle_*` methods (called by engines) dispatch to user-overridable `on_*` hooks AND feed registered `Indicator` instances -- dual consumers per event.

## MessageBus

`MessageBus` → `component.pyx:MessageBus` supports three patterns:
1. **Pub/Sub**: topics with `*`/`?` wildcards via Rust's `is_matching_ffi`. Subscriptions resolved lazily and cached in `_patterns`.
2. **Req/Rep**: correlation IDs in `_correlation_index` route responses back to requester.
3. **Point-to-point**: `register(endpoint, handler)` / `send(endpoint, msg)`.

**Not thread-safe** -- must be called from event loop thread only.

Optional Redis backing via `nautilus_pyo3.RedisMessageBusDatabase`. The `_publishable_types` tuple controls which message types are serialized externally; populated from `nautilus_trader/serialization/base.py`'s `_EXTERNAL_PUBLISHABLE_TYPES` at init time.

## OrderFactory and ID Generators

`OrderFactory` → `factories.pyx:OrderFactory` delegates to internal generators that embed clock UTC datetime for human-readability and collision avoidance. `PositionIdGenerator` appends `F` for flipped positions.

## Module Boundaries

- **Downstream**: `trading/strategy.pyx` inherits `Actor`. `data/`, `execution/`, `risk/` all consume `MessageBus`, `Clock`, `Logger`, `Component`.
- **Upstream**: depends on `model/` (identifiers, orders, data types), `core/` (FSM, UUID, Rust FFI), `cache/` (CacheFacade), `portfolio/` (PortfolioFacade).

## Conventions

- Cython `cdef`/`cpdef` methods are internal fast path; public `def` methods are user-facing API.
- `Condition` assertions → `core/correctness.pyx` raise `ValueError`/`TypeError` immediately for all precondition checks.
- Logger name is set to component name (not class name): `self._log = Logger(name=component_name)`.
- Modifying `.pyx` class signatures requires updating the corresponding `.pxd` in lockstep.