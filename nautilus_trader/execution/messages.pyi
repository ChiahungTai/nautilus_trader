# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from datetime import datetime

class ExecutionReportCommand(Any):
    """
    The base class for all execution report commands.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the command.
    start : datetime, optional
        The start datetime (UTC) of request time range (inclusive).
    end : datetime, optional
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    instrument_id: Any
    start: datetime
    end: datetime
    params: dict

    def __init__(self, instrument_id: Any | None, start: datetime | None, end: datetime | None, command_id: Any, ts_init: int, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

class GenerateOrderStatusReport(ExecutionReportCommand):
    """
    Command to generate an order status report.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the command.
    client_order_id : ClientOrderId
        The client order ID to update.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue) to query.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.
    """
    client_order_id: Any
    venue_order_id: Any

    def __init__(self, instrument_id: Any | None, client_order_id: Any | None, venue_order_id: Any | None, command_id: Any, ts_init: int, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> GenerateOrderStatusReport:
        """
        Return a generate order status report command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        GenerateOrderStatusReport

        """

    @staticmethod
    def to_dict(obj: GenerateOrderStatusReport):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class GenerateOrderStatusReports(ExecutionReportCommand):
    """
    Command to generate order status reports.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the command.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    open_only : bool
        If True then only open orders will be requested.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.
    log_receipt_level : LogLevel, default 'INFO'
        The log level for logging received reports. Must be either `LogLevel.DEBUG` or `LogLevel.INFO`.
    """
    open_only: bool
    log_receipt_level: Any

    def __init__(self, instrument_id: Any | None, start: datetime | None, end: datetime | None, open_only: bool, command_id: Any, ts_init: int, params: dict | None | None=None, log_receipt_level: Any=..., correlation_id: Any=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> GenerateOrderStatusReports:
        """
        Return a generate order status reports command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        GenerateOrderStatusReports

        """

    @staticmethod
    def to_dict(obj: GenerateOrderStatusReports):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class GenerateFillReports(ExecutionReportCommand):
    """
    Command to generate fill reports.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the command.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue) to query.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.
    """
    venue_order_id: Any

    def __init__(self, instrument_id: Any | None, venue_order_id: Any | None, start: datetime | None, end: datetime | None, command_id: Any, ts_init: int, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> GenerateFillReports:
        """
        Return a generate fill reports command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        GenerateFillReports

        """

    @staticmethod
    def to_dict(obj: GenerateFillReports):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class GeneratePositionStatusReports(ExecutionReportCommand):
    """
    Command to generate position status reports.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the command.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.
    log_receipt_level : LogLevel, default 'INFO'
        The log level for logging received reports. Must be either `LogLevel.DEBUG` or `LogLevel.INFO`.
    """
    log_receipt_level: Any

    def __init__(self, instrument_id: Any | None, start: datetime | None, end: datetime | None, command_id: Any, ts_init: int, params: dict | None | None=None, log_receipt_level: Any=..., correlation_id: Any=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> GeneratePositionStatusReports:
        """
        Return a generate position status reports command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        GeneratePositionStatusReports

        """

    @staticmethod
    def to_dict(obj: GeneratePositionStatusReports):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class GenerateExecutionMassStatus(ExecutionReportCommand):
    """
    Command to generate an execution mass status report.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    client_id : ClientId
        The client ID for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    venue : Venue, optional
        The venue for the command.
    params : dict[str, object], optional
        Additional parameters for the command.
    """
    trader_id: Any
    client_id: Any
    venue: Any

    def __init__(self, trader_id: Any, client_id: Any, command_id: Any, ts_init: int, venue: Any | None | None=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> GenerateExecutionMassStatus:
        """
        Return a generate execution mass status command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        GenerateExecutionMassStatus

        """

    @staticmethod
    def to_dict(obj: GenerateExecutionMassStatus):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class TradingCommand(Any):
    """
    The base class for all trading related commands.

    Parameters
    ----------
    client_id : ClientId or ``None``
        The execution client ID for the command.
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    instrument_id : InstrumentId
        The instrument ID for the command.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    client_id: Any
    trader_id: Any
    strategy_id: Any
    instrument_id: Any
    params: dict

    def __init__(self, client_id: Any | None, trader_id: Any, strategy_id: Any, instrument_id: Any, command_id: Any, ts_init: int, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

class SubmitOrder(TradingCommand):
    """
    Represents a command to submit the given order.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    order : Order
        The order to submit.
    command_id : UUID4
        The commands ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    position_id : PositionId, optional
        The position ID for the command.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.

    References
    ----------
    https://www.onixs.biz/fix-dictionary/5.0.SP2/msgType_D_68.html
    """
    order: Any
    exec_algorithm_id: Any
    position_id: Any

    def __init__(self, trader_id: Any, strategy_id: Any, order: Any, command_id: Any, ts_init: int, position_id: Any | None | None=None, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> SubmitOrder:
        """
        Return a submit order command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        SubmitOrder

        """

    @staticmethod
    def to_dict(obj: SubmitOrder):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class SubmitOrderList(TradingCommand):
    """
    Represents a command to submit an order list consisting of an order batch/bulk
    of related parent-child contingent orders.

    This command can correspond to a `NewOrderList <E> message` for the FIX
    protocol.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    order_list : OrderList
        The order list to submit.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    position_id : PositionId, optional
        The position ID for the command.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.

    References
    ----------
    https://www.onixs.biz/fix-dictionary/5.0.SP2/msgType_E_69.html
    """
    order_list: Any
    exec_algorithm_id: Any
    position_id: Any
    has_emulated_order: bool

    def __init__(self, trader_id: Any, strategy_id: Any, order_list: Any, command_id: Any, ts_init: int, position_id: Any | None | None=None, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> SubmitOrderList:
        """
        Return a submit order list command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        SubmitOrderList

        """

    @staticmethod
    def to_dict(obj: SubmitOrderList):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class ModifyOrder(TradingCommand):
    """
    Represents a command to modify the properties of an existing order.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    instrument_id : InstrumentId
        The instrument ID for the command.
    client_order_id : ClientOrderId
        The client order ID to update.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue) to update.
    quantity : Quantity or ``None``
        The quantity for the order update.
    price : Price or ``None``
        The price for the order update.
    trigger_price : Price or ``None``
        The trigger price for the order update.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.

    References
    ----------
    https://www.onixs.biz/fix-dictionary/5.0.SP2/msgType_G_71.html
    """
    client_order_id: Any
    venue_order_id: Any
    quantity: Any
    price: Any
    trigger_price: Any

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, quantity: Any | None, price: Any | None, trigger_price: Any | None, command_id: Any, ts_init: int, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> ModifyOrder:
        """
        Return a modify order command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        ModifyOrder

        """

    @staticmethod
    def to_dict(obj: ModifyOrder):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class CancelOrder(TradingCommand):
    """
    Represents a command to cancel an order.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    instrument_id : InstrumentId
        The instrument ID for the command.
    client_order_id : ClientOrderId
        The client order ID to cancel.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue) to cancel.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.

    References
    ----------
    https://www.onixs.biz/fix-dictionary/5.0.SP2/msgType_F_70.html
    """
    client_order_id: Any
    venue_order_id: Any

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, command_id: Any, ts_init: int, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> CancelOrder:
        """
        Return a cancel order command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        CancelOrder

        """

    @staticmethod
    def to_dict(obj: CancelOrder):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class CancelAllOrders(TradingCommand):
    """
    Represents a command to cancel all orders for an instrument.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    instrument_id : InstrumentId
        The instrument ID for the command.
    order_side : OrderSide
        The order side for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.
    """
    order_side: Any

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, order_side: Any, command_id: Any, ts_init: int, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> CancelAllOrders:
        """
        Return a cancel order command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        CancelAllOrders

        """

    @staticmethod
    def to_dict(obj: CancelAllOrders):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class BatchCancelOrders(TradingCommand):
    """
    Represents a command to batch cancel orders working on a venue for an instrument.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    instrument_id : InstrumentId
        The instrument ID for the command.
    cancels : list[CancelOrder]
        The inner list of cancel order commands.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.

    Raises
    ------
    ValueError
        If `cancels` is empty.
    ValueError
        If `cancels` contains a type other than `CancelOrder`.
    """
    cancels: list

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, cancels: list, command_id: Any, ts_init: int, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> BatchCancelOrders:
        """
        Return a batch cancel order command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        BatchCancelOrders

        """

    @staticmethod
    def to_dict(obj: BatchCancelOrders):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class QueryOrder(TradingCommand):
    """
    Represents a command to query an order.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    strategy_id : StrategyId
        The strategy ID for the command.
    instrument_id : InstrumentId
        The instrument ID for the command.
    client_order_id : ClientOrderId
        The client order ID for the order to query.
    venue_order_id : VenueOrderId or ``None``
        The venue order ID (assigned by the venue) to query.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.
    """
    client_order_id: Any
    venue_order_id: Any

    def __init__(self, trader_id: Any, strategy_id: Any, instrument_id: Any, client_order_id: Any, venue_order_id: Any | None, command_id: Any, ts_init: int, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> QueryOrder:
        """
        Return a query order command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        QueryOrder

        """

    @staticmethod
    def to_dict(obj: QueryOrder):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

class QueryAccount(Any):
    """
    Represents a command to query an account.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the command.
    account_id : AccountId
        The account ID to query.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    client_id : ClientId, optional
        The execution client ID for the command.
    params : dict[str, object], optional
        Additional parameters for the command.
    """
    client_id: Any
    trader_id: Any
    account_id: Any
    params: dict

    def __init__(self, trader_id: Any, account_id: Any, command_id: Any, ts_init: int, client_id: Any=None, params: dict | None | None=None, correlation_id: Any=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def from_dict(values: dict) -> QueryAccount:
        """
        Return a query account command from the given dict values.

        Parameters
        ----------
        values : dict[str, object]
            The values for initialization.

        Returns
        -------
        QueryAccount

        """

    @staticmethod
    def to_dict(obj: QueryAccount):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """