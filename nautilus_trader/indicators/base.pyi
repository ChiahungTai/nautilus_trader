# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class Indicator:
    """
    The base class for all indicators.

    Parameters
    ----------
    params : list
        The initialization parameters for the indicator.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    name: str
    has_inputs: bool
    initialized: bool

    def __init__(self, params: list) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def handle_quote_tick(self, tick: Any) -> None:
        """Abstract method (implement in subclass)."""

    def handle_trade_tick(self, tick: Any) -> None:
        """Abstract method (implement in subclass)."""

    def handle_bar(self, bar: Any) -> None:
        """Abstract method (implement in subclass)."""

    def reset(self) -> None:
        """
        Reset the indicator.

        All stateful fields are reset to their initial value.
        """