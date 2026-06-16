# nautilus_trader/risk/

Pre-trade risk engine -- every trading command passes through here before reaching execution.

## Architecture

RiskEngine sits between strategies and execution as a gateway/interceptor:

```
Strategy → TradingCommand → MessageBus → RiskEngine.execute → (approved) → ExecEngine.execute
                                                   → (denied)   → ExecEngine.process (OrderDenied)
```

## TradingState FSM

Three states control order flow -- ACTIVE (all pass), REDUCING (only position-reducing), HALTED (all non-cancel denied). Transitions publish `TradingStateChanged` on `events.risk` topic.

## Risk Checks (execution order matters)

1. TradingState -- HALTED denies everything except cancels
2. Throttle -- independent rate limiters for submit and modify
3. Instrument existence
4. Price/quantity precision -- validated against instrument settings
5. Min/max notional -- per-order and instrument-level bounds
6. Free balance -- cash accounts check notional; margin accounts check initial margin
7. Reduce-only -- in REDUCING state, verifies order would not increase position
8. Position-reducing sell optimization -- skips balance check for sells that reduce long positions
9. Min/max quantity bounds
10. Trailing stop trigger price -- computed from market data if not set

## Design Decisions

- **Bypass mode** (`config.py:RiskEngineConfig` `bypass=True`): Skips ALL checks except reduce-only. Designed for backtesting where pre-trade risk is unnecessary. Logs RED warning on startup.
- **Order list atomicity**: Any order in an `OrderList` fails -> entire list denied with individual `OrderDenied` per order.
- **Quote quantity orders** (crypto): `min_quantity`/`max_quantity` checks skipped (venue authoritative), base quantity estimated from market price.
- **Negative prices**: Futures/option spreads can have negative prices; regular instruments cannot.
- **Multi-account**: Orders grouped by `account_id`, checked independently.
- **Dual throttler**: Submit and modify have independent rate limiters with separate success/failure handlers.

## Account Type Differentiation

| Account Type | Balance Check | Special Handling |
|-------------|--------------|-----------------|
| Cash | Full notional vs free balance | `allow_borrowing` for spot margin |
| Margin | Initial margin vs free margin | Cumulative margin tracking across orders |
| Betting | Balance-locked liability | Dedicated calculation path |

## Connections

- **Cache** -- read-only queries for instrument lookup, order/position state, account balances, last market price
- **Portfolio** -- `PortfolioFacade.is_net_long()`/`is_net_short()` for REDUCING state checks
- **ExecEngine** -- approved commands via `"ExecEngine.execute"`, denied via `"ExecEngine.process"`
- **MessageBus** -- subscribes to `events.order.*`, `events.position.*`; publishes `TradingStateChanged`

## Navigation

| Concept | Location |
|---------|----------|
| Risk engine | `engine.pyx:RiskEngine` |
| Position sizing | `sizing.pyx:PositionSizer`, `sizing.pyx:FixedRiskSizer` |
| Config | `config.py:RiskEngineConfig` |

## Rust Counterpart

`crates/risk/` has an equivalent Rust implementation. Key difference: Rust uses a separate `risk_engine_queue_execute` endpoint to prevent re-entrancy (a synchronous `deny_order()` dispatching `OrderDenied` back into a strategy holding a mutable `RefCell` borrow would panic).