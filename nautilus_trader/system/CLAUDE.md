# nautilus_trader/system/

System orchestration -- the kernel that assembles and wires all platform components. Pure dependency injection: reads config, instantiates components, connects them via MessageBus endpoints, manages startup/shutdown lifecycle. Contains NO business logic.

## Files

- → `config.py:NautilusKernelConfig` -- frozen config declaring every subsystem
- → `kernel.py:NautilusKernel` -- builder that wires config to concrete components

## Kernel Assembly Order

The kernel assembles in strict order at `kernel.py`. Understanding this order is critical for debugging startup failures:

1. MessageBus database (Redis Streams, if configured)
2. Cache database (Redis only)
3. MessageBus + Cache + Clock + Logger
4. Portfolio (subscribes to order/position events)
5. Data Engine (environment-gated: `DataEngineConfig` for backtest, `LiveDataEngineConfig` for live)
6. Risk Engine (same gating pattern)
7. Execution Engine (same gating pattern)
8. Order Emulator
9. Trader (top-level orchestrator)
10. Controller, Streaming Writer, Data Catalogs
11. Actors and Strategies (registered last)

## Non-Obvious Behaviors

**load_state default discrepancy** → `config.py:122` -- the docstring says `default True` but the actual code default is `False`. The code is authoritative. Same for `save_state`.

**Database wiring is Redis-only** → `kernel.py:288-325` -- both MessageBus and Cache databases hard-validate that `type == "redis"`. Any other type raises `ValueError`. `CachePostgresAdapter` exists in `cache/adapter.py` but is never imported or used by the kernel.

**Environment gating** → `kernel.py:369-459` -- DataEngine, RiskEngine, and ExecEngine each have separate config types for backtest vs live. The kernel validates the config type matches the environment and raises `InvalidConfiguration` on mismatch. This is the enforcement point for backtest/live code path sharing.

**Streaming Writer is opt-in** → `kernel.py:502-505` -- only created when `config.streaming` is provided. Writes Feather files with rotation, registered as MessageBus subscriber.

## Config Inheritance

Three configs inherit from `NautilusKernelConfig`:

| Config | Environment | Key Difference |
|--------|------------|----------------|
| `BacktestEngineConfig` | BACKTEST | Pre-sets a `CacheConfig(drop_instruments_on_reset=False)` |
| `TradingNodeConfig` | LIVE | Legacy v1 Cython path |
| `LiveNodeConfig` | LIVE | New v2 Rust-native path (`crates/system/`) |

## Module Boundaries

- **Upstream**: `config/` (config classes), `common/` (MessageBus, Clock, Logger), `cache/` (Cache, adapters)
- **Downstream**: Assembles everything -- `data/`, `execution/`, `risk/`, `portfolio/`, `trading/`, `persistence/`, `live/`
- **Rust counterpart**: `crates/system/` contains `NautilusKernelBuilder` for Rust-native components (used by `LiveNode`)

## Conventions

- One-shot builder: `__init__` creates and wires everything. No re-configuration after construction.
- Creation order matters: MessageBus and Cache must exist before engines; Portfolio must exist before RiskEngine (receives `PortfolioFacade`).
- The kernel does NOT start components -- it only creates and registers them. Starting is delegated to `Trader` or `BacktestEngine`.