# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
'\nThe `ExecutionEngine` is the central component of the entire execution stack.\n\nThe execution engines primary responsibility is to orchestrate interactions\nbetween the `ExecutionClient` instances, and the rest of the platform. This\nincludes sending commands to, and receiving events from, the trading venue\nendpoints via its registered execution clients.\n\nThe engine employs a simple fan-in fan-out messaging pattern to execute\n`TradingCommand` messages and `OrderEvent` messages.\n\nAlternative implementations can be written on top of the generic engine - which\njust need to override the `execute` and `process` methods.\n'
from nautilus_trader.execution.client import ExecutionClient

class ExecutionEngine(Any):
    """
    Provides a high-performance execution engine for the management of many
    `ExecutionClient` instances, and the asynchronous ingest and distribution of
    trading commands and events.

    Parameters
    ----------
    msgbus : MessageBus
        The message bus for the engine.
    cache : Cache
        The cache for the engine.
    clock : Clock
        The clock for the engine.
    config : ExecEngineConfig, optional
        The configuration for the instance.

    Raises
    ------
    TypeError
        If `config` is not of type `ExecEngineConfig`.
    """
    snapshot_positions_timer_name: str
    debug: bool
    allow_overfills: bool
    manage_own_order_books: bool
    snapshot_orders: bool
    snapshot_positions: bool
    snapshot_positions_interval_secs: float
    purge_closed_orders_interval_mins: object
    purge_closed_orders_buffer_mins: object
    purge_closed_positions_interval_mins: object
    purge_closed_positions_buffer_mins: object
    purge_account_events_interval_mins: object
    purge_account_events_lookback_mins: object
    purge_from_database: bool
    command_count: int
    event_count: int
    report_count: int

    def __init__(self, msgbus: Any, cache: Any, clock: Any, config: Any | None | None=None) -> None:
        ...

    @property
    def reconciliation(self) -> bool:
        """
        Return whether the reconciliation process will be run on start.

        Returns
        -------
        bool

        """

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
        Return the default execution client registered with the engine.

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

    def position_id_count(self, strategy_id: Any) -> int:
        """
        The position ID count for the given strategy ID.

        Parameters
        ----------
        strategy_id : StrategyId
            The strategy ID for the position count.

        Returns
        -------
        int

        """

    def check_integrity(self) -> bool:
        """
        Check integrity of data within the cache and clients.

        Returns
        -------
        bool
            True if checks pass, else False.
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

    def check_residuals(self) -> bool:
        """
        Check for any residual open state and log warnings if found.

        'Open state' is considered to be open orders and open positions.

        Returns
        -------
        bool
            True if residuals exist, else False.

        """

    def get_external_client_ids(self) -> set:
        """
        Returns the configured external client order IDs.

        Returns
        -------
        set[ClientId]

        """

    def get_external_order_claim(self, instrument_id: Any) -> Any:
        """
        Get any external order claim for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the claim.

        Returns
        -------
        StrategyId or ``None``

        """

    def get_external_order_claims_instruments(self) -> set:
        """
        Get all instrument IDs registered for external order claims.

        Returns
        -------
        set[InstrumentId]

        """

    def get_clients_for_orders(self, orders: list) -> set:
        """
        Get all execution clients corresponding to the given orders.

        Parameters
        ----------
        orders : list[Order]
            The orders to locate associated execution clients for.

        Returns
        -------
        set[ExecutionClient]

        """

    def set_manage_own_order_books(self, value: bool) -> None:
        """
        Set the `manage_own_order_books` setting with the given `value`.

        Parameters
        ----------
        value : bool
            The value to set.

        """

    def register_client(self, client: ExecutionClient) -> None:
        """
        Register the given execution client with the execution engine.

        If the `client.venue` is ``None`` and a default routing client has not
        been previously registered then will be registered as such.

        Parameters
        ----------
        client : ExecutionClient
            The execution client to register.

        Raises
        ------
        ValueError
            If `client` is already registered with the execution engine.

        """

    def register_default_client(self, client: ExecutionClient) -> None:
        """
        Register the given client as the default routing client (when a specific
        venue routing cannot be found).

        Any existing default routing client will be overwritten.

        Parameters
        ----------
        client : ExecutionClient
            The client to register.

        """

    def register_venue_routing(self, client: ExecutionClient, venue: Any) -> None:
        """
        Register the given client to route orders to the given venue.

        Any existing client in the routing map for the given venue will be
        overwritten.

        Parameters
        ----------
        venue : Venue
            The venue to route orders to.
        client : ExecutionClient
            The client for the venue routing.

        """

    def register_oms_type(self, strategy: Any) -> None:
        """
        Register the given trading strategies OMS (Order Management System) type.

        Parameters
        ----------
        strategy : Strategy
            The strategy for the registration.

        """

    def register_external_order_claims(self, strategy: Any) -> None:
        """
        Register the given strategies external order claim instrument IDs (if any)

        Parameters
        ----------
        strategy : Strategy
            The strategy for the registration.

        Raises
        ------
        InvalidConfiguration
            If a strategy is already registered to claim external orders for an instrument ID.

        """

    def deregister_client(self, client: ExecutionClient) -> None:
        """
        Deregister the given execution client from the execution engine.

        Parameters
        ----------
        client : ExecutionClient
            The execution client to deregister.

        Raises
        ------
        ValueError
            If `client` is not registered with the execution engine.

        """

    async def reconcile_execution_state(self, timeout_secs: float=10.0) -> bool:
        """
        Reconcile the internal execution state with all execution clients (external state).

        Parameters
        ----------
        timeout_secs : double, default 10.0
            The timeout (seconds) for reconciliation to complete.

        Returns
        -------
        bool
            True if states reconcile within timeout, else False.

        Raises
        ------
        ValueError
            If `timeout_secs` is not positive (> 0).

        """

    def reconcile_execution_report(self, report: Any) -> bool:
        """
        Check the given execution report.

        Parameters
        ----------
        report : ExecutionReport
            The execution report to check.

        Returns
        -------
        bool
            True if reconciliation successful, else False.

        """

    def reconcile_execution_mass_status(self, report: Any) -> None:
        """
        Reconcile the given execution mass status report.

        Parameters
        ----------
        report : ExecutionMassStatus
            The execution mass status report to reconcile.

        """

    def stop_clients(self) -> None:
        """
        Stop the registered clients.
        """

    def load_cache(self) -> None:
        """
        Load the cache up from the execution database.
        """

    def execute(self, command: Any) -> None:
        """
        Execute the given command.

        Parameters
        ----------
        command : Command
            The command to execute.

        """

    def process(self, event: Any) -> None:
        """
        Process the given order event.

        Parameters
        ----------
        event : OrderEvent
            The order event to process.

        """

    def flush_db(self) -> None:
        """
        Flush the execution database which permanently removes all persisted data.

        Warnings
        --------
        Permanent data loss.

        """