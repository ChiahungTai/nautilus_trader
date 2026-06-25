# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.backtest.engine import SimulatedExchange

class BacktestExecClient(Any):
    """
    Provides an execution client for the `BacktestEngine`.

    Parameters
    ----------
    exchange : SimulatedExchange
        The simulated exchange for the backtest.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache for the client.
    clock : TestClock
        The clock for the client.
    routing : bool
        If multi-venue routing is enabled for the client.
    frozen_account : bool
        If the backtest run account is frozen.
    allow_cash_borrowing : bool
        If cash accounts should allow borrowing (negative balances).
    """

    def __init__(self, exchange: SimulatedExchange, msgbus: Any, cache: Any, clock: Any, routing: bool=False, frozen_account: bool=False, allow_cash_borrowing: bool=False) -> None:
        ...

    def submit_order(self, command: Any) -> None:
        ...

    def submit_order_list(self, command: Any) -> None:
        ...

    def modify_order(self, command: Any) -> None:
        ...

    def cancel_order(self, command: Any) -> None:
        ...

    def cancel_all_orders(self, command: Any) -> None:
        ...

    def batch_cancel_orders(self, command: Any) -> None:
        ...