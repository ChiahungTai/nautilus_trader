# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
import numpy as np
from nautilus_trader.model.objects import Price
from nautilus_trader.model.tick_scheme.base import TickScheme
TOPIX100_TICK_SCHEME: TieredTickScheme = ...

class TieredTickScheme(TickScheme):
    """
    Represents a tick scheme where tick levels change based on price level, such as various financial exchanges.

    Parameters
    ----------
    name : str
        The name of the tick scheme.
    tiers : list[tuple(start, stop, step)]
        The tiers for the tick scheme. Should be a list of (start, stop, step) tuples.
    max_ticks_per_tier : int, default 100
        The maximum number of ticks per tier.

    Raises
    ------
    ValueError
        If `name` is not a valid string.
    """
    ticks: np.ndarray

    def __init__(self, name: str, tiers: list, price_precision: int, max_ticks_per_tier: int=100) -> None:
        ...

    def find_tick_index(self, value: float) -> int:
        ...

    def next_ask_price(self, value: float, n: int=0) -> Price:
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

    def next_bid_price(self, value: float, n: int=0) -> Price:
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