# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class PositionEvent(Any):
    """
    The base class for all position events.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    position_id : PositionId
        The position IDt.
    account_id : AccountId
        The strategy ID.
    opening_order_id : ClientOrderId
        The client order ID for the order which opened the position.
    closing_order_id : ClientOrderId
        The client order ID for the order which closed the position.
    entry : OrderSide {``BUY``, ``SELL``}
        The position entry order side.
    side : PositionSide {``FLAT``, ``LONG``, ``SHORT``}
        The current position side.
    signed_qty : double
        The current signed quantity (positive for ``LONG``, negative for ``SHORT``).
    quantity : Quantity
        The current open quantity.
    peak_qty : Quantity
        The peak directional quantity reached by the position.
    last_qty : Quantity
        The last fill quantity for the position.
    last_px : Price
        The last fill price for the position (not average price).
    currency : Currency
        The position quote currency.
    avg_px_open : double
        The average open price.
    avg_px_close : double
        The average close price.
    realized_return : double
        The realized return for the position.
    realized_pnl : Money
        The realized PnL for the position.
    unrealized_pnl : Money
        The unrealized PnL for the position.
    event_id : UUID4
        The event ID.
    ts_opened : uint64_t
        UNIX timestamp (nanoseconds) when the position opened event occurred.
    ts_closed : uint64_t
        UNIX timestamp (nanoseconds) when the position closed event occurred.
    duration_ns : uint64_t
        The total open duration (nanoseconds), will be 0 if still open.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    trader_id: Any
    strategy_id: Any
    instrument_id: Any
    position_id: Any
    account_id: Any
    opening_order_id: Any
    closing_order_id: Any
    entry: Any
    side: Any
    signed_qty: float
    quantity: Any
    peak_qty: Any
    last_qty: Any
    last_px: Any
    currency: Any
    avg_px_open: float
    avg_px_close: float
    realized_return: float
    realized_pnl: Any
    unrealized_pnl: Any
    ts_opened: int
    ts_closed: int
    duration_ns: int

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, position_id: Any, account_id: Any, opening_order_id: Any, closing_order_id: Any | None, entry: Any, side: Any, signed_qty: float, quantity: Any, peak_qty: Any, last_qty: Any, last_px: Any, currency: Any, avg_px_open: float, avg_px_close: float, realized_return: float, realized_pnl: Any, unrealized_pnl: Any, event_id: Any, ts_opened: int, ts_closed: int, duration_ns: int, ts_event: int, ts_init: int):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def id(self) -> Any:
        """
        The event message identifier.

        Returns
        -------
        UUID4

        """

    @property
    def ts_event(self) -> int:
        """
        UNIX timestamp (nanoseconds) when the event occurred.

        Returns
        -------
        int

        """

    @property
    def ts_init(self) -> int:
        """
        UNIX timestamp (nanoseconds) when the object was initialized.

        Returns
        -------
        int

        """

class PositionOpened(PositionEvent):
    """
    Represents an event where a position has been opened.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    position_id : PositionId
        The position IDt.
    account_id : AccountId
        The strategy ID.
    opening_order_id : ClientOrderId
        The client order ID for the order which opened the position.
    strategy_id : StrategyId
        The strategy ID associated with the event.
    entry : OrderSide {``BUY``, ``SELL``}
        The position entry order side.
    side : PositionSide {``LONG``, ``SHORT``}
        The current position side.
    signed_qty : double
        The current signed quantity (positive for ``LONG``, negative for ``SHORT``).
    quantity : Quantity
        The current open quantity.
    peak_qty : Quantity
        The peak directional quantity reached by the position.
    last_qty : Quantity
        The last fill quantity for the position.
    last_px : Price
        The last fill price for the position (not average price).
    currency : Currency
        The position quote currency.
    avg_px_open : double
        The average open price.
    realized_pnl : Money
        The realized PnL for the position.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the position opened event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, position_id: Any, account_id: Any, opening_order_id: Any, entry: Any, side: Any, signed_qty: float, quantity: Any, peak_qty: Any, last_qty: Any, last_px: Any, currency: Any, avg_px_open: float, realized_pnl: Any, event_id: Any, ts_event: int, ts_init: int):
        ...

    @staticmethod
    def create(position: Any, fill: Any, event_id: Any, ts_init: int):
        """
        Return a position opened event from the given params.

        Parameters
        ----------
        position : Position
            The position for the event.
        fill : OrderFilled
            The order fill for the event.
        event_id : UUID4
            The event ID.
        ts_init : uint64_t
            UNIX timestamp (nanoseconds) when the object was initialized.

        Returns
        -------
        PositionOpened

        """

    @staticmethod
    def from_dict(values: dict) -> PositionOpened:
        """
        Return a position opened event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        PositionOpened

        """

    @staticmethod
    def to_dict(obj: PositionOpened):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class PositionChanged(PositionEvent):
    """
    Represents an event where a position has changed.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    position_id : PositionId
        The position IDt.
    account_id : AccountId
        The strategy ID.
    opening_order_id : ClientOrderId
        The client order ID for the order which opened the position.
    strategy_id : StrategyId
        The strategy ID associated with the event.
    entry : OrderSide {``BUY``, ``SELL``}
        The position entry order side.
    side : PositionSide {``FLAT``, ``LONG``, ``SHORT``}
        The current position side.
    signed_qty : double
        The current signed quantity (positive for ``LONG``, negative for ``SHORT``).
    quantity : Quantity
        The current open quantity.
    peak_qty : Quantity
        The peak directional quantity reached by the position.
    last_qty : Quantity
        The last fill quantity for the position.
    last_px : Price
        The last fill price for the position (not average price).
    currency : Currency
        The position quote currency.
    avg_px_open : double
        The average open price.
    avg_px_close : double
        The average close price.
    realized_return : double
        The realized return for the position.
    realized_pnl : Money
        The realized PnL for the position.
    unrealized_pnl : Money
        The unrealized PnL for the position.
    event_id : UUID4
        The event ID.
    ts_opened : uint64_t
        UNIX timestamp (nanoseconds) when the position opened event occurred.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the position changed event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, position_id: Any, account_id: Any, opening_order_id: Any, entry: Any, side: Any, signed_qty: float, quantity: Any, peak_qty: Any, last_qty: Any, last_px: Any, currency: Any, avg_px_open: float, avg_px_close: float, realized_return: float, realized_pnl: Any, unrealized_pnl: Any, event_id: Any, ts_opened: int, ts_event: int, ts_init: int):
        ...

    @staticmethod
    def create(position: Any, fill: Any, event_id: Any, ts_init: int):
        """
        Return a position changed event from the given params.

        Parameters
        ----------
        position : Position
            The position for the event.
        fill : OrderFilled
            The order fill for the event.
        event_id : UUID4
            The event ID.
        ts_init : uint64_t
            UNIX timestamp (nanoseconds) when the object was initialized.

        Returns
        -------
        PositionChanged

        """

    @staticmethod
    def from_dict(values: dict) -> PositionChanged:
        """
        Return a position changed event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        PositionChanged

        """

    @staticmethod
    def to_dict(obj: PositionChanged):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class PositionClosed(PositionEvent):
    """
    Represents an event where a position has been closed.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    position_id : PositionId
        The position IDt.
    account_id : AccountId
        The strategy ID.
    opening_order_id : ClientOrderId
        The client order ID for the order which opened the position.
    closing_order_id : ClientOrderId
        The client order ID for the order which closed the position.
    strategy_id : StrategyId
        The strategy ID associated with the event.
    entry : OrderSide {``BUY``, ``SELL``}
        The position entry order side.
    side : PositionSide {``FLAT``}
        The current position side.
    signed_qty : double
        The current signed quantity (positive for ``LONG``, negative for ``SHORT``).
    quantity : Quantity
        The current open quantity.
    peak_qty : Quantity
        The peak directional quantity reached by the position.
    last_qty : Quantity
        The last fill quantity for the position.
    last_px : Price
        The last fill price for the position (not average price).
    currency : Currency
        The position quote currency.
    avg_px_open : Decimal
        The average open price.
    avg_px_close : Decimal
        The average close price.
    realized_return : Decimal
        The realized return for the position.
    realized_pnl : Money
        The realized PnL for the position.
    event_id : UUID4
        The event ID.
    ts_opened : uint64_t
        UNIX timestamp (nanoseconds) when the position opened event occurred.
    ts_closed : uint64_t
        UNIX timestamp (nanoseconds) when the position closed event occurred.
    duration_ns : uint64_t
        The total open duration (nanoseconds).
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, position_id: Any, account_id: Any, opening_order_id: Any, closing_order_id: Any, entry: Any, side: Any, signed_qty: float, quantity: Any, peak_qty: Any, last_qty: Any, last_px: Any, currency: Any, avg_px_open: float, avg_px_close: float, realized_return: float, realized_pnl: Any, event_id: Any, ts_opened: int, ts_closed: int, duration_ns: int, ts_init: int):
        ...

    @staticmethod
    def create(position: Any, fill: Any, event_id: Any, ts_init: int):
        """
        Return a position closed event from the given params.

        Parameters
        ----------
        position : Position
            The position for the event.
        fill : OrderFilled
            The order fill for the event.
        event_id : UUID4
            The event ID.
        ts_init : uint64_t
            UNIX timestamp (nanoseconds) when the object was initialized.

        Returns
        -------
        PositionClosed

        """

    @staticmethod
    def from_dict(values: dict) -> PositionClosed:
        """
        Return a position closed event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        PositionClosed

        """

    @staticmethod
    def to_dict(obj: PositionClosed):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class PositionAdjusted(Any):
    """
    Represents an adjustment to a position's quantity or realized PnL.

    This event is used to track changes to positions that occur outside of normal
    order fills, such as commission adjustments or funding payments.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    position_id : PositionId
        The position ID.
    account_id : AccountId
        The account ID.
    adjustment_type : PositionAdjustmentType
        The type of adjustment.
    quantity_change : Decimal | None
        The quantity change (positive increases quantity, negative decreases).
    pnl_change : Money | None
        The PnL change.
    reason : str | None
        Optional reason or reference for the adjustment.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    """
    trader_id: Any
    strategy_id: Any
    instrument_id: Any
    position_id: Any
    account_id: Any
    adjustment_type: Any
    quantity_change: object
    pnl_change: Any
    reason: str

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, position_id: Any, account_id: Any, adjustment_type: Any, quantity_change: object, pnl_change: Any | None, reason: str | None, event_id: Any, ts_event: int, ts_init: int) -> None:
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @property
    def id(self) -> Any:
        """
        The event message identifier.

        Returns
        -------
        UUID4

        """

    @property
    def ts_event(self) -> int:
        """
        UNIX timestamp (nanoseconds) when the event occurred.

        Returns
        -------
        int

        """

    @property
    def ts_init(self) -> int:
        """
        UNIX timestamp (nanoseconds) when the object was initialized.

        Returns
        -------
        int

        """

    @staticmethod
    def from_dict(values: dict) -> PositionAdjusted:
        """
        Return a position adjustment event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        PositionAdjusted

        """

    @staticmethod
    def to_dict(obj: PositionAdjusted):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """