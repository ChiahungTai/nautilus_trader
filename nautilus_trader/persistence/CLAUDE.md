# Persistence

Data storage and retrieval layer for backtesting. Pipeline: external data → DataFrames → Nautilus objects → queryable Parquet files.

## Data Flow (Backtesting Pipeline)

1. Load → `loaders.py:CSVTickDataLoader` / `ParquetTickDataLoader` → DataFrame
2. Wrangle → `wranglers_v2.py:*WranglerV2` → PyO3 Nautilus objects
3. Write → `catalog/parquet.py:ParquetDataCatalog.write_data()` → Parquet on disk
4. Query → `catalog/parquet.py:ParquetDataCatalog` → Nautilus objects

## Key Design Decisions

- **Wrangler V1 vs V2** → V2 (`wranglers_v2.py`, pure Python, PyO3) preferred. V1 (`wranglers.pyx`, Cython) kept only for bar preprocessing helpers (`preprocess_bar_data`, `calculate_bar_price_offsets`, `align_bid_ask_bar_data`).
- **Dual query backend** → `catalog/parquet.py:ParquetDataCatalog.query()` auto-selects: Rust/DataFusion for built-in tick/bar types (supports SQL `where`, cloud storage), PyArrow for everything else.
- **Singleton catalog** → `catalog/singleton.py` metaclass caches instances by constructor args. Reset with `clear_singleton_instances()`.

## Storage Layout & Conventions

- **Bar data is special-cased**: grouped by `bar_type` string (not `instrument_id`) as the directory identifier.
- **Filename encoding**: `{start_iso}-{end_iso}.parquet` — catalog parses filenames for interval filtering without reading file contents.
- **Custom data classes**: get `custom_` filename prefix; registerable for Rust backend via `_RUST_CUSTOM_DATA_TYPES`.
- **Filesystem abstraction**: `fsspec` throughout — supports local, S3, GCS, Azure, memory.

## Hard Constraints

- Data must be monotonically non-decreasing by `ts_init`. Catalog raises `ValueError` on violation.
- File intervals must be disjoint. Enforced during writes and after consolidation/deletion.
- **Not threadsafe** — `ParquetDataCatalog` must not be shared across threads.

## Navigation

| File | Core Class/Function | Design Note |
|------|-------------------|-------------|
| `catalog/parquet.py` | `ParquetDataCatalog` | Primary catalog; dual backend query |
| `catalog/base.py` | `BaseDataCatalog` | Abstract base with convenience query methods |
| `wranglers_v2.py` | `*WranglerV2` | Preferred; supports `from_arrow()`, `from_pandas()`, `from_schema()` |
| `wranglers.pyx` | Legacy wranglers | Bar preprocessing only reason to keep |
| `writer.py` | `StreamingFeatherWriter` | Live/backtest streams → Feather with file rotation |
| `loaders.py` | `CSVTickDataLoader`, `ParquetTickDataLoader` | DataFrame I/O + `InterestRateProvider` actor |
| `funcs.py` | Shared utilities | Class↔filename mapping, URI-safe IDs, PyArrow filter parsing |
| `config.py` | `DataCatalogConfig`, `StreamingConfig` | Frozen configs; `as_catalog()` produces catalog instances |
