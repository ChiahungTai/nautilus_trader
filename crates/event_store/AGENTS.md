# crates/event_store/

Append-only event sourcing -- the authoritative log of state-affecting messages (commands, events, venue reports). Provides crash recovery via tail replay, deterministic incident replay, and audit trails.

## Architecture

```
crates/event_store/src/
  backend/         -- EventStore trait + MemoryBackend (tests) + RedbBackend (production)
  kernel.rs        -- EventStoreSession: kernel boot integration
  capture/         -- Bus capture subsystem: adapter, encoders, registry
  writer/          -- Dedicated writer thread with batching + fail-stop
  reader/          -- EventStoreReader: range scans, snapshot replay plans
  replay.rs        -- Core recovery: restore_cache_snapshot_and_replay_tail
  snapshot.rs      -- SnapshotAnchor, content hash
  verifier/        -- Cross-checks stored indices vs projections
  manifest.rs      -- RunManifest, RunId, RunStatus FSM
  entry.rs / headers.rs / wire.rs  -- Entry types, metadata, wire format
```

## Design Decisions

- **Embedded DB over network DB** → `backend/redb.rs:RedbBackend` — append-only log needs local low-latency writes. Network round-trip would bottleneck. `redb` provides `Durability::Immediate` (fsync per write) without network overhead.

- **One `.redb` file per run** → `kernel.rs:EventStoreSession` — each kernel boot creates `<base>/<instance_id>/<run_id>.redb`. Crashed predecessors are detected and sealed. Enables crash recovery without data corruption.

- **Capture allow-list** → `capture/registry.rs:EncoderRegistry` — not every message bus message is captured. Registry controls which types enter the event store, keeping the log focused on state-affecting events (orders, fills, positions, account state).

- **Not wired by default** → wired via `NautilusKernelBuilder::with_event_store()`. Builder has `event_store_factory: None` unless explicitly provided. Most users (backtesters) do not need it; live trading nodes that need crash recovery must explicitly configure it.

## Kernel Boot Lifecycle → `kernel.rs:EventStoreSession`

Multi-step pipeline executed in order:

1. Scan for crashed predecessors (unsealed `.redb` files from previous runs)
2. Seal crashed runs as `CrashedRecovered` → `manifest.rs`
3. Open new run (fresh `.redb` file)
4. Block until `RunStarted` ack (system confirmation)
5. Seal on graceful stop as `Sealed`

Run status FSM: `Running` → `CrashedRecovered` (predecessor) / `Sealed` (graceful) / `Quarantined` (flagged for inspection).

## Crash Recovery → `replay.rs:restore_cache_snapshot_and_replay_tail`

Core recovery mechanism: loads a snapshot anchor, then replays all entries after the snapshot to restore current state. This is the only recovery path — no partial state reconstruction.

## System Integration

`KernelEventStore` trait (`crates/system/src/event_store.rs`) is the kernel-facing seam. `EventStoreConfig` controls `RetentionMode` and `RecoveryOutcome`.