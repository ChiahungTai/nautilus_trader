# nautilus_trader/config/

Thin package — the `__init__.py` re-exports config classes from each component's own module. The actual config definitions live with their components.

## Architecture

All configs inherit from `NautilusConfig` → `common/config.py:NautilusConfig` — a frozen msgspec Struct with `kw_only=True` and `forbid_unknown_fields=True`. One config class per component, all immutable after creation.

## Importable Config Pattern (config-driven instantiation)

Several configs store a `class_path` string (e.g., `"my_module:MyStrategy"`) for runtime resolution. The kernel resolves the path and instantiates the component:

| Config Class | Target Component | Location |
|-------------|-----------------|----------|
| `ImportableActorConfig` | Actors | `common/config.py` |
| `ImportableConfig` | Generic importable | `common/config.py` |
| `ImportableFactoryConfig` | Client factories | `common/config.py` |
| `ImportableStrategyConfig` | Strategies | `trading/config.py` |
| `ImportableControllerConfig` | Trader controller | `trading/config.py` |
| `ImportableExecAlgorithmConfig` | Exec algorithms | `execution/config.py` |

## Non-Obvious Constraints

- **DatabaseConfig** → `common/config.py:DatabaseConfig` — only `type="redis"` is supported. PostgreSQL adapter (`CachePostgresAdapter`) exists but has no config path.
- **Config classes are pure data** — no behavior, no dependencies on runtime components. This is by design: configs must be serializable and usable before the kernel boots.

## Module Boundaries

- **Upstream**: `common/` (NautilusConfig base), `model/` (TraderId, identifiers used in configs)
- **Downstream**: Every module imports its own config class — config is the most widely imported package
- **Each component owns its config** — `CacheConfig` is in `cache/config.py`, not here. This package is a re-export convenience.