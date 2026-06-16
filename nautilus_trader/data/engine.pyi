# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable, Generator
'\nThe `DataEngine` is the central component of the entire data stack.\n\nThe data engines primary responsibility is to orchestrate interactions between\nthe `DataClient` instances, and the rest of the platform. This includes sending\nrequests to, and receiving responses from, data endpoints via its registered\ndata clients.\n\nThe engine employs a simple fan-in fan-out messaging pattern to execute\n`DataCommand` type messages, and process `DataResponse` messages or market data\nobjects.\n\nAlternative implementations can be written on top of the generic engine - which\njust need to override the `execute`, `process`, `send` and `receive` methods.\n'
from dataclasses import dataclass
from datetime import datetime
TimeRangeGenerator = Callable[[int, dict[str, Any]], Generator[int, bool, None]]

class DataEngine(Any):
    """
    Provides a high-performance data engine for managing many `DataClient`
    instances, for the asynchronous ingest of data.

    Parameters
    ----------
    msgbus : MessageBus
        The message bus for the engine.
    cache : Cache
        The cache for the engine.
    clock : Clock
        The clock for the engine.
    config : DataEngineConfig, optional
        The configuration for the instance.
    """
    debug: bool
    command_count: int
    request_count: int
    response_count: int
    data_count: int

    def __init__(self, msgbus: Any, cache: Any, clock: Any, config: Any | None | None=None) -> None:
        ...

    @property
    def registered_clients(self) -> list[Any]:
        """
        Return the execution clients registered with the engine.

        Returns
        -------
        list[ClientId]

        """

    @property
    def default_client(self) -> Any | None:
        """
        Return the default data client registered with the engine.

        Returns
        -------
        ClientId or ``None``

        """

    @property
    def routing_map(self) -> dict[Any, Any]:
        """
        Return the default data client registered with the engine.

        Returns
        -------
        ClientId or ``None``

        """

    def connect(self) -> None:
        """
        Connect the engine by calling connect on all registered clients.
        """

    def disconnect(self) -> None:
        """
        Disconnect the engine by calling disconnect on all registered clients.
        """

    def check_connected(self) -> bool:
        """
        Check all of the engines clients are connected.

        Returns
        -------
        bool
            True if all clients connected, else False.

        """

    def check_disconnected(self) -> bool:
        """
        Check all of the engines clients are disconnected.

        Returns
        -------
        bool
            True if all clients disconnected, else False.

        """

    def get_external_client_ids(self) -> set:
        """
        Returns the configured external client order IDs.

        Returns
        -------
        set[ClientId]

        """

    def register_catalog(self, catalog: Any, name: str='catalog_0') -> None:
        """
        Register the given data catalog with the engine.

        Parameters
        ----------
        catalog : BaseDataCatalog
            The data catalog to register.
        name : str, default 'catalog_0'
            The name of the catalog to register.

        """

    def register_client(self, client: Any) -> None:
        """
        Register the given data client with the data engine.

        Parameters
        ----------
        client : DataClient
            The client to register.

        Raises
        ------
        ValueError
            If `client` is already registered.

        """

    def register_default_client(self, client: Any) -> None:
        """
        Register the given client as the default routing client (when a specific
        venue routing cannot be found).

        Any existing default routing client will be overwritten.

        Parameters
        ----------
        client : DataClient
            The client to register.

        """

    def register_venue_routing(self, client: Any, venue: Any) -> None:
        """
        Register the given client to route messages to the given venue.

        Any existing client in the routing map for the given venue will be
        overwritten.

        Parameters
        ----------
        venue : Venue
            The venue to route messages to.
        client : DataClient
            The client for the venue routing.

        """

    def deregister_client(self, client: Any) -> None:
        """
        Deregister the given data client from the data engine.

        Parameters
        ----------
        client : DataClient
            The data client to deregister.

        """

    def subscribed_custom_data(self) -> list:
        """
        Return the custom data types subscribed to.

        Returns
        -------
        list[DataType]

        """

    def subscribed_instruments(self) -> list:
        """
        Return the instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_order_book_deltas(self) -> list:
        """
        Return the order book delta instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_order_book_depth(self) -> list:
        """
        Return the order book depth instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_quote_ticks(self) -> list:
        """
        Return the quote tick instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_trade_ticks(self) -> list:
        """
        Return the trade tick instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_mark_prices(self) -> list:
        """
        Return the mark price update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_index_prices(self) -> list:
        """
        Return the index price update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_funding_rates(self) -> list:
        """
        Return the funding rate update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_bars(self) -> list:
        """
        Return the bar types subscribed to.

        Returns
        -------
        list[BarType]

        """

    def subscribed_instrument_status(self) -> list:
        """
        Return the status update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_instrument_close(self) -> list:
        """
        Return the close price instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_option_greeks(self) -> list:
        """
        Return the option greeks instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_synthetic_quotes(self) -> list:
        """
        Return the synthetic instrument quotes subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_synthetic_trades(self) -> list:
        """
        Return the synthetic instrument trades subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def stop_clients(self) -> None:
        """
        Stop the registered clients.
        """

    def execute(self, command: Any) -> None:
        """
        Execute the given data command.

        Parameters
        ----------
        command : DataCommand
            The command to execute.

        """

    def process(self, data: Any, historical: bool=False) -> None:
        """
        Process the given data.

        Parameters
        ----------
        data : Data
            The data to process.

        """

    def process_historical(self, data: Any) -> None:
        """
        Process historical data.

        Parameters
        ----------
        data : Data
            The historical data to process.
        """

    def request(self, request: Any) -> None:
        """
        Handle the given request.

        Parameters
        ----------
        request : RequestData
            The request to handle.

        """

    def response(self, response: Any) -> None:
        """
        Handle the given response.

        Parameters
        ----------
        response : DataResponse
            The response to handle.

        """

@dataclass(slots=True)
class RequestWorkflowState:
    start: datetime | None
    end: datetime | None
    original_start_date: datetime | None = None
    identifier: str | None = None
    data_count: int = 0
    has_aggregated_bars: bool = False
    join_request: bool = False
    join_started: bool = False
    time_range_generator_enabled: bool = False
    continuous_future_cursor_ns: int = 0
    continuous_future_primary_bar_type: Any | None = None
    continuous_future_active_source: tuple | None = None
    continuous_future_active_segment_id: Any | None = None

@dataclass(slots=True)
class ContinuousFutureSubscriptionState:
    target_bar_type: Any
    client_id: Any | None
    venue: Any | None
    params: dict
    active_segment_instrument_id: Any | None = None
    next_transition_index: int | None = None
    timer_name: str | None = None

class SnapshotInfo:
    ...

def register_time_range_generator(name: str, function: TimeRangeGenerator):
    ...

def get_time_range_generator(name: str):
    ...

def default_time_range_generator(request: Any):
    """
    Generator that yields (request_start_ns, request_end_ns) tuples for subrequests.

    This generator handles the duration logic and receives data_received feedback via .send().
    """