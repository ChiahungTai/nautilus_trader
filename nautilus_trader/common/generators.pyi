# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class IdentifierGenerator:
    """
    Provides a generator for unique ID strings.

    Parameters
    ----------
    trader_id : TraderId
        The ID tag for the trader.
    clock : Clock
        The internal clock.
    """

    def __init__(self, trader_id: Any, clock: Any):
        ...

class ClientOrderIdGenerator(IdentifierGenerator):
    """
    Provides a generator for unique `ClientOrderId`(s).

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the generator.
    strategy_id : StrategyId
        The strategy ID for the generator.
    clock : Clock
        The clock for the generator.
    initial_count : int
        The initial count for the generator.
    use_uuids : bool, default False
        If UUID4's should be used for client order ID values.
    use_hyphens : bool, default True
        If hyphens should be used in generated client order ID values.

    Raises
    ------
    ValueError
        If `initial_count` is negative (< 0).
    """
    count: int
    use_uuids: bool
    use_hyphens: bool

    def __init__(self, trader_id: Any, strategy_id: Any, clock: Any, initial_count: int=0, use_uuids: bool=False, use_hyphens: bool=True):
        ...

    def set_count(self, count: int) -> None:
        """
        Set the internal counter to the given count.

        Parameters
        ----------
        count : int
            The count to set.

        """

    def generate(self) -> Any:
        """
        Return a unique client order ID.

        Returns
        -------
        ClientOrderId

        """

    def reset(self) -> None:
        """
        Reset the ID generator.

        All stateful fields are reset to their initial value.
        """

class OrderListIdGenerator(IdentifierGenerator):
    """
    Provides a generator for unique `OrderListId`(s).

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the generator.
    strategy_id : StrategyId
        The strategy ID for the generator.
    clock : Clock
        The clock for the generator.
    initial_count : int
        The initial count for the generator.

    Raises
    ------
    ValueError
        If `initial_count` is negative (< 0).
    """
    count: int

    def __init__(self, trader_id: Any, strategy_id: Any, clock: Any, initial_count: int=0):
        ...

    def set_count(self, count: int) -> None:
        """
        Set the internal counter to the given count.

        Parameters
        ----------
        count : int
            The count to set.

        """

    def generate(self) -> Any:
        """
        Return a unique order list ID.

        Returns
        -------
        OrderListId

        """

    def reset(self) -> None:
        """
        Reset the ID generator.

        All stateful fields are reset to their initial value.
        """

class PositionIdGenerator(IdentifierGenerator):
    """
    Provides a generator for unique PositionId(s).

    Parameters
    ----------
    trader_id : TraderId
        The trader ID tag for the generator.
    """

    def __init__(self, trader_id: Any, clock: Any):
        ...

    def set_count(self, strategy_id: Any, count: int) -> None:
        """
        Set the internal position count for the given strategy ID.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the count.
        count : int
            The count to set.

        Raises
        ------
        ValueError
            If `count` is negative (< 0).

        """

    def get_count(self, strategy_id: Any) -> int:
        """
        Return the internal position count for the given strategy ID.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the count.

        Returns
        -------
        int

        """

    def generate(self, strategy_id: Any, flipped: bool=False) -> Any:
        """
        Return a unique position ID.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the position.
        flipped : bool
            If the position is being flipped. If True, then the generated id
            will be appended with 'F'.

        Returns
        -------
        PositionId

        """

    def reset(self) -> None:
        """
        Reset the ID generator.

        All stateful fields are reset to their initial value.
        """