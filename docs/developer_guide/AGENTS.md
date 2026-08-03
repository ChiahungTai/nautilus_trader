# Developer Guide

Contributor-facing documentation for NautilusTrader. The project uses a **Rust core with Python bindings (PyO3)** architecture.

## Navigation

| You are... | Read this |
|---|---|
| Setting up a dev environment | [environment_setup.md](environment_setup.md) |
| Writing Rust code | [rust.md](rust.md) |
| Writing Python code | [python.md](python.md) |
| Writing or modifying tests | [testing.md](testing.md) |
| Adding a new data type | [testing.md](testing.md) -- six test layers every new type must cover |
| Working across the FFI boundary | [ffi.md](ffi.md) |
| Building a venue adapter | [adapters.md](adapters.md) |
| Adapter acceptance tests | [spec_data_testing.md](spec_data_testing.md), [spec_exec_testing.md](spec_exec_testing.md) |
| Test data fixtures | [test_datasets.md](test_datasets.md) |
| Writing documentation | [docs.md](docs.md) |
| Benchmarking Rust | [benchmarking.md](benchmarking.md) |
| Cutting a release | [releases.md](releases.md) |
| Formatting / commit messages | [coding_standards.md](coding_standards.md) |
| Architectural invariants | [design_principles.md](design_principles.md) |

## Cross-Cutting Conventions

Violating these breaks CI or causes subtle bugs.

### Error handling chain (Rust)

Layered approach, not catch-all `Result`:

1. **Type system** -- encode what the compiler can prove.
2. **`check_*` from `nautilus_core::correctness`** -- public API preconditions. Pair `new_checked()` (returns `CorrectnessResult`) with `new()` (panics via `.expect_display(FAILED)`).
3. **`debug_assert!`** -- internal invariants, stripped in release. Prefix messages with `Invariant:`.
4. **`assert!`** -- always-on, soundness-critical or unsafe preconditions.

Do NOT use `debug_assert!` for public API validation (correctness module's job). Do NOT use `assert!` where `debug_assert!` suffices (release builds silently skip).

### Hash collection decision tree (Rust)

Follow in order:

1. Iteration order feeds observable state (events on message bus, ordered Vecs, seeded RNG)? **`IndexMap`/`IndexSet`**.
2. Lookup-only hot path? **`AHashMap`/`AHashSet`**.
3. Concurrent access needed? **`DashMap`** (not `Arc<AHashMap>` with mutation).
4. Non-critical, simple code? Standard `HashMap`/`HashSet`.

### FFI memory contract

Violations cause double-free or memory leaks:

- **CVec**: Rust `Vec<T>` converts with `into()` (leaks to foreign). Foreign calls the **type-specific** `vec_drop_*` helper exactly once. No generic `cvec_drop` exists.
- **Capsules**: Always `PyCapsule::new_with_destructor` (never `PyCapsule::new(..., None)`). Destructor reconstructs the original `Box`/`Vec` and lets it drop.
- **`*_API` wrappers**: Every `*_new` must have a matching `*_drop`. New code uses PyCapsule with destructors; legacy Cython uses `__del__`/`__dealloc__`.
- All FFI functions wrapped in `abort_on_panic` to prevent panic unwinding across `extern "C"`.

### Adapter runtime pattern (Rust)

Adapter crates: use `get_runtime().spawn()` (from `nautilus_common::live::get_runtime`), NOT `tokio::spawn()`. The latter panics from Python threads (relies on thread-local Tokio context). Test code with `#[tokio::test]` is exempt.

### PyO3 naming (Rust)

Rust functions exposed to Python: prefix `py_*` in Rust, `#[pyo3(name = "...")]` maps to clean Python name. Every `#[pyclass]`/`#[pymethods]`/`#[pyfunction]` needs a matching `pyo3_stub_gen` annotation. Regenerate stubs: `make py-stubs-v2`.

### Test style

- **Python**: pytest free functions, no classes. Use `@pytest.fixture` and `@pytest.mark.parametrize`. Import from `nautilus_trader.model`, not `nautilus_trader.core.nautilus_pyo3`.
- **Rust**: Use `#[rstest]` (not `#[test]`). Property tests: separate `mod property_tests` with `prop_` prefix. Test specs: `bon::Builder` with `finish_fn = into_spec`.
- **Async waiting**: `await eventually(...)` (Python), `wait_until_async(...)` (Rust) -- not arbitrary sleeps.
- **Mocks**: Prefer hand-written stubs over `MagicMock`. Avoid mocking the object under test.

### Shell scripts

Portable across Linux and macOS. `#!/usr/bin/env bash`. Avoid bash 4+ features in user-facing scripts (macOS ships 3.2). CI scripts (`scripts/ci/*`) may use bash 4+ and GNU tools.

## Pre-commit Hooks

Many Rust conventions are enforced by pre-commit. If `prek` fails, the hook name tells you what to fix:

| Hook | What it enforces |
|---|---|
| `check_anyhow_usage.sh` | Fully qualify `anyhow::bail!`, `anyhow::anyhow!`, `anyhow::Result<T>` |
| `check_logging_macro_usage.sh` | Use `log::debug!` etc., not bare `debug!` |
| `check_pyo3_conventions.sh` | `py_` prefix on PyO3 functions |
| `check_testing_conventions.sh` | `#[rstest]` over `#[test]` |
| `check_tokio_usage.sh` | `get_runtime().spawn()` in adapter crates |
| `check_error_conventions.sh` | Error handling patterns |
| `check_copyright_year.sh` | Copyright headers must include current year |
| `check-dst-conventions` | `IndexMap`/`IndexSet` in DST-load-bearing files |

## Important Caveats

- **v1 vs v2 test suites**: `tests/` (v1, Cython) and `python/tests/` (v2, PyO3) are separate. Use `make pytest` vs `make pytest-v2`. Do not mix.
- **Panic paths in v2 tests**: Do NOT write `pytest.raises(BaseException)` to catch Rust panics -- debug builds may catch them but release builds abort the interpreter. Isolate in a subprocess or verify signatures instead.
- **`make pytest-v2` isolation**: The Makefile target isolates certain test modules in separate processes to avoid global Rust state conflicts. Always use `make pytest-v2`, never invoke pytest directly.
- **Message immutability**: Once created, messages (events, commands, requests, responses) must not be mutated. Underpins determinism, replay, concurrency safety, and auditability. See [design_principles.md](design_principles.md).
- **LiveNode vs TradingNode**: New adapter code should use `nautilus_trader.live.LiveNode`. `nautilus_trader.live.node.TradingNode` is legacy v1/Cython.

## Build Commands

| Command | Purpose |
|---|---|
| `make build-debug` | Debug build (fast iteration) |
| `make build-debug-v2` | Debug PyO3 extension for `python/tests/` |
| `make pytest` | Run v1 legacy tests (`tests/`) |
| `make pytest-v2` | Run v2 PyO3 tests (`python/tests/`) |
| `make cargo-test` | Rust tests via nextest |
| `make test-performance` | Performance/benchmark tests |
| `make pre-commit` | Run all pre-commit checks |
| `make py-stubs-v2` | Regenerate Python type stubs |
| `make format` | Run rustfmt + ruff |
