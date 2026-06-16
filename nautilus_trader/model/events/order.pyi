# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class OrderEvent(Any):
    """
    The abstract base class for all order events.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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

    def set_client_order_id(self, client_order_id: Any):
        ...

class OrderInitialized(OrderEvent):
    """
    Represents an event where an order has been initialized.

    This is a seed event which can instantiate any order through a creation
    method. This event should contain enough information to be able to send it
    'over the wire' and have a valid order created with exactly the same
    properties as if it had been instantiated locally.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    order_side : OrderSide {``BUY``, ``SELL``}
        The order side.
    order_type : OrderType
        The order type.
    quantity : Quantity
        The order quantity.
    time_in_force : TimeInForce {``GTC``, ``IOC``, ``FOK``, ``GTD``, ``DAY``, ``AT_THE_OPEN``, ``AT_THE_CLOSE``}
        The order time in force.
    post_only : bool
        If the order will only provide liquidity (make a market).
    reduce_only : bool
        If the order carries the 'reduce-only' execution instruction.
    quote_quantity : bool
        If the order quantity is denominated in the quote currency.
    options : dict[str, str]
        The order initialization options. Contains mappings for specific
        order parameters.
    emulation_trigger : TriggerType, default ``NO_TRIGGER``
        The type of market price trigger to use for local order emulation.
        - ``NO_TRIGGER`` (default): Disables local emulation; orders are sent directly to the venue.
        - ``DEFAULT`` (the same as ``BID_ASK``): Enables local order emulation by triggering orders based on bid/ask prices.
        Additional trigger types are available. See the "Emulated Orders" section in the documentation for more details.
    trigger_instrument_id : InstrumentId or ``None``
        The emulation trigger instrument ID for the order (if ``None`` then will be the `instrument_id`).
    contingency_type : ContingencyType
        The order contingency type.
    order_list_id : OrderListId or ``None``
        The order list ID associated with the order.
    linked_order_ids : list[ClientOrderId] or ``None``
        The order linked client order ID(s).
    parent_order_id : ClientOrderId or ``None``
        The orders parent client order ID.
    exec_algorithm_id : ExecAlgorithmId or ``None``
        The execution algorithm ID for the order.
    exec_algorithm_params : dict[str, Any], optional
        The execution algorithm parameters for the order.
    exec_spawn_id : ClientOrderId or ``None``
        The execution algorithm spawning primary client order ID.
    tags : list[str] or ``None``
        The custom user tags for the order.
    event_id : UUID4
        The event ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.

    Raises
    ------
    ValueError
        If `order_side` is ``NO_ORDER_SIDE``.
    ValueError
        If `contingency_type` is not ``NO_CONTINGENCY``, and `linked_order_ids` is ``None`` or empty.
    ValueError
        If `exec_algorithm_id` is not ``None``, and `exec_spawn_id` is ``None``.
    """
    side: Any
    order_type: Any
    quantity: Any
    time_in_force: Any
    post_only: bool
    reduce_only: bool
    quote_quantity: bool
    options: dict
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

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, order_side: Any, order_type: Any, quantity: Any, time_in_force: Any, post_only: bool, reduce_only: bool, quote_quantity: bool, options: dict, emulation_trigger: Any, trigger_instrument_id: Any | None, contingency_type: Any, order_list_id: Any | None, linked_order_ids: list[Any] | None, parent_order_id: Any | None, exec_algorithm_id: Any | None, exec_algorithm_params: dict[str, object] | None, exec_spawn_id: Any | None, tags: list[str] | None, event_id: Any, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderInitialized:
        """
        Return an order initialized event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderInitialized

        """

    @staticmethod
    def to_dict(obj: OrderInitialized):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderDenied(OrderEvent):
    """
    Represents an event where an order has been denied by the Nautilus system.

    This could be due an unsupported feature, a risk limit exceedance, or for
    any other reason that an otherwise valid order is not able to be submitted.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    reason : str
        The order denied reason.
    event_id : UUID4
        The event ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.

    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, reason: str, event_id: Any, ts_init: int):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reason(self) -> str:
        """
        Return the reason the order was denied.

        Returns
        -------
        str

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderDenied:
        """
        Return an order denied event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderDenied

        """

    @staticmethod
    def to_dict(obj: OrderDenied):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderEmulated(OrderEvent):
    """
    Represents an event where an order has become emulated by the Nautilus system.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    event_id : UUID4
        The event ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.

    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, event_id: Any, ts_init: int):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderEmulated:
        """
        Return an order emulated event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderEmulated

        """

    @staticmethod
    def to_dict(obj: OrderEmulated):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderReleased(OrderEvent):
    """
    Represents an event where an order was released from the `OrderEmulator` by the Nautilus system.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    released_price : Price
        The price which released the order from the emulator.
    event_id : UUID4
        The event ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.

    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, released_price: Any, event_id: Any, ts_init: int):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def released_price(self) -> Any:
        """
        The released price for the event.

        Returns
        -------
        Price

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderReleased:
        """
        Return an order released event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderReleased

        """

    @staticmethod
    def to_dict(obj: OrderReleased):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderSubmitted(OrderEvent):
    """
    Represents an event where an order has been submitted by the system to the
    trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    account_id : AccountId
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order submitted event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, account_id: Any, event_id: Any, ts_event: int, ts_init: int):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderSubmitted:
        """
        Return an order submitted event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderSubmitted

        """

    @staticmethod
    def to_dict(obj: OrderSubmitted):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderAccepted(OrderEvent):
    """
    Represents an event where an order has been accepted by the trading venue.

    This event often corresponds to a `NEW` OrdStatus <39> field in FIX execution reports.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId
        The venue order ID (assigned by the venue).
    account_id : AccountId
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order accepted event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.

    References
    ----------
    https://www.onixs.biz/fix-dictionary/5.0.SP2/tagNum_39.html
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, account_id: Any, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderAccepted:
        """
        Return an order accepted event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderAccepted

        """

    @staticmethod
    def to_dict(obj: OrderAccepted):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderRejected(OrderEvent):
    """
    Represents an event where an order has been rejected by the trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    account_id : AccountId
        The account ID (with the venue).
    reason : str
        The order rejected reason.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order rejected event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    due_post_only : bool, default False
        If the order was rejected because it was post-only and would execute immediately as a taker.

    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, account_id: Any, reason: str, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False, due_post_only: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reason(self) -> str:
        """
        Return the reason the order was rejected.

        Returns
        -------
        str

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

    @property
    def due_post_only(self) -> bool:
        """
        If the order was rejected because it was post-only and would execute immediately as a taker.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderRejected:
        """
        Return an order rejected event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderRejected

        """

    @staticmethod
    def to_dict(obj: OrderRejected):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderCanceled(OrderEvent):
    """
    Represents an event where an order has been canceled at the trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when order canceled event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderCanceled:
        """
        Return an order canceled event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderCanceled

        """

    @staticmethod
    def to_dict(obj: OrderCanceled):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderExpired(OrderEvent):
    """
    Represents an event where an order has expired at the trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order expired event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderExpired:
        """
        Return an order expired event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderExpired

        """

    @staticmethod
    def to_dict(obj: OrderExpired):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderTriggered(OrderEvent):
    """
    Represents an event where an order has triggered.

    Applicable to :class:`StopLimit` orders only.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order triggered event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderTriggered:
        """
        Return an order triggered event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderTriggered

        """

    @staticmethod
    def to_dict(obj: OrderTriggered):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderPendingUpdate(OrderEvent):
    """
    Represents an event where an `ModifyOrder` command has been sent to the
    trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order pending update event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderPendingUpdate:
        """
        Return an order pending update event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderPendingUpdate

        """

    @staticmethod
    def to_dict(obj: OrderPendingUpdate):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderPendingCancel(OrderEvent):
    """
    Represents an event where a `CancelOrder` command has been sent to the
    trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order pending cancel event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderPendingCancel:
        """
        Return an order pending cancel event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderPendingCancel

        """

    @staticmethod
    def to_dict(obj: OrderPendingCancel):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderModifyRejected(OrderEvent):
    """
    Represents an event where a `ModifyOrder` command has been rejected by the
    trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    reason : str
        The order update rejected reason.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order update rejected event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.

    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, reason: str, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reason(self) -> str:
        """
        Return the reason the order was rejected.

        Returns
        -------
        str

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderModifyRejected:
        """
        Return an order update rejected event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderModifyRejected

        """

    @staticmethod
    def to_dict(obj: OrderModifyRejected):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderCancelRejected(OrderEvent):
    """
    Represents an event where a `CancelOrder` command has been rejected by the
    trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    reason : str
        The order cancel rejected reason.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order cancel rejected event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.

    """

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, reason: str, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reason(self) -> str:
        """
        Return the reason the order was rejected.

        Returns
        -------
        str

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderCancelRejected:
        """
        Return an order cancel rejected event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderCancelRejected

        """

    @staticmethod
    def to_dict(obj: OrderCancelRejected):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderUpdated(OrderEvent):
    """
    Represents an event where an order has been updated at the trading venue.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue).
    account_id : AccountId or ``None``
        The account ID (with the venue).
    quantity : Quantity
        The orders current quantity.
    price : Price or ``None``
        The orders current price.
    trigger_price : Price or ``None``
        The orders current trigger.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order updated event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    reconciliation : bool, default False
        If the event was generated during reconciliation.
    is_quote_quantity : bool, default False
        If the order quantity is denominated in the quote currency.

    Raises
    ------
    ValueError
        If `quantity` is not positive (> 0).
    """
    quantity: Any
    price: Any
    trigger_price: Any
    is_quote_quantity: bool

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, account_id: Any | None, quantity: Any, price: Any | None, trigger_price: Any | None, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False, is_quote_quantity: bool=False):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderUpdated:
        """
        Return an order updated event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderUpdated

        """

    @staticmethod
    def to_dict(obj: OrderUpdated):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class OrderFilled(OrderEvent):
    """
    Represents an event where an order has been filled at the exchange.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID.
    strategy_id : StrategyId
        The strategy ID.
    instrument_id : InstrumentId
        The instrument ID.
    client_order_id : ClientOrderId
        The client order ID.
    venue_order_id : VenueOrderId
        The venue order ID (assigned by the venue).
    account_id : AccountId
        The account ID (with the venue).
    trade_id : TradeId
        The trade match ID (assigned by the venue).
    position_id : PositionId or ``None``
        The position ID associated with the order fill (assigned by the venue).
    order_side : OrderSide {``BUY``, ``SELL``}
        The execution order side.
    order_type : OrderType
        The execution order type.
    last_qty : Quantity
        The fill quantity for this execution.
    last_px : Price
        The fill price for this execution (not average price).
    currency : Currency
        The currency of the price.
    commission : Money
        The fill commission.
    liquidity_side : LiquiditySide {``NO_LIQUIDITY_SIDE``, ``MAKER``, ``TAKER``}
        The execution liquidity side.
    event_id : UUID4
        The event ID.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the order filled event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    info : dict[str, object], optional
        The additional fill information.
    reconciliation : bool, default False
        If the event was generated during reconciliation.

    Raises
    ------
    ValueError
        If `order_side` is ``NO_ORDER_SIDE``.
    ValueError
        If `last_qty` is not positive (> 0).
    """
    trade_id: Any
    position_id: Any
    order_side: Any
    order_type: Any
    last_qty: Any
    last_px: Any
    currency: Any
    commission: Any
    liquidity_side: Any
    info: dict

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, account_id: Any, trade_id: Any, position_id: Any | None, order_side: Any, order_type: Any, last_qty: Any, last_px: Any, currency: Any, commission: Any, liquidity_side: Any, event_id: Any, ts_event: int, ts_init: int, reconciliation: bool=False, info: dict | None=None):
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def set_client_order_id(self, client_order_id: Any):
        ...

    @property
    def trader_id(self) -> Any:
        """
        The trader ID associated with the event.

        Returns
        -------
        TraderId

        """

    @property
    def strategy_id(self) -> Any:
        """
        The strategy ID associated with the event.

        Returns
        -------
        StrategyId

        """

    @property
    def instrument_id(self) -> Any:
        """
        The instrument ID associated with the event.

        Returns
        -------
        InstrumentId

        """

    @property
    def client_order_id(self) -> Any:
        """
        The client order ID associated with the event.

        Returns
        -------
        ClientOrderId

        """

    @property
    def venue_order_id(self) -> Any | None:
        """
        The venue order ID associated with the event.

        Returns
        -------
        VenueOrderId or ``None``

        """

    @property
    def account_id(self) -> Any | None:
        """
        The account ID associated with the event.

        Returns
        -------
        AccountId or ``None``

        """

    @property
    def reconciliation(self) -> bool:
        """
        If the event was generated during reconciliation.

        Returns
        -------
        bool

        """

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
    def from_dict(values: dict) -> OrderFilled:
        """
        Return an order filled event from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        OrderFilled

        """

    @staticmethod
    def to_dict(obj: OrderFilled):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

    @property
    def is_buy(self):
        """
        Return whether the fill order side is ``BUY``.

        Returns
        -------
        bool

        """

    @property
    def is_sell(self):
        """
        Return whether the fill order side is ``SELL``.

        Returns
        -------
        bool

        """