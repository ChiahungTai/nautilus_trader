# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.execution.messages import BatchCancelOrders, CancelAllOrders, CancelOrder, ModifyOrder, QueryAccount, QueryOrder, SubmitOrder, SubmitOrderList

class ExecutionClient(Any):
    """
    The base class for all execution clients.

    Parameters
    ----------
    client_id : ClientId
        The client ID.
    venue : Venue or ``None``
        The client venue. If multi-venue then can be ``None``.
    oms_type : OmsType
        The venues order management system type.
    account_type : AccountType
        The account type for the client.
    base_currency : Currency or ``None``
        The account base currency. Use ``None`` for multi-currency accounts.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache for the client.
    clock : Clock
        The clock for the client.
    config : NautilusConfig, optional
        The configuration for the instance.

    Raises
    ------
    ValueError
        If `client_id` is not equal to `account_id.get_issuer()`.
    ValueError
        If `oms_type` is ``UNSPECIFIED`` (must be specified).

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    oms_type: Any
    venue: Any
    account_id: Any
    account_type: Any
    base_currency: Any
    is_connected: bool

    def __init__(self, client_id: Any, venue: Any | None, oms_type: Any, account_type: Any, base_currency: Any | None, msgbus: Any, cache: Any, clock: Any, config: Any | None | None=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def get_account(self) -> Any:
        """
        Return the account for the client (if registered).

        Returns
        -------
        Account or ``None``

        """

    def calculate_commission(self, instrument: Any, last_qty: Any, last_px: Any, liquidity_side: Any) -> Any:
        """
        Calculate the commission for a reconciliation fill.

        Override this method to provide venue-specific commission logic
        for inferred fills generated during reconciliation.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the fill.
        last_qty : Quantity
            The fill quantity.
        last_px : Price
            The fill price.
        liquidity_side : LiquiditySide {``NO_LIQUIDITY_SIDE``, ``MAKER``, ``TAKER``}
            The liquidity side for the fill.

        Returns
        -------
        Money or ``None``

        """

    def submit_order(self, command: SubmitOrder) -> None:
        """
        Submit the order contained in the given command for execution.

        Parameters
        ----------
        command : SubmitOrder
            The command to execute.

        """

    def submit_order_list(self, command: SubmitOrderList) -> None:
        """
        Submit the order list contained in the given command for execution.

        Parameters
        ----------
        command : SubmitOrderList
            The command to execute.

        """

    def modify_order(self, command: ModifyOrder) -> None:
        """
        Modify the order with parameters contained in the command.

        Parameters
        ----------
        command : ModifyOrder
            The command to execute.

        """

    def cancel_order(self, command: CancelOrder) -> None:
        """
        Cancel the order with the client order ID contained in the given command.

        Parameters
        ----------
        command : CancelOrder
            The command to execute.

        """

    def cancel_all_orders(self, command: CancelAllOrders) -> None:
        """
        Cancel all orders for the instrument ID contained in the given command.

        Parameters
        ----------
        command : CancelAllOrders
            The command to execute.

        """

    def batch_cancel_orders(self, command: BatchCancelOrders) -> None:
        """
        Batch cancel orders for the instrument ID contained in the given command.

        Parameters
        ----------
        command : BatchCancelOrders
            The command to execute.

        """

    def query_account(self, command: QueryAccount) -> None:
        """
        Query the account specified by the command which will generate an `AccountState` event.

        Parameters
        ----------
        command : QueryAccount
            The command to execute.

        """

    def query_order(self, command: QueryOrder) -> None:
        """
        Initiate a reconciliation for the queried order which will generate an
        `OrderStatusReport`.

        Parameters
        ----------
        command : QueryOrder
            The command to execute.

        """

    def generate_account_state(self, balances: list, margins: list, reported: bool, ts_event: int, info: dict | None=None) -> None:
        """
        Generate an `AccountState` event and publish on the message bus.

        Parameters
        ----------
        balances : list[AccountBalance]
            The account balances.
        margins : list[MarginBalance]
            The margin balances.
        reported : bool
            If the balances are reported directly from the exchange.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the account state event occurred.
        info : dict [str, object]
            The additional implementation specific account information.

        """

    def generate_order_denied(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, reason: str, ts_event: int) -> None:
        """
        Generate an `OrderDenied` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        reason : str
            The order denied reason.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order denied event occurred.

        """

    def generate_order_submitted(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, ts_event: int) -> None:
        """
        Generate an `OrderSubmitted` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order submitted event occurred.

        """

    def generate_order_rejected(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, reason: str, ts_event: int, due_post_only: bool=False) -> None:
        """
        Generate an `OrderRejected` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        reason : datetime
            The order rejected reason.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order rejected event occurred.
        due_post_only : bool, default False
            If the order was rejected because it was post-only and would execute immediately as a taker.

        """

    def generate_order_accepted(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, ts_event: int) -> None:
        """
        Generate an `OrderAccepted` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order accepted event occurred.

        """

    def generate_order_modify_rejected(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, reason: str, ts_event: int) -> None:
        """
        Generate an `OrderModifyRejected` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        reason : str
            The order update rejected reason.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order update rejection event occurred.

        """

    def generate_order_cancel_rejected(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, reason: str, ts_event: int) -> None:
        """
        Generate an `OrderCancelRejected` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        reason : str
            The order cancel rejected reason.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order cancel rejected event occurred.

        """

    def generate_order_updated(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, quantity: Any, price: Any, trigger_price: Any, ts_event: int, venue_order_id_modified: bool=False, is_quote_quantity: object | None=None) -> None:
        """
        Generate an `OrderUpdated` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        quantity : Quantity
            The orders current quantity.
        price : Price
            The orders current price.
        trigger_price : Price or ``None``
            The orders current trigger price.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order update event occurred.
        venue_order_id_modified : bool
            If the ID was modified for this event.
        is_quote_quantity : bool, optional
            Override for the quote quantity flag. If ``None``, preserves
            the existing value from the cached order.

        """

    def generate_order_canceled(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, ts_event: int) -> None:
        """
        Generate an `OrderCanceled` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when order canceled event occurred.

        """

    def generate_order_triggered(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, ts_event: int) -> None:
        """
        Generate an `OrderTriggered` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order triggered event occurred.

        """

    def generate_order_expired(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, ts_event: int) -> None:
        """
        Generate an `OrderExpired` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order expired event occurred.

        """

    def generate_order_filled(self, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any, venue_position_id: Any | None, trade_id: Any, order_side: Any, order_type: Any, last_qty: Any, last_px: Any, quote_currency: Any, commission: Any, liquidity_side: Any, ts_event: int, info: dict | None=None) -> None:
        """
        Generate an `OrderFilled` event and send it to the `ExecutionEngine`.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID associated with the event.
        instrument_id : InstrumentId
            The instrument ID.
        client_order_id : ClientOrderId
            The client order ID.
        venue_order_id : VenueOrderId
            The venue order ID (assigned by the venue).
        trade_id : TradeId
            The trade ID.
        venue_position_id : PositionId or ``None``
            The venue position ID associated with the order. If the trading
            venue has assigned a position ID / ticket then pass that here,
            otherwise pass ``None`` and the execution engine OMS will handle
            position ID resolution.
        order_side : OrderSide {``BUY``, ``SELL``}
            The execution order side.
        order_type : OrderType
            The execution order type.
        last_qty : Quantity
            The fill quantity for this execution.
        last_px : Price
            The fill price for this execution (not average price).
        quote_currency : Currency
            The currency of the price.
        commission : Money
            The fill commission.
        liquidity_side : LiquiditySide {``NO_LIQUIDITY_SIDE``, ``MAKER``, ``TAKER``}
            The execution liquidity side.
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) when the order filled event occurred.
        info : dict[str, object], optional
            The additional fill information.

        """