# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.indicators.base import Indicator

class SpreadAnalyzer(Indicator):
    """
    Provides various spread analysis metrics.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the tick updates.
    capacity : int
        The max length for the internal `QuoteTick` deque (determines averages).

    Raises
    ------
    ValueError
        If `capacity` is not positive (> 0).
    """
    instrument_id: Any
    capacity: int
    current: float
    average: float

    def __init__(self, instrument_id: Any, capacity: int) -> None:
        ...

    def handle_quote_tick(self, tick: Any) -> None:
        """
        Update the analyzer with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The tick for the update.

        Raises
        ------
        ValueError
            If `tick.instrument_id` does not equal the analyzers instrument ID.

        """