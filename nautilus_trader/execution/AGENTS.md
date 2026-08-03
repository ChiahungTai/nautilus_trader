# Execution Module

Order execution engine: routes commands to clients, processes order events, manages position lifecycle, and provides local order emulation and custom execution algorithms.

All performance-critical components are Cython (.pyx/.pxd). Pure Python is limited to `config.py` and `reports.py`.

## Architecture — Fan-in Fan-out

Strategies submit `TradingCommand` messages through the engine, which routes to `ExecutionClient` adapters; clients stream `OrderEvent` messages back through the engine, which applies state transitions and publishes to the message bus.

Routing chain (each stage is a gate, not a fork):

```
Strategy → RiskEngine → ExecAlgorithm? → OrderEmulator? → ExecutionEngine._execute_command() → ExecutionClient (adapter)
```

- ExecAlgorithm intercepts and can spawn child orders (TWAP/VWAP slicing)
- OrderEmulator holds stop/conditional orders locally until trigger, then releases as Market/Limit
- External clients (configured in `ExecEngineConfig.external_clients`) bypass local execution entirely — commands are published to message bus topics only

## Command Routing Priority → `engine.pyx:ExecutionEngine._find_client_for_command`

1. Explicit `client_id` on the command
2. `account_id.get_issuer()` mapped to registered client
3. Venue-based routing via `_routing_map[venue]`
4. Default client fallback

## OMS Types (Position Management)

The engine supports two OMS modes, resolved per-strategy with fallback to client's `oms_type`:

- **NETTING**: single position per `(instrument_id, strategy_id)`. Position ID is `{instrument_id}-{strategy_id}`. Reopening closed positions is valid (snapshot then reopen).
- **HEDGING**: multiple concurrent positions per instrument. Position IDs from `PositionIdGenerator` (auto-incrementing per strategy). Each order gets its own position.

Position flips on fill: engine splits the fill into two — close original position, open new in opposite direction with remaining quantity. Commission is split proportionally.

## Order Emulation → `emulator.pyx:OrderEmulator`

Purpose: handle stop/conditional orders locally instead of sending to exchange. Useful when venue does not support the order type, or for backtesting fidelity.

Key differences from exchange stop orders:
- Orders held in local `MatchingCore` instances, monitored against streaming market data
- When triggered, original order transformed to `MarketOrder` or `LimitOrder` and released as new submission
- Emulation trigger types: `DEFAULT`/`BID_ASK` (subscribe to quotes), `LAST_PRICE` (subscribe to trades)
- Trailing stop recalculation via `trailing.pyx:TrailingStopCalculator` on each price update
- Supports synthetic instruments as trigger sources
- On restart, reactivates emulated orders from cache (re-checks parent order and position states)

## Execution Algorithms → `algorithm.pyx:ExecAlgorithm`

Base class extends `Actor` (has access to cache, msgbus, clock, portfolio). When a command has an `exec_algorithm_id`, it routes to the registered `ExecAlgorithm` instead of directly to a client.

Key mechanism: `spawn_market()`/`spawn_limit()`/`spawn_market_to_limit()` create child orders from a primary order. Primary order's quantity can be reduced to avoid over-execution. Child orders linked via `exec_spawn_id`.

## Conventions

- Event generation in `ExecutionClient` subclasses follows `generate_*` pattern — creates event, applies to order, sends to engine via `_send_order_event`
- Position events are buffered in `_pending_position_events` during fill processing and published after the fill event to prevent recursion
- Overfill detection: `allow_overfills=True` logs warning and continues; `False` (default) rejects the fill
- Leg fills (spread order components with `-LEG-` in ID) are handled without requiring a corresponding order in cache
- `manage_own_order_books` mode maintains `nautilus_pyo3.OwnOrderBook` instances per instrument for order book tracking from commands/events
- State transitions enforced per-order-type FSM in Rust (`model/orders`). `order.apply(event)` may raise `InvalidStateTrigger` for illegal transitions (handled in `_apply_event_to_order`)

## Navigation

| Concept | Location |
|---------|----------|
| Central router, position lifecycle | `engine.pyx:ExecutionEngine` |
| Abstract adapter base | `client.pyx:ExecutionClient` |
| Custom algo execution | `algorithm.pyx:ExecAlgorithm` |
| Local stop/conditional emulation | `emulator.pyx:OrderEmulator` |
| Order state machine helper | `manager.pyx:OrderManager` |
| Matching engine (backtest/emulation) | `matching_core.pyx:MatchingCore` |
| Trailing stop price calc | `trailing.pyx:TrailingStopCalculator` |
| Command types (SubmitOrder, etc.) | `messages.pyx` |
| Config dataclasses | `config.py` |
| Reconciliation data structures | `reports.py` |

## Event Publishing Topics

- `events.order.{strategy_id}` — all order events for a strategy
- `events.position.{strategy_id}` — position opened/changed/closed events
- `events.fills.{instrument_id}` — fill events for an instrument
- `events.cancels.{instrument_id}` — cancel events for an instrument
- `commands.trading.{client_id}` — commands for external clients

## Module Boundaries

- **Depends on**: `model/orders` (order types and FSM), `model/events`, `model/identifiers`, `model/objects`, `model/position`, `cache`, `common/component`, `portfolio/base` (read-only), `accounting/accounts`
- **Consumed by**: `trading/strategy` (submits orders), adapters (implement `ExecutionClient`), backtest engine
- **Does NOT depend on**: any specific exchange adapter or data feed