# crates/system/

System-level orchestration -- the Rust kernel that assembles and wires all platform components. Counterpart to `nautilus_trader/system/kernel.py` but for the Rust-native path (used by `LiveNode` v2).

## Architecture

- `builder.rs:NautilusKernelBuilder` — Fluent builder for dependency injection; all subsystems default to `None`, must be explicitly provided
- `kernel.rs:NautilusKernel` — Assembled runtime; orchestrates boot → run → seal lifecycle
- `config.rs:KernelConfig` — Rust-side config structs mirroring Python `NautilusKernelConfig`
- `event_store.rs:KernelEventStore` — Trait defining the integration seam between kernel and `crates/event_store/`
- `trader.rs:Trader` — Top-level lifecycle manager for strategies and actors

## Key Design Decisions

**Builder pattern over config-driven** → `builder.rs:NautilusKernelBuilder`
The Rust kernel uses a fluent builder API instead of a frozen config class. This provides compile-time validation and explicit dependency declaration. Every subsystem is opt-in.

**State persistence defaults differ from Python**: `load_state` and `save_state` default to `true` in the Rust builder, but `false` in Python `NautilusKernelConfig`. Rust path is designed for live trading where state persistence matters; Python path defaults to transient operation.

**Event store is optional** → `kernel.rs` exposes `event_store()` as `Option`. Not wired by default; concrete implementation from `crates/event_store/` is injected via `with_event_store()`.

**No default cache database**: `cache_database: None` means pure in-memory unless explicitly provided (matching Python behavior).

## Lifecycle: Boot → Run → Seal

1. **Boot**: Initialize all components in dependency order
2. **Run**: Process events through the message bus
3. **Seal**: Gracefully shut down, persisting state if configured

## Relationship to Python Kernel

Python `system/kernel.py` uses config-driven assembly (`NautilusKernelConfig` -> `NautilusKernel.__init__`), consumed by `BacktestEngine` and legacy `TradingNode`. Rust `crates/system/` uses builder-pattern assembly (`NautilusKernelBuilder::build()`), consumed by `LiveNode` (v2 Rust-native). The `load_state` default differs: `False` in Python, `True` in Rust (live trading wants persistence).
