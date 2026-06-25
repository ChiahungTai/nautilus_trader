# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
STOP_ORDER_TYPES = {Any, Any, Any, Any}
LIMIT_ORDER_TYPES = {Any, Any, Any, Any}
TRIGGERABLE_ORDER_TYPES = {Any, Any, Any}
CANCELLABLE_ORDER_STATUSES = {Any, Any, Any, Any}
LOCAL_ACTIVE_ORDER_STATUSES = {Any, Any, Any}

class Order:
    """
    The base class for all orders.

    Parameters
    ----------
    init : OrderInitialized
        The order initialized event.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    trader_id: Any
    strategy_id: Any
    instrument_id: Any
    client_order_id: Any
    venue_order_id: Any
    position_id: Any
    account_id: Any
    last_trade_id: Any
    side: Any
    order_type: Any
    time_in_force: Any
    liquidity_side: Any
    is_post_only: bool
    is_reduce_only: bool
    is_quote_quantity: bool
    quantity: Any
    filled_qty: Any
    leaves_qty: Any
    overfill_qty: Any
    avg_px: float
    slippage: float
    emulation_trigger: Any
    trigger_instrument_id: Any
    contingency_type: Any
    order_list_id: Any
    linked_order_ids: list
    parent_order_id: Any
    exec_algorithm_id: Any
    exec_algorithm_params: dict
    exec_spawn_id: Any
    tags: list
    init_id: Any
    ts_init: int
    ts_submitted: int
    ts_accepted: int
    ts_closed: int
    ts_last: int

    def __init__(self, init: Any) -> None:
        ...

    def __eq__(self, other: Order) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    def status_string(self) -> str:
        """
        Return the orders current status as a string.

        Returns
        -------
        str

        """

    def side_string(self) -> str:
        """
        Return the orders side as a string.

        Returns
        -------
        str

        """

    def type_string(self) -> str:
        """
        Return the orders type as a string.

        Returns
        -------
        str

        """

    def tif_string(self) -> str:
        """
        Return the orders time in force as a string.

        Returns
        -------
        str

        """

    def info(self) -> str:
        """
        Return a summary description of the order.

        Returns
        -------
        str

        """

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

    def set_quote_quantity(self, value: bool) -> None:
        ...

    def to_own_book_order(self) -> Any:
        """
        Returns an own/user order representation of this order.

        Returns
        -------
        nautilus_pyo3.OwnBookOrder

        """

    @property
    def symbol(self):
        """
        Return the orders ticker symbol.

        Returns
        -------
        Symbol

        """

    @property
    def venue(self):
        """
        Return the orders trading venue.

        Returns
        -------
        Venue

        """

    @property
    def status(self):
        """
        Return the orders current status.

        Returns
        -------
        OrderStatus

        """

    @property
    def init_event(self):
        """
        Return the initialization event for the order.

        Returns
        -------
        OrderInitialized

        """

    @property
    def last_event(self):
        """
        Return the last event applied to the order.

        Returns
        -------
        OrderEvent

        """

    @property
    def events(self):
        """
        Return the order events.

        Returns
        -------
        list[OrderEvent]

        """

    @property
    def venue_order_ids(self):
        """
        Return the venue order IDs.

        Returns
        -------
        list[VenueOrderId]

        """

    @property
    def trade_ids(self):
        """
        Return the trade match IDs.

        Returns
        -------
        list[TradeId]

        """

    @property
    def event_count(self):
        """
        Return the count of events applied to the order.

        Returns
        -------
        int

        """

    @property
    def has_price(self):
        """
        Return whether the order has a `price` property.

        Returns
        -------
        bool

        """

    @property
    def has_trigger_price(self):
        """
        Return whether the order has a `trigger_price` property.

        Returns
        -------
        bool

        """

    @property
    def has_activation_price(self):
        """
        Return whether the order has a `activation_price` property.

        Returns
        -------
        bool

        """

    @property
    def is_buy(self):
        """
        Return whether the order side is ``BUY``.

        Returns
        -------
        bool

        """

    @property
    def is_sell(self):
        """
        Return whether the order side is ``SELL``.

        Returns
        -------
        bool

        """

    @property
    def is_passive(self):
        """
        Return whether the order is passive (`order_type` **not** ``MARKET``).

        Returns
        -------
        bool

        """

    @property
    def is_aggressive(self):
        """
        Return whether the order is aggressive (`order_type` is ``MARKET``).

        Returns
        -------
        bool

        """

    @property
    def is_emulated(self):
        """
        Return whether the order is emulated and held in the local system.

        Returns
        -------
        bool

        """

    @property
    def is_active_local(self):
        """
        Return whether the order is active and held in the local system.

        An order is considered active local when its status is any of:
        - ``INITIALIZED``
        - ``EMULATED``
        - ``RELEASED``

        Returns
        -------
        bool

        """

    @property
    def is_primary(self):
        """
        Return whether the order is the primary for an execution algorithm sequence.

        Returns
        -------
        bool

        """

    @property
    def is_spawned(self):
        """
        Return whether the order was spawned as part of an execution algorithm sequence.

        Returns
        -------
        bool

        """

    @property
    def is_contingency(self):
        """
        Return whether the order has a contingency (`contingency_type` is not ``NO_CONTINGENCY``).

        Returns
        -------
        bool

        """

    @property
    def is_parent_order(self):
        """
        Return whether the order has **at least** one child order.

        Returns
        -------
        bool

        """

    @property
    def is_child_order(self):
        """
        Return whether the order has a parent order.

        Returns
        -------
        bool

        """

    @property
    def is_inflight(self):
        """
        Return whether the order is in-flight (order request sent to the trading venue).

        An order is considered in-flight when its status is any of:
        - ``SUBMITTED``
        - ``PENDING_UPDATE``
        - ``PENDING_CANCEL``

        Returns
        -------
        bool

        Warnings
        --------
        An emulated order is never considered in-flight.

        """

    @property
    def is_open(self):
        """
        Return whether the order is open at the trading venue.

        An order is considered open when its status is any of:
        - ``ACCEPTED``
        - ``TRIGGERED``
        - ``PENDING_UPDATE``
        - ``PENDING_CANCEL``
        - ``PARTIALLY_FILLED``

        Returns
        -------
        bool

        Warnings
        --------
        An emulated order is never considered open.

        """

    @property
    def is_canceled(self):
        """
        Return whether current `status` is ``CANCELED``.

        Returns
        -------
        bool

        """

    @property
    def is_closed(self):
        """
        Return whether the order is closed (lifecycle completed).

        An order is considered closed when its status can no longer change.
        The possible statuses of closed orders include;

        - ``DENIED``
        - ``REJECTED``
        - ``CANCELED``
        - ``EXPIRED``
        - ``FILLED``

        Returns
        -------
        bool

        """

    @property
    def is_pending_update(self):
        """
        Return whether the current `status` is ``PENDING_UPDATE``.

        Returns
        -------
        bool

        """

    @property
    def is_pending_cancel(self):
        """
        Return whether the current `status` is ``PENDING_CANCEL``.

        Returns
        -------
        bool

        """

    @staticmethod
    def opposite_side(side: Any) -> Any:
        """
        Return the opposite order side from the given side.

        Parameters
        ----------
        side : OrderSide {``BUY``, ``SELL``}
            The original order side.

        Returns
        -------
        OrderSide

        Raises
        ------
        ValueError
            If `side` is invalid.

        """

    @staticmethod
    def closing_side(position_side: Any) -> Any:
        """
        Return the order side needed to close a position with the given side.

        Parameters
        ----------
        position_side : PositionSide {``LONG``, ``SHORT``}
            The side of the position to close.

        Returns
        -------
        OrderSide

        Raises
        ------
        ValueError
            If `position_side` is ``FLAT`` or invalid.

        """

    def signed_decimal_qty(self):
        """
        Return a signed decimal representation of the remaining quantity.

         - If the order is a BUY, the value is positive (e.g. Decimal('10.25'))
         - If the order is a SELL, the value is negative (e.g. Decimal('-10.25'))

        Returns
        -------
        Decimal

        """

    def would_reduce_only(self, position_side: Any, position_qty: Any) -> bool:
        """
        Whether the current order would only reduce the given position if applied
        in full.

        Parameters
        ----------
        position_side : PositionSide {``FLAT``, ``LONG``, ``SHORT``}
            The side of the position to check against.
        position_qty : Quantity
            The quantity of the position to check against.

        Returns
        -------
        bool

        """

    def commissions(self) -> list:
        """
        Return the total commissions generated by the order.

        Returns
        -------
        list[Money]

        """

    def apply(self, event: Any) -> None:
        """
        Apply the given order event to the order.

        Parameters
        ----------
        event : OrderEvent
            The order event to apply.

        Raises
        ------
        ValueError
            If `self.client_order_id` is not equal to `event.client_order_id`.
        ValueError
            If `self.venue_order_id` and `event.venue_order_id` are both not ``None``, and are not equal.
        InvalidStateTrigger
            If `event` is not a valid trigger from the current `order.status`.
        KeyError
            If `event` is `OrderFilled` and `event.trade_id` already applied to the order.

        """

    def is_duplicate_fill(self, fill: Any) -> bool:
        """
        Return whether a fill with matching trade_id, side, qty, and price already exists.

        Parameters
        ----------
        fill : OrderFilled
            The fill event to check.

        Returns
        -------
        bool

        """