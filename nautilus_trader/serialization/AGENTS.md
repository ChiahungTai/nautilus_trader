# nautilus_trader/serialization/

Serialization backends for the platform. Three formats serve different purposes: MsgSpec (msgpack/JSON) for database persistence, Arrow for Parquet data catalog, and Cap'n Proto/SBE for wire-level transport (Rust only).

## Three-Format Design Rationale

| Format | Why It Exists | Language |
|--------|--------------|----------|
| **MsgSpec** | Cache/MessageBus DB persistence; global type registries dispatch ~60 types | Cython |
| **Arrow** | Parquet catalog read/write; Rust-defined tick types bypass Python entirely | Python + Rust delegation |
| **Cap'n Proto / SBE** | Zero-copy wire format for high-throughput market data | Rust only |

Cap'n Proto wire format is **not yet stable across releases** -- do not depend on binary compatibility.

## MsgSpec Serializer

`MsgSpecSerializer` → `serializer.pyx:MsgSpecSerializer`

- Encoding choice: `msgspec.msgpack` (default) or `msgspec.json` -- set at construction
- Dispatches via global registries in `base.pyx`: `_OBJECT_TO_DICT_MAP` and `_OBJECT_FROM_DICT_MAP`
- Timestamp handling: `timestamps_as_str` and `timestamps_as_iso8601` flags control uint64 ↔ string conversion (not obvious from API alone)
- External types: `register_serializable_type()` extends the registries at runtime

## Arrow Serializer

`ArrowSerializer` → `arrow/serializer.py:ArrowSerializer`

### Rust vs Python Serialization Boundary

This is the key non-obvious design decision:

1. **Rust-defined tick types** (`OrderBookDelta`, `QuoteTick`, `TradeTick`, `Bar`, `MarkPriceUpdate`): No Python encoder. Delegated to `nautilus_pyo3.*_to_arrow_record_batch_bytes()`. Price/Quantity fields use `FixedSizeBinary` (not float) to preserve fixed-point precision.

2. **Dict-based types** (events, instruments): Generic path using `make_dict_serializer()` / `make_dict_deserializer()` from `arrow/schema.py`. Calls `to_dict()` / `from_dict()` on each object.

3. **Custom implementations** in `arrow/implementations/`: `AccountState` (flattens balance/margin rows), `OrderInitialized`/`OrderFilled` (JSON-encodes complex fields), 16 instrument subclasses, component events.

### Connection to Persistence

Write path: `catalog.write_data()` → `ArrowSerializer.serialize_batch()` → `pa.Table` → Parquet

Read path is a **dual backend** (not obvious):
- **Rust** (`DataBackendSession`): DataFusion SQL queries against Parquet for built-in tick types
- **PyArrow**: Parquet → `pa.Table` → `ArrowSerializer.deserialize()` for everything else

Wranglers (`persistence/wranglers_v2.py`) bridge Rust Arrow output to Python objects.

## Module Boundaries

- **Upstream**: `model/` (all types being serialized), `core/` (UUID, nautilus_pyo3)
- **Downstream**: `persistence/` (Parquet catalog uses Arrow), `cache/` (Redis backing uses MsgSpec), `common/` (MessageBus DB uses MsgSpec)
- **External extension**: `register_serializable_type()` (MsgSpec) and `register_arrow()` (Arrow) allow external types
- **Rust counterpart**: `crates/serialization/` -- Arrow, Cap'n Proto (`schemas/capnp/`), SBE backends