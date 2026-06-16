# Rust Workspace (crates/)

Production-grade Rust-native trading engine with deterministic event-driven architecture. Compiled into a single Python extension module (`nautilus_pyo3`) via PyO3, with C FFI headers for Cython integration.

## Why This Structure Exists

**Workspace shim crate** → `crates/lib.rs` — Exists solely to keep `crates/` a valid Cargo target, preventing Cargo from discarding incremental build artifacts when only the dependency graph changes. Exposes no public API.

**Centralized dependency management** — All dependency versions, ~120 clippy lints, and tool versions are pinned in root `Cargo.toml` under `[workspace.dependencies]`, `[workspace.lints.clippy]`, `[workspace.metadata.tools]`. Each crate inherits with `workspace = true`.

**`high-precision` feature** — Compile-time flag (not runtime) that switches `nautilus-model` and `nautilus-serialization` from 64-bit to 128-bit fixed-point. Propagates through adapters and is baked into C headers via `build.rs`.

**`debug-assertions = false` in dev profile** — Rust debug assertions trigger panics incompatible with Cython builds. The `test` profile re-enables them.

## The Three-Language Bridge

### Rust to Python (PyO3 path)

```
crates/{name}/src/python/  -->  crates/pyo3/src/lib.rs  -->  nautilus_trader._libnautilus
```

- Each crate defines its own `python` module with `#[pymodule]` + `#[pyclass]`/`#[pymethods]`
- `crates/pyo3/` is the aggregator: imports every crate's Python module, registers as submodules
- Built by maturin into single `nautilus_pyo3` extension
- `cython-compat` feature re-exports all submodule attributes at top level for Cython access

### Rust to Cython (C FFI path, 4 crates only)

```
crates/{name}/src/ffi/  -->  cbindgen  -->  nautilus_trader/core/includes/{name}.h
                                     -->  nautilus_trader/core/rust/{name}.pxd
```

Only `core`, `model`, `common`, `backtest` have FFI/cbindgen configs (confirmed by `cbindgen.toml` presence). `build.rs` generates both `.h` and `.pxd`. High-precision mode forwarded via `DEF HIGH_PRECISION` macro in `.pxd`.

### Navigation: Python Class to Rust Source

1. Identify the domain: `model` (events, orders, instruments), `execution`, `backtest`, etc.
2. Go to `crates/{domain}/src/python/` → find `#[pyclass]` or `#[pymethods]`
3. The Python binding wraps a Rust struct in `crates/{domain}/src/{submodule}/`
4. For Cython FFI types → `crates/{domain}/src/ffi/` + `nautilus_trader/core/rust/{domain}.pxd`

## Crate Dependency Flow

```
core (foundational types, no domain logic)
  |
  v
model (trading domain model)
  |
  +-- common / serialization / indicators
  |
  v
execution / data / portfolio / risk / analysis
  |
  v
backtest / live / trading
  |
  v
system (kernel, trader, controller)
  |
  v
adapters/* (exchange-specific implementations)
```

Dependency direction is strictly top-down. Circular dependencies between crates at the same level are forbidden.

## Crate Structure Convention

Every crate uses the same feature flags:

| Feature | Purpose |
|---------|---------|
| `python` | Enables `src/python/` — PyO3 bindings |
| `ffi` | Enables `src/ffi/` — C FFI exports via cbindgen |
| `extension-module` | Builds as Python extension module |
| `high-precision` | 128-bit value types (model, serialization, adapters) |

## Key Commands

| Command | Purpose |
|---------|---------|
| `cargo test -p nautilus-{name}` | Unit tests for a crate |
| `cargo nextest run --workspace` | All crate tests |
| `make clippy-fix` | Auto-fix clippy violations |
| `cargo run --bin python-stub-gen` | Regenerate Python type stubs |