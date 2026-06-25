# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
FOREX_5DECIMAL_TICK_SCHEME = FixedTickScheme(name='FOREX_5DECIMAL', price_precision=5, min_tick=Any, max_tick=Any)
FOREX_3DECIMAL_TICK_SCHEME = FixedTickScheme(name='FOREX_3DECIMAL', price_precision=3, min_tick=Any, max_tick=Any)

class FixedTickScheme(Any):
    """
    Represents a fixed precision tick scheme such as for Forex or Crypto.

    Parameters
    ----------
    name : str
        The name of the tick scheme.
    price_precision: int
        The instrument price precision.
    min_tick : Price
        The minimum possible tick `Price`.
    max_tick: Price
        The maximum possible tick `Price`.
    increment : float, optional
        The tick increment.

    Raises
    ------
    ValueError
        If `name` is not a valid string.
    """
    price_precision: int
    increment: Any

    def __init__(self, name: str, price_precision: int, min_tick: Any, max_tick: Any, increment: float | None | None=None) -> None:
        ...

    def next_ask_price(self, value: float, n: int=0) -> Any:
        """
        Return the price `n` ask ticks away from value.

        If a given price is between two ticks, n=0 will find the nearest ask tick.

        Parameters
        ----------
        value : double
            The reference value.
        n : int, default 0
            The number of ticks to move.

        Returns
        -------
        Price

        """

    def next_bid_price(self, value: float, n: int=0) -> Any:
        """
        Return the price `n` bid ticks away from value.

        If a given price is between two ticks, n=0 will find the nearest bid tick.

        Parameters
        ----------
        value : double
            The reference value.
        n : int, default 0
            The number of ticks to move.

        Returns
        -------
        Price

        """