# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class MatchingCore:
    """
    Provides a generic order matching core.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the matching core.
    price_increment : Price
        The minimum price increment (tick size) for the matching core.
    trigger_stop_order : Callable[[Order], None]
        The callable when a stop order is triggered.
    fill_market_order : Callable[[Order], None]
        The callable when a market order is filled.
    fill_limit_order : Callable[[Order], None]
        The callable when a limit order is filled.
    """
    bid_raw: Any
    ask_raw: Any
    last_raw: Any
    is_bid_initialized: bool
    is_ask_initialized: bool
    is_last_initialized: bool

    def __init__(self, instrument_id: Any, price_increment: Any, trigger_stop_order: Callable, fill_market_order: Callable, fill_limit_order: Callable):
        ...

    @property
    def instrument_id(self) -> Any:
        """
        Return the instrument ID for the matching core.

        Returns
        -------
        InstrumentId

        """

    @property
    def price_precision(self) -> int:
        """
        Return the instruments price precision for the matching core.

        Returns
        -------
        int

        """

    @property
    def price_increment(self) -> Any:
        """
        Return the instruments minimum price increment (tick size) for the matching core.

        Returns
        -------
        Price

        """

    @property
    def bid(self) -> Any | None:
        """
        Return the current bid price for the matching core.

        Returns
        -------
        Price or ``None``

        """

    @property
    def ask(self) -> Any | None:
        """
        Return the current ask price for the matching core.

        Returns
        -------
        Price or ``None``

        """

    @property
    def last(self) -> Any | None:
        """
        Return the current last price for the matching core.

        Returns
        -------
        Price or ``None``

        """

    def get_order(self, client_order_id: Any) -> Any:
        ...

    def order_exists(self, client_order_id: Any) -> bool:
        ...

    def get_orders(self) -> list:
        ...

    def get_orders_bid(self) -> list:
        ...

    def get_orders_ask(self) -> list:
        ...

    def update_price_increment(self, price_increment: Any) -> None:
        """
        Update the price increment (tick size) for the matching core.

        Parameters
        ----------
        price_increment : Price
            The new minimum price increment (tick size).

        """

    def reset(self) -> None:
        ...

    def add_order(self, order: Any) -> None:
        ...

    def delete_order(self, order: Any) -> None:
        ...

    def iterate(self, timestamp_ns: int) -> None:
        ...

    def match_order(self, order: Any, initial: bool=False) -> None:
        """
        Match the given order.

        Parameters
        ----------
        order : Order
            The order to match.
        initial : bool, default False
            If this is an initial match.

        Raises
        ------
        TypeError
            If the `order.order_type` is an invalid type for the core (e.g. `MARKET`).

        """

    def match_limit_order(self, order: Any) -> None:
        ...

    def match_stop_market_order(self, order: Any) -> None:
        ...

    def match_stop_limit_order(self, order: Any, initial: bool) -> None:
        ...

    def match_market_if_touched_order(self, order: Any) -> None:
        ...

    def match_limit_if_touched_order(self, order: Any, initial: bool) -> None:
        ...

    def match_trailing_stop_limit_order(self, order: Any, initial: bool) -> None:
        ...

    def match_trailing_stop_market_order(self, order: Any) -> None:
        ...

    def set_fill_limit_inside_spread(self, value: bool) -> None:
        ...

    def is_limit_fillable(self, side: Any, price: Any) -> bool:
        ...

    def is_limit_marketable(self, side: Any, price: Any) -> bool:
        ...

    def is_stop_triggered(self, side: Any, trigger_price: Any) -> bool:
        ...

    def is_touch_triggered(self, side: Any, trigger_price: Any) -> bool:
        ...