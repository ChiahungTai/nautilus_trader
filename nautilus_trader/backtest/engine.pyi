# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable, Generator
from decimal import Decimal
import cython
import pandas as pd
from datetime import datetime
from nautilus_trader.accounting.accounts.base import Account
from nautilus_trader.accounting.margin_models import MarginModel
from nautilus_trader.backtest.execution_client import BacktestExecClient
from nautilus_trader.backtest.modules import SimulationModule
from nautilus_trader.cache.base import CacheFacade
from nautilus_trader.cache.cache import Cache
from nautilus_trader.common.actor import Actor
from nautilus_trader.common.component import Logger, LogGuard, MessageBus, TestClock
from nautilus_trader.core.data import Data
from nautilus_trader.core.uuid import UUID4
from nautilus_trader.execution.algorithm import ExecAlgorithm
from nautilus_trader.execution.messages import BatchCancelOrders, CancelAllOrders, CancelOrder, ModifyOrder, TradingCommand
from nautilus_trader.model.book import OrderBook
from nautilus_trader.model.data import Bar, InstrumentStatus, OrderBookDelta, OrderBookDeltas, QuoteTick, TradeTick
from nautilus_trader.model.identifiers import AccountId, ClientId, ClientOrderId, InstrumentId, PositionId, TraderId, Venue
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Currency, Money, Price, Quantity
from nautilus_trader.model.orders.base import Order
from nautilus_trader.model.position import Position
from nautilus_trader.portfolio.base import PortfolioFacade
from nautilus_trader.trading.strategy import Strategy

class BacktestEngine:
    """
    Provides a backtest engine to run a portfolio of strategies over historical
    data.

    Parameters
    ----------
    config : BacktestEngineConfig, optional
        The configuration for the instance.

    Raises
    ------
    TypeError
        If `config` is not of type `BacktestEngineConfig`.
    """

    def __init__(self, config: Any | None | None=None) -> None:
        ...

    def __del__(self) -> None:
        ...

    @property
    def trader_id(self) -> TraderId:
        """
        Return the engines trader ID.

        Returns
        -------
        TraderId

        """

    @property
    def machine_id(self) -> str:
        """
        Return the engines machine ID.

        Returns
        -------
        str

        """

    @property
    def instance_id(self) -> UUID4:
        """
        Return the engines instance ID.

        This is a unique identifier per initialized engine.

        Returns
        -------
        UUID4

        """

    @property
    def kernel(self) -> Any:
        """
        Return the internal kernel for the engine.

        Returns
        -------
        NautilusKernel

        """

    @property
    def logger(self) -> Logger:
        """
        Return the internal logger for the engine.

        Returns
        -------
        Logger

        """

    @property
    def run_config_id(self) -> str | None:
        """
        Return the last backtest engine run config ID.

        Returns
        -------
        str or ``None``

        """

    @property
    def run_id(self) -> UUID4 | None:
        """
        Return the last backtest engine run ID (if run).

        Returns
        -------
        UUID4 or ``None``

        """

    @property
    def iteration(self) -> int:
        """
        Return the backtest engine iteration count.

        Returns
        -------
        int

        """

    @property
    def run_started(self) -> pd.Timestamp | None:
        """
        Return when the last backtest run started (if run).

        Returns
        -------
        pd.Timestamp or ``None``

        """

    @property
    def run_finished(self) -> pd.Timestamp | None:
        """
        Return when the last backtest run finished (if run).

        Returns
        -------
        pd.Timestamp or ``None``

        """

    @property
    def backtest_start(self) -> pd.Timestamp | None:
        """
        Return the last backtest run time range start (if run).

        Returns
        -------
        pd.Timestamp or ``None``

        """

    @property
    def backtest_end(self) -> pd.Timestamp | None:
        """
        Return the last backtest run time range end (if run).

        Returns
        -------
        pd.Timestamp or ``None``

        """

    @property
    def trader(self) -> Any:
        """
        Return the engines internal trader.

        Returns
        -------
        Trader

        """

    @property
    def cache(self) -> CacheFacade:
        """
        Return the engines internal read-only cache.

        Returns
        -------
        CacheFacade

        """

    @property
    def data(self) -> list[Data]:
        """
        Return the engines internal data stream.

        Returns
        -------
        list[Data]

        """

    @property
    def portfolio(self) -> PortfolioFacade:
        """
        Return the engines internal read-only portfolio.

        Returns
        -------
        PortfolioFacade

        """

    def get_log_guard(self) -> Any | LogGuard | None:
        """
        Return the global logging subsystems log guard.

        May return ``None`` if the logging subsystem was already initialized.

        Returns
        -------
        nautilus_pyo3.LogGuard | LogGuard | None

        """

    def list_venues(self) -> list[Venue]:
        """
        Return the venues contained within the engine.

        Returns
        -------
        list[Venue]

        """

    def add_venue(self, venue: Venue, oms_type: Any, account_type: Any, starting_balances: list[Money], base_currency: Currency | None | None=None, default_leverage: Decimal | None | None=None, leverages: dict[InstrumentId, Decimal] | None | None=None, margin_model: MarginModel | None=None, modules: list[SimulationModule] | None | None=None, fill_model: Any | None | None=None, fee_model: Any | None | None=None, latency_model: Any | None | None=None, book_type: Any=..., routing: bool=False, reject_stop_orders: bool=True, support_gtd_orders: bool=True, support_contingent_orders: bool=True, oto_trigger_mode: Any=..., use_position_ids: bool=True, use_random_ids: bool=False, use_reduce_only: bool=True, use_message_queue: bool=True, use_market_order_acks: bool=False, bar_execution: bool=True, bar_adaptive_high_low_ordering: bool=False, trade_execution: bool=True, liquidity_consumption: bool=False, queue_position: bool=False, allow_cash_borrowing: bool=False, frozen_account: bool=False, price_protection_points=None, settlement_prices: dict[InstrumentId, float] | None | None=None) -> None:
        """
        Add a `SimulatedExchange` with the given parameters to the backtest engine.

        Parameters
        ----------
        venue : Venue
            The venue ID.
        oms_type : OmsType {``HEDGING``, ``NETTING``}
            The order management system type for the exchange. If ``HEDGING`` will
            generate new position IDs.
        account_type : AccountType
            The account type for the exchange.
        starting_balances : list[Money]
            The starting account balances (specify one for a single asset account).
        base_currency : Currency, optional
            The account base currency for the client. Use ``None`` for multi-currency accounts.
        default_leverage : Decimal, optional
            The account default leverage (for margin accounts).
        leverages : dict[InstrumentId, Decimal], optional
            The instrument specific leverage configuration (for margin accounts).
        margin_model : MarginModelConfig, optional
            The margin calculation model configuration. Default 'leveraged'.
        modules : list[SimulationModule], optional
            The simulation modules to load into the exchange.
        fill_model : FillModel, optional
            The fill model for the exchange.
        fee_model : FeeModel, optional
            The fee model for the venue.
        latency_model : LatencyModel, optional
            The latency model for the exchange.
        book_type : BookType, default ``BookType.L1_MBP``
            The default order book type.
        routing : bool, default False
            If multi-venue routing should be enabled for the execution client.
        reject_stop_orders : bool, default True
            If stop orders are rejected on submission if trigger price is in the market.
        support_gtd_orders : bool, default True
            If orders with GTD time in force will be supported by the venue.
        support_contingent_orders : bool, default True
            If contingent orders will be supported/respected by the venue.
            If False, then it's expected the strategy will be managing any contingent orders.
        oto_trigger_mode : OtoTriggerMode, default ``OtoTriggerMode.PARTIAL``
            The OTO trigger mode for contingent orders:
            - ``PARTIAL``: release child orders pro-rata to each partial fill (default).
            - ``FULL``: release child orders only once the parent is fully filled.
        use_position_ids : bool, default True
            If venue position IDs will be generated on order fills.
        use_random_ids : bool, default False
            If venue order IDs and position IDs will be random UUID4's.
            Trade IDs are always deterministic and not affected by this flag.
        use_reduce_only : bool, default True
            If the `reduce_only` execution instruction on orders will be honored.
        use_message_queue : bool, default True
            If an internal message queue should be used to process trading commands in sequence after
            they have initially arrived. Setting this to False would be appropriate for real-time
            sandbox environments, where we don't want to introduce additional latency of waiting for
            the next data event before processing the trading command.
        use_market_order_acks : bool, default False
            If OrderAccepted events will be generated for market orders before filling.
        bar_execution : bool, default True
            If bars should be processed by the matching engine(s) (and move the market).
        bar_adaptive_high_low_ordering : bool, default False
            Determines whether the processing order of bar prices is adaptive based on a heuristic.
            This setting is only relevant when `bar_execution` is True.
            If False, bar prices are always processed in the fixed order: Open, High, Low, Close.
            If True, the processing order adapts with the heuristic:
            - If High is closer to Open than Low then the processing order is Open, High, Low, Close.
            - If Low is closer to Open than High then the processing order is Open, Low, High, Close.
        trade_execution : bool, default True
            If trades should be processed by the matching engine(s) (and move the market).
        liquidity_consumption : bool, default False
            If liquidity consumption should be tracked per price level. When enabled, fills
            consume available liquidity which resets when fresh data arrives at that level.
            When disabled, each iteration can fill against the full book liquidity independently.
        queue_position : bool, default False
            If queue position tracking should be enabled for limit orders during trade
            execution mode. When enabled, limit orders only fill after the quantity ahead
            of them (at order placement time) has been traded through or the price level
            is deleted. Requires trade_execution=True.
        allow_cash_borrowing : bool, default False
            If cash accounts should allow borrowing (negative balances).
        frozen_account : bool, default False
            If the account for this exchange is frozen (balances will not change).
        price_protection_points : int, optional
            Defines an exchange-calculated price boundary (in points) to prevent
            marketable orders from executing at excessively aggressive prices.
        settlement_prices : dict[InstrumentId, float], optional
            Map of instrument ID to settlement price for expiring instruments.
            For futures, positions close at this price instead of market.
            For options, the option leg settles at this price.

        Raises
        ------
        ValueError
            If `venue` is already registered with the engine.

        """

    def change_fill_model(self, venue: Venue, model: Any) -> None:
        """
        Change the fill model for the exchange of the given venue.

        Parameters
        ----------
        venue : Venue
            The venue of the simulated exchange.
        model : FillModel
            The fill model to change to.

        """

    def add_instrument(self, instrument: Instrument) -> None:
        """
        Add the instrument to the backtest engine.

        The instrument must be valid for its associated venue. For instance,
        derivative instruments which would trade on margin cannot be added to
        a venue with a ``CASH`` account.

        Parameters
        ----------
        instrument : Instrument
            The instrument to add.

        Raises
        ------
        InvalidConfiguration
            If the venue for the `instrument` has not been added to the engine.
        InvalidConfiguration
            If `instrument` is not valid for its associated venue.

        """

    def add_data(self, data: list, client_id: ClientId | None=None, validate: bool=True, sort: bool=True) -> None:
        """
        Add the given `data` to the backtest engine.

        Parameters
        ----------
        data : list[Data]
            The data to add.
        client_id : ClientId, optional
            The client ID to associate with the data.
        validate : bool, default True
            If `data` should be validated
            (recommended when adding data directly to the engine).
        sort : bool, default True
            If `data` should be sorted by `ts_init` with the rest of the stream after adding
            (recommended when adding data directly to the engine).

        Raises
        ------
        ValueError
            If `data` is empty.
        ValueError
            If `data` contains objects which are not a type of `Data`.
        ValueError
            If `instrument_id` for the data is not found in the cache.
        ValueError
            If `data` elements do not have an `instrument_id` and `client_id` is ``None``.
        TypeError
            If `data` is a Rust PyO3 data type (cannot add directly to engine yet).

        Warnings
        --------
        Assumes all data elements are of the same type. Adding lists of varying
        data types could result in incorrect backtest logic.

        Caution if adding data without `sort` being True, as this could lead to running backtests
        on a stream which does not have monotonically increasing timestamps.

        Notes
        -----
        For optimal performance when loading large datasets, consider using `sort=False` for all
        calls to `add_data()`, then calling `sort_data()` once after all data has been added:

        .. code-block:: python

            # Add multiple data streams without sorting
            engine.add_data(instrument1_bars, sort=False)
            engine.add_data(instrument2_bars, sort=False)
            engine.add_data(instrument3_bars, sort=False)

            # Sort once at the end
            engine.sort_data()

        This approach avoids repeatedly sorting the entire data stream on each call,
        significantly reducing load time for large datasets.

        **Contract invariants:**

        - When `sort=True`: Data is immediately available for backtesting via `run()`.
        - When `sort=False`: You **must** call `sort_data()` or add data with `sort=True` before `run()`.
        - The provided `data` list is always copied internally to prevent external mutations from affecting the engine state.

        """

    def add_data_iterator(self, data_name: str, generator: Generator[list[Data], None, None], client_id: ClientId | None=None) -> None:
        """
        Add a single stream generator that yields ``list[Data]`` objects for the low-level streaming backtest API.

        Parameters
        ----------
        data_name : str
            The name identifier for the data stream.
        generator : Generator[list[Data], None, None]
            A Python generator that yields lists of ``Data`` objects.
        client_id : ClientId, optional
            The client ID to associate with the data.

        Notes
        -----
        This method enables streaming large datasets by loading data in chunks.
        The generator should yield ``list[Data]`` objects sorted by `ts_init` timestamp.

        """

    def dump_pickled_data(self) -> bytes:
        """
        Return the internal data stream pickled.

        Returns
        -------
        bytes

        """

    def load_pickled_data(self, data: bytes) -> None:
        """
        Load the given pickled data directly into the internal data stream.

        It is highly advised to only pass data to this method which was obtained
        through a call to `.dump_pickled_data()`.

        Warnings
        --------
        This low-level direct access method makes the following assumptions:
         - The data contains valid Nautilus objects only, which inherit from `Data`.
         - The data was successfully pickled from a call to `pickle.dumps()`.
         - The data was sorted prior to pickling.
         - All required instruments have been added to the engine.

        """

    def add_actor(self, actor: Actor) -> None:
        """
        Add the given actor to the backtest engine.

        Parameters
        ----------
        actor : Actor
            The actor to add.

        """

    def add_actors(self, actors: list[Actor]) -> None:
        """
        Add the given list of actors to the backtest engine.

        Parameters
        ----------
        actors : list[Actor]
            The actors to add.

        """

    def add_strategy(self, strategy: Strategy) -> None:
        """
        Add the given strategy to the backtest engine.

        Parameters
        ----------
        strategy : Strategy
            The strategy to add.

        """

    def add_strategies(self, strategies: list[Strategy]) -> None:
        """
        Add the given list of strategies to the backtest engine.

        Parameters
        ----------
        strategies : list[Strategy]
            The strategies to add.

        """

    def add_exec_algorithm(self, exec_algorithm: ExecAlgorithm) -> None:
        """
        Add the given execution algorithm to the backtest engine.

        Parameters
        ----------
        exec_algorithm : ExecAlgorithm
            The execution algorithm to add.

        """

    def add_exec_algorithms(self, exec_algorithms: list[ExecAlgorithm]) -> None:
        """
        Add the given list of execution algorithms to the backtest engine.

        Parameters
        ----------
        exec_algorithms : list[ExecAlgorithm]
            The execution algorithms to add.

        """

    def reset(self) -> None:
        """
        Reset the backtest engine.

        All stateful fields are reset to their initial value, except for data and instruments which persist.

        Notes
        -----
        Data and instruments are retained across resets by default to enable repeated runs
        with different strategies or parameters against the same dataset.

        See Also
        --------
        https://nautilustrader.io/docs/concepts/backtesting#repeated-runs

        """

    def sort_data(self) -> None:
        """
        Sort the engines internal data stream.

        """

    def clear_data(self) -> None:
        """
        Clear the engines internal data stream.

        Does not clear added instruments.

        """

    def clear_actors(self) -> None:
        """
        Clear all actors from the engines internal trader.

        """

    def clear_strategies(self) -> None:
        """
        Clear all trading strategies from the engines internal trader.

        """

    def clear_exec_algorithms(self) -> None:
        """
        Clear all execution algorithms from the engines internal trader.

        """

    def dispose(self) -> None:
        """
        Dispose of the backtest engine by disposing the trader and releasing system resources.

        Calling this method multiple times has the same effect as calling it once (it is idempotent).
        Once called, it cannot be reversed, and no other methods should be called on this instance.

        """

    def run(self, start: datetime | str | int | None | None=None, end: datetime | str | int | None | None=None, run_config_id: str | None | None=None, streaming: bool=False) -> None:
        """
        Run a backtest.

        When ``streaming`` is False (default), the run is finalized via
        ``end()`` which stops all engines and produces results. When True,
        the run pauses without finalizing so additional data batches can be
        loaded. Timer advancement stops at data exhaustion to avoid producing
        synthetic events (e.g. zero-volume bars) past the current batch.

        For datasets larger than available memory, use ``streaming`` mode::

            engine.add_strategy(strategy)

            for batch in data_batches:
                engine.add_data(batch)
                engine.run(streaming=True)
                engine.clear_data()

            engine.end()

        Parameters
        ----------
        start : datetime or str or int, optional
            The start datetime (UTC) for the backtest run.
            If ``None`` engine runs from the start of the data.
        end : datetime or str or int, optional
            The end datetime (UTC) for the backtest run.
            If ``None`` engine runs to the end of the data.
        run_config_id : str, optional
            The tokenized `BacktestRunConfig` ID.
        streaming : bool, default False
            If False (default), calls ``end()`` after the run to stop
            engines and produce results.
            If True, pauses after data exhaustion without finalizing.
            Call ``end()`` manually after all batches are processed.

        Raises
        ------
        ValueError
            If no data has been added to the engine.
        ValueError
            If the `start` is >= the `end` datetime.
        RuntimeError
            If data has been added with `sort=False` but `sort_data()` has not been called.

        Notes
        -----
        **Contract invariants:**

        - All data added via `add_data()` must be sorted and synced to the internal iterator before calling `run()`.
        - If any data was added with `sort=False`, you must call `sort_data()` or add data with `sort=True` before this method.
        - The engine validates this requirement and will raise `RuntimeError` if unsorted data is detected.

        """

    def end(self):
        """
        Manually end the backtest.

        Notes
        -----
        Only required if you have previously been running with streaming.

        """

    def get_result(self):
        """
        Return the backtest result from the last run.

        Returns
        -------
        BacktestResult

        """

    def set_default_market_data_client(self) -> None:
        ...

class BacktestDataIterator:
    """
    Time-ordered multiplexer for historical ``Data`` streams in backtesting.

    The iterator efficiently manages multiple data streams and yields ``Data`` objects
    in strict chronological order based on their ``ts_init`` timestamps. It supports
    both static data lists and dynamic data generators for streaming large datasets.

    **Architecture:**

    - **Single-stream optimization**: When exactly one stream is loaded, uses a fast
      array walk for optimal performance.
    - **Multi-stream merging**: With two or more streams, employs a binary min-heap
      to perform efficient k-way merge sorting.
    - **Dynamic streaming**: Supports Python generators that yield data chunks on-demand,
      enabling processing of datasets larger than available memory.

    **Stream Priority:**

    Streams can be assigned different priorities using the ``append_data`` parameter:

    - ``append_data=True`` (default): Lower priority, processed after existing streams
    - ``append_data=False``: Higher priority, processed before existing streams

    When multiple data points have identical timestamps, higher priority streams
    are yielded first.

    **Performance Characteristics:**

    - **Memory efficient**: Dynamic generators load data incrementally
    - **Time complexity**: O(log n) per item for n streams (heap operations)
    - **Space complexity**: O(k) where k is the total number of active data points
      across all streams at any given time

    Notes
    -----
    When using ``add_data()`` with ``presorted=False`` (default), the data will be
    sorted internally. When using ``presorted=True`` or ``init_data()``, the data
    must be pre-sorted by ``ts_init`` in ascending order.

    See Also
    --------
    BacktestEngine.add_data : Add static data to the backtest engine
    BacktestEngine.add_data_iterator : Add streaming data generators

    """

    def __init__(self) -> None:
        ...

    def add_data(self, data_name: str, data: list, append_data: bool=True, presorted: bool=False) -> None:
        """
        Add (or replace) a named data list for static data loading.

        If a stream with the same ``data_name`` already exists, it will be replaced
        with the new data.

        Parameters
        ----------
        data_name : str
            Unique identifier for the data stream.
        data : list[Data]
            Data instances to add. Must be pre-sorted by `ts_init` if ``presorted=True``.
        append_data : bool, default ``True``
            Controls stream priority for timestamp ties:
            ``True`` – lower priority (appended).
            ``False`` – higher priority (prepended).
        presorted : bool, default ``False``
            If ``True``, assumes the data is already sorted by `ts_init` and
            skips internal sorting for better performance. If ``False`` (default),
            the data will be sorted internally.

        Raises
        ------
        ValueError
            If `data_name` is not a valid string.

        """

    def init_data(self, data_name: str, data_generator, append_data: bool=True) -> None:
        """
        Add (or replace) a named data generator for streaming large datasets.

        This method enables memory-efficient processing of large datasets by using
        Python generators that yield data chunks on-demand. The generator is called
        incrementally as data is consumed, allowing datasets larger than available
        memory to be processed.

        The generator should yield lists of ``Data`` objects, where each list represents
        a chunk of data. When a chunk is exhausted, the iterator automatically calls
        ``next()`` on the generator to fetch the next chunk.

        Parameters
        ----------
        data_name : str
            Unique identifier for the data stream.
        data_generator : Generator[list[Data], None, None]
            A Python generator that yields lists of ``Data`` instances sorted ascending by `ts_init`.
        append_data : bool, default ``True``
            Controls stream priority for timestamp ties:
            ``True`` – lower priority (appended).
            ``False`` – higher priority (prepended).

        Raises
        ------
        ValueError
            If `data_name` is not a valid string.

        """

    def remove_data(self, data_name: str, complete_remove: bool=False) -> None:
        """
        Remove the data stream identified by ``data_name``. The operation is silently
        ignored if the specified stream does not exist.

        Parameters
        ----------
        data_name : str
            The unique identifier of the data stream to remove.
        complete_remove : bool, default False
            Controls the level of cleanup performed:
            - ``False``: Remove stream data but preserve generator function for potential
              re-initialization (useful for temporary stream removal)
            - ``True``: Complete removal including any associated generator function
              (recommended for permanent stream removal)

        Raises
        ------
        ValueError
            If `data_name` is not a valid string.

        """

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def next(self) -> Data | None:
        """
        Return the next ``Data`` object in chronological order.

        This method implements the core iteration logic, yielding data points from
        all streams in strict chronological order based on ``ts_init`` timestamps.
        When multiple data points have identical timestamps, stream priority
        determines the order.

        The method automatically handles:
        - Single-stream optimization for performance
        - Multi-stream heap-based merging
        - Dynamic data loading from generators
        - Stream exhaustion and cleanup

        Returns
        -------
        Data or None
            The next ``Data`` object in chronological order, or ``None`` when
            all streams are exhausted.

        Notes
        -----
        - Returns ``None`` when all streams are exhausted
        - Automatically triggers generator calls for streaming data
        - Performance is optimized for single-stream scenarios
        - Thread-safe only when called from a single thread

        """

    def set_index(self, data_name: str, index: int) -> None:
        """
        Move the cursor of `data_name` to `index` and rebuild ordering.

        Raises
        ------
        ValueError
            If `data_name` is not a valid string.

        """

    def is_done(self) -> bool:
        """
        Return ``True`` when every stream has been fully consumed.
        """

    def all_data(self) -> dict:
        """
        Return a *shallow* mapping of ``{stream_name: list[Data]}``.
        """

    def data(self, data_name: str) -> list:
        """
        Return the underlying data list for `data_name`.

        Returns
        -------
        list[Data]

        Raises
        ------
        ValueError
            If `data_name` is not a valid string.
        KeyError
            If the stream is unknown.

        """

    def __iter__(self):
        ...

    def __next__(self):
        ...

class SimulatedExchange:
    """
    Provides a simulated exchange venue.

    Parameters
    ----------
    venue : Venue
        The venue to simulate.
    oms_type : OmsType {``HEDGING``, ``NETTING``}
        The order management system type used by the exchange.
    account_type : AccountType
        The account type for the client.
    starting_balances : list[Money]
        The starting balances for the exchange.
    base_currency : Currency, optional
        The account base currency for the client. Use ``None`` for multi-currency accounts.
    default_leverage : Decimal
        The account default leverage (for margin accounts).
    leverages : dict[InstrumentId, Decimal]
        The instrument specific leverage configuration (for margin accounts).
    modules : list[SimulationModule]
        The simulation modules for the exchange.
    portfolio : PortfolioFacade
        The read-only portfolio for the exchange.
    msgbus : MessageBus
        The message bus for the exchange.
    cache : CacheFacade
        The read-only cache for the exchange.
    clock : TestClock
        The clock for the exchange.
    fill_model : FillModel
        The fill model for the exchange.
    fee_model : FeeModel
        The fee model for the exchange.
    latency_model : LatencyModel, optional
        The latency model for the exchange.
    book_type : BookType
        The order book type for the exchange.
    frozen_account : bool, default False
        If the account for this exchange is frozen (balances will not change).
    reject_stop_orders : bool, default True
        If stop orders are rejected on submission if in the market.
    support_gtd_orders : bool, default True
        If orders with GTD time in force will be supported by the exchange.
    support_contingent_orders : bool, default True
        If contingent orders will be supported/respected by the exchange.
        If False, then its expected the strategy will be managing any contingent orders.
    oto_trigger_mode : OtoTriggerMode, default ``OtoTriggerMode.PARTIAL``
        The OTO trigger mode for contingent orders:
        - ``PARTIAL``: release child orders pro-rata to each partial fill (default).
        - ``FULL``: release child orders only once the parent is fully filled.
    use_position_ids : bool, default True
        If venue position IDs will be generated on order fills.
    use_random_ids : bool, default False
        If all exchange generated identifiers will be random UUID4's.
    use_reduce_only : bool, default True
        If the `reduce_only` execution instruction on orders will be honored.
    use_message_queue : bool, default True
        If an internal message queue should be used to process trading commands in sequence after
        they have initially arrived. Setting this to False would be appropriate for real-time
        sandbox environments, where we don't want to introduce additional latency of waiting for
        the next data event before processing the trading command.
    use_market_order_acks : bool, default False
        If OrderAccepted events will be generated for market orders before filling.
    bar_execution : bool, default True
        If bars should be processed by the matching engine(s) (and move the market).
    bar_adaptive_high_low_ordering : bool, default False
        Determines whether the processing order of bar prices is adaptive based on a heuristic.
        This setting is only relevant when `bar_execution` is True.
        If False, bar prices are always processed in the fixed order: Open, High, Low, Close.
        If True, the processing order adapts with the heuristic:
        - If High is closer to Open than Low then the processing order is Open, High, Low, Close.
        - If Low is closer to Open than High then the processing order is Open, Low, High, Close.
    price_protection_points : int, optional
        Defines an exchange-calculated price boundary (in points) to prevent
        marketable orders from executing at excessively aggressive prices.
    trade_execution : bool, default True
        If trades should be processed by the matching engine(s) (and move the market).
    liquidity_consumption : bool, default False
        If liquidity consumption should be tracked per price level. When enabled, fills
        consume available liquidity which resets when fresh data arrives at that level.
        When disabled, each iteration can fill against the full book liquidity independently.
    queue_position : bool, default False
        If queue position tracking should be enabled for limit orders during trade
        execution mode. When enabled, limit orders only fill after the quantity ahead
        of them (at order placement time) has been traded through or the price level
        is deleted. Requires trade_execution=True.
    settlement_prices : dict[InstrumentId, float], optional
        Map of instrument ID to settlement price for expiring instruments.
        For futures, positions close at this price instead of market.
        For options, the option leg settles at this price.

    Raises
    ------
    ValueError
        If `instruments` is empty.
    ValueError
        If `instruments` contains a type other than `Instrument`.
    ValueError
        If `starting_balances` is empty.
    ValueError
        If `starting_balances` contains a type other than `Money`.
    ValueError
        If `base_currency` and multiple starting balances.
    ValueError
        If `modules` contains a type other than `SimulationModule`.

    """
    id: Venue
    oms_type: Any
    book_type: Any
    msgbus: MessageBus
    cache: Cache
    exec_client: BacktestExecClient
    account_type: Any
    base_currency: Currency
    starting_balances: list
    default_leverage: Any
    leverages: dict
    margin_model: MarginModel
    is_frozen_account: bool
    latency_model: Any
    fill_model: Any
    fee_model: Any
    reject_stop_orders: bool
    support_gtd_orders: bool
    support_contingent_orders: bool
    oto_full_trigger: bool
    use_position_ids: bool
    use_random_ids: bool
    use_reduce_only: bool
    use_message_queue: bool
    use_market_order_acks: bool
    bar_execution: bool
    bar_adaptive_high_low_ordering: bool
    trade_execution: bool
    liquidity_consumption: bool
    queue_position: bool
    price_protection_points: int
    modules: list
    instruments: dict

    def __init__(self, venue: Venue, oms_type: Any, account_type: Any, starting_balances: list, base_currency: Currency | None, default_leverage: Decimal, leverages: dict[InstrumentId, Decimal], modules: list, portfolio: PortfolioFacade, msgbus: MessageBus, cache: CacheFacade, clock: TestClock, fill_model: Any, fee_model: Any, latency_model: Any=None, margin_model: MarginModel | None=None, book_type: Any=..., frozen_account: bool=False, reject_stop_orders: bool=True, support_gtd_orders: bool=True, support_contingent_orders: bool=True, oto_trigger_mode: Any=..., use_position_ids: bool=True, use_random_ids: bool=False, use_reduce_only: bool=True, use_message_queue: bool=True, use_market_order_acks: bool=False, bar_execution: bool=True, bar_adaptive_high_low_ordering: bool=False, trade_execution: bool=True, liquidity_consumption: bool=False, queue_position: bool=False, price_protection_points=None, settlement_prices: dict[InstrumentId, float] | None | None=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def register_client(self, client: BacktestExecClient) -> None:
        """
        Register the given execution client with the simulated exchange.

        Parameters
        ----------
        client : BacktestExecClient
            The client to register

        """

    def set_fill_model(self, fill_model: Any) -> None:
        """
        Set the fill model for all matching engines.

        Parameters
        ----------
        fill_model : FillModel
            The fill model to set.

        """

    def set_latency_model(self, latency_model: Any) -> None:
        """
        Change the latency model for this exchange.

        Parameters
        ----------
        latency_model : LatencyModel
            The latency model to set.

        """

    def initialize_account(self) -> None:
        """
        Initialize the account to the starting balances.

        """

    def add_instrument(self, instrument: Instrument) -> None:
        """
        Add the given instrument to the exchange.

        Parameters
        ----------
        instrument : Instrument
            The instrument to add.

        Raises
        ------
        ValueError
            If `instrument.id.venue` is not equal to the venue ID.
        InvalidConfiguration
            If `instrument` is invalid for this venue.

        """

    def best_bid_price(self, instrument_id: InstrumentId) -> Price | None:
        """
        Return the best bid price for the given instrument ID (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the price.

        Returns
        -------
        Price or ``None``

        """

    def best_ask_price(self, instrument_id: InstrumentId) -> Price | None:
        """
        Return the best ask price for the given instrument ID (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the price.

        Returns
        -------
        Price or ``None``

        """

    def get_book(self, instrument_id: InstrumentId) -> OrderBook | None:
        """
        Return the order book for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the price.

        Returns
        -------
        OrderBook or ``None``

        """

    def get_matching_engine(self, instrument_id: InstrumentId) -> OrderMatchingEngine | None:
        """
        Return the matching engine for the given instrument ID (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the matching engine.

        Returns
        -------
        OrderMatchingEngine or ``None``

        """

    def get_matching_engines(self) -> dict:
        """
        Return all matching engines for the exchange (for every instrument).

        Returns
        -------
        dict[InstrumentId, OrderMatchingEngine]

        """

    def get_books(self) -> dict:
        """
        Return all order books within the exchange.

        Returns
        -------
        dict[InstrumentId, OrderBook]

        """

    def get_open_orders(self, instrument_id: InstrumentId | None=None) -> list:
        """
        Return the open orders at the exchange.

        Parameters
        ----------
        instrument_id : InstrumentId, optional
            The instrument_id query filter.

        Returns
        -------
        list[Order]

        """

    def get_open_bid_orders(self, instrument_id: InstrumentId | None=None) -> list:
        """
        Return the open bid orders at the exchange.

        Parameters
        ----------
        instrument_id : InstrumentId, optional
            The instrument_id query filter.

        Returns
        -------
        list[Order]

        """

    def get_open_ask_orders(self, instrument_id: InstrumentId | None=None) -> list:
        """
        Return the open ask orders at the exchange.

        Parameters
        ----------
        instrument_id : InstrumentId, optional
            The instrument_id query filter.

        Returns
        -------
        list[Order]

        """

    def get_account(self) -> Account | None:
        """
        Return the account for the registered client (if registered).

        Returns
        -------
        Account or ``None``

        """

    def adjust_account(self, adjustment: Money) -> None:
        """
        Adjust the account at the exchange with the given adjustment.

        Parameters
        ----------
        adjustment : Money
            The adjustment for the account.

        """

    def update_instrument(self, instrument: Instrument) -> None:
        """
        Update the venues current instrument definition with the given instrument.

        Parameters
        ----------
        instrument : Instrument
            The instrument definition to update.

        """

    def send(self, command: TradingCommand) -> None:
        """
        Send the given trading command into the exchange.

        Parameters
        ----------
        command : TradingCommand
            The command to send.

        """

    def process_order_book_delta(self, delta: OrderBookDelta) -> None:
        """
        Process the exchanges market for the given order book delta.

        Parameters
        ----------
        data : OrderBookDelta
            The order book delta to process.

        """

    def process_order_book_deltas(self, deltas: OrderBookDeltas) -> None:
        """
        Process the exchanges market for the given order book deltas.

        Parameters
        ----------
        data : OrderBookDeltas
            The order book deltas to process.

        """

    def process_order_book_depth10(self, depth: Any) -> None:
        """
        Process the exchanges market for the given order book depth.

        Parameters
        ----------
        depth : OrderBookDepth10
            The order book depth to process.

        """

    def process_quote_tick(self, tick: QuoteTick) -> None:
        """
        Process the exchanges market for the given quote tick.

        Market dynamics are simulated by auctioning open orders.

        Parameters
        ----------
        tick : QuoteTick
            The tick to process.

        """

    def process_trade_tick(self, tick: TradeTick) -> None:
        """
        Process the exchanges market for the given trade tick.

        Market dynamics are simulated by auctioning open orders.

        Parameters
        ----------
        tick : TradeTick
            The tick to process.

        """

    def process_bar(self, bar: Bar) -> None:
        """
        Process the exchanges market for the given bar.

        Market dynamics are simulated by auctioning open orders.

        Parameters
        ----------
        bar : Bar
            The bar to process.

        """

    def process_instrument_status(self, data: InstrumentStatus) -> None:
        """
        Process a specific instrument status.

        Parameters
        ----------
        data : InstrumentStatus
            The instrument status update to process.

        """

    def process_instrument_close(self, close: Any) -> None:
        """
        Process the exchanges market for the given instrument close.

        Parameters
        ----------
        close : InstrumentClose
            The instrument close to process.

        """

    def process(self, ts_now: int) -> None:
        """
        Process the exchange to the given time.

        All pending commands will be processed along with all simulation modules.

        Parameters
        ----------
        ts_now : uint64_t
            The current UNIX timestamp (nanoseconds).

        """

    def reset(self) -> None:
        """
        Reset the simulated exchange.

        All stateful fields are reset to their initial value.
        """

class OrderMatchingEngine:
    """
    Provides an order matching engine for a single market.

    Parameters
    ----------
    instrument : Instrument
        The market instrument for the matching engine.
    raw_id : uint32_t
        The raw integer ID for the instrument.
    fill_model : FillModel
        The fill model for the matching engine.
    fee_model : FeeModel
        The fee model for the matching engine.
    book_type : BookType
        The order book type for the engine.
    oms_type : OmsType
        The order management system type for the matching engine. Determines
        the generation and handling of venue position IDs.
    account_type : AccountType
        The account type for the matching engine. Determines allowable
        executions based on the instrument.
    msgbus : MessageBus
        The message bus for the matching engine.
    cache : CacheFacade
        The read-only cache for the matching engine.
    clock : TestClock
        The clock for the matching engine.
    logger : Logger
        The logger for the matching engine.
    bar_execution : bool, default True
        If bars should be processed by the matching engine (and move the market).
    trade_execution : bool, default True
        If trades should be processed by the matching engine (and move the market).
    liquidity_consumption : bool, default False
        If liquidity consumption should be tracked per price level.
    reject_stop_orders : bool, default True
        If stop orders are rejected if already in the market on submitting.
    support_gtd_orders : bool, default True
        If orders with GTD time in force will be supported by the venue.
    support_contingent_orders : bool, default True
        If contingent orders will be supported/respected by the venue.
        If False, then its expected the strategy will be managing any contingent orders.
    use_position_ids : bool, default True
        If venue position IDs will be generated on order fills.
    use_random_ids : bool, default False
        If venue order IDs and position IDs will be random UUID4's.
        Trade IDs are always deterministic and not affected by this flag.
    use_reduce_only : bool, default True
        If the `reduce_only` execution instruction on orders will be honored.
    bar_adaptive_high_low_ordering : bool, default False
        Determines whether the processing order of bar prices is adaptive based on a heuristic.
        This setting is only relevant when `bar_execution` is True.
        If False, bar prices are always processed in the fixed order: Open, High, Low, Close.
        If True, the processing order adapts with the heuristic:
        - If High is closer to Open than Low then the processing order is Open, High, Low, Close.
        - If Low is closer to Open than High then the processing order is Open, Low, High, Close.
    settlement_prices : dict[InstrumentId, float], optional
        Map of instrument ID to settlement price for expiring instruments.
        For futures, positions close at this price instead of market.
        For options, the option leg settles at this price.

    """
    venue: Venue
    instrument: Instrument
    raw_id: int
    book_type: Any
    oms_type: Any
    account_type: Any
    market_status: Any
    cache: CacheFacade
    msgbus: MessageBus

    def __init__(self, instrument: Instrument, raw_id: int, fill_model: Any, fee_model: Any, book_type: Any, oms_type: Any, account_type: Any, msgbus: MessageBus, cache: CacheFacade, clock: TestClock, reject_stop_orders: bool=True, support_gtd_orders: bool=True, support_contingent_orders: bool=True, oto_full_trigger: bool=False, use_position_ids: bool=True, use_random_ids: bool=False, use_reduce_only: bool=True, use_market_order_acks: bool=False, bar_execution: bool=True, bar_adaptive_high_low_ordering: bool=False, trade_execution: bool=True, liquidity_consumption: bool=False, queue_position: bool=False, price_protection_points=None, settlement_prices: dict[InstrumentId, float] | None | None=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def reset(self) -> None:
        ...

    def set_fill_model(self, fill_model: Any) -> None:
        """
        Set the fill model to the given model.

        Parameters
        ----------
        fill_model : FillModel
            The fill model to set.

        """

    def update_instrument(self, instrument: Instrument) -> None:
        """
        Update the matching engines current instrument definition with the given instrument.

        Parameters
        ----------
        instrument : Instrument
            The instrument definition to update.

        """

    def best_bid_price(self) -> Price | None:
        """
        Return the best bid price for the given instrument ID (if found).

        Returns
        -------
        Price or ``None``

        """

    def best_ask_price(self) -> Price | None:
        """
        Return the best ask price for the given instrument ID (if found).

        Returns
        -------
        Price or ``None``

        """

    def get_book(self) -> OrderBook:
        """
        Return the internal order book.

        Returns
        -------
        OrderBook

        """

    def get_open_orders(self) -> list:
        """
        Return the open orders in the matching engine.

        Returns
        -------
        list[Order]

        """

    def get_open_bid_orders(self) -> list:
        """
        Return the open bid orders in the matching engine.

        Returns
        -------
        list[Order]

        """

    def get_open_ask_orders(self) -> list:
        """
        Return the open ask orders at the exchange.

        Returns
        -------
        list[Order]

        """

    def order_exists(self, client_order_id: ClientOrderId) -> bool:
        ...

    def process_order_book_delta(self, delta: OrderBookDelta) -> None:
        """
        Process the exchanges market for the given order book delta.

        Parameters
        ----------
        delta : OrderBookDelta
            The order book delta to process.

        Raises
        ------
        RuntimeError
            If the delta price precision does not match the instrument for the matching engine.
        RuntimeError
            If the delta size precision does not match the instrument for the matching engine.

        """

    def process_order_book_deltas(self, deltas: OrderBookDeltas) -> None:
        """
        Process the exchanges market for the given order book deltas.

        Parameters
        ----------
        delta : OrderBookDeltas
            The order book deltas to process.

        Raises
        ------
        RuntimeError
            If any delta price precision does not match the instrument for the matching engine.
        RuntimeError
            If any delta size precision does not match the instrument for the matching engine.

        """

    def process_order_book_depth10(self, depth: Any) -> None:
        """
        Process the exchanges market for the given order book depth.

        Parameters
        ----------
        depth : OrderBookDepth10
            The order book depth to process.

        Raises
        ------
        RuntimeError
            If any order price precision does not match the instrument for the matching engine.
        RuntimeError
            If any order size precision does not match the instrument for the matching engine.

        """

    def process_quote_tick(self, tick: QuoteTick) -> None:
        """
        Process the exchanges market for the given quote tick.

        The internal order book will only be updated if the venue `book_type` is 'L1_MBP'.

        Parameters
        ----------
        tick : QuoteTick
            The tick to process.

        Raises
        ------
        RuntimeError
            If a price precision does not match the instrument for the matching engine.
        RuntimeError
            If a size precision does not match the instrument for the matching engine.

        """

    def process_trade_tick(self, tick: TradeTick) -> None:
        """
        Process the exchanges market for the given trade tick.

        The internal order book is always updated if the venue `book_type` is 'L1_MBP'.
        When `trade_execution` is disabled, the trade tick updates market state (book and
        last price) but does not trigger order matching or maintenance operations (GTD
        order expiry, trailing stop activation, instrument expiration checks). These
        maintenance operations will run on the next quote tick or bar. When `trade_execution`
        is enabled, resting orders can fill against the trade price.

        Parameters
        ----------
        tick : TradeTick
            The tick to process.

        Raises
        ------
        RuntimeError
            If the trades price precision does not match the instrument for the matching engine.
        RuntimeError
            If the trades size precision does not match the instrument for the matching engine.

        """

    def process_bar(self, bar: Bar) -> None:
        """
        Process the exchanges market for the given bar.

        Market dynamics are simulated by auctioning open orders.

        Parameters
        ----------
        bar : Bar
            The bar to process.

        Raises
        ------
        RuntimeError
            If a price precision does not match the instrument for the matching engine.
        RuntimeError
            If a size precision does not match the instrument for the matching engine.

        """

    def process_status(self, status: Any) -> None:
        """
        Process the exchange status.

        Parameters
        ----------
        status : MarketStatusAction
            The status action to process.

        """

    def process_instrument_close(self, close: Any) -> None:
        """
        Process the instrument close.

        Parameters
        ----------
        close : InstrumentClose
            The close price to process.

        """

    def process_order(self, order: Order, account_id: AccountId) -> None:
        ...

    def process_modify(self, command: ModifyOrder, account_id: AccountId) -> None:
        ...

    def process_cancel(self, command: CancelOrder, account_id: AccountId) -> None:
        ...

    def process_batch_cancel(self, command: BatchCancelOrders, account_id: AccountId) -> None:
        ...

    def process_cancel_all(self, command: CancelAllOrders, account_id: AccountId) -> None:
        ...

    def iterate(self, timestamp_ns: int, aggressor_side: Any=...) -> None:
        """
        Iterate the matching engine by processing the bid and ask order sides
        and advancing time up to the given UNIX `timestamp_ns`.

        Parameters
        ----------
        timestamp_ns : uint64_t
            UNIX timestamp to advance the matching engine time to.
        aggressor_side : AggressorSide, default 'NO_AGGRESSOR'
            The aggressor side for trade execution processing.

        """

    def check_instrument_expiration(self, timestamp_ns: int) -> None:
        """Run instrument expiration at timestamp_ns (option exercise/expiry or futures close)."""

    def fill_market_order(self, order: Order) -> None:
        """
        Fill the given *marketable* order.

        Parameters
        ----------
        order : Order
            The order to fill.

        """

    def determine_market_price_and_volume(self, order: Order) -> list:
        """
        Return the projected fills for the given *marketable* order filling
        aggressively into the opposite order side.

        The list may be empty if no fills.

        Parameters
        ----------
        order : Order
            The order to determine fills for.

        Returns
        -------
        list[tuple[Price, Quantity]]

        """

    def fill_limit_order(self, order: Order) -> None:
        """
        Fill the given limit order.

        Parameters
        ----------
        order : Order
            The order to fill.

        Raises
        ------
        ValueError
            If the `order` does not have a LIMIT `price`.

        """

    def determine_limit_price_and_volume(self, order: Order) -> list:
        """
        Return the projected fills for the given *limit* order filling passively
        from its limit price.

        The list may be empty if no fills.

        Parameters
        ----------
        order : Order
            The order to determine fills for.

        Returns
        -------
        list[tuple[Price, Quantity]]

        Raises
        ------
        ValueError
            If the `order` does not have a LIMIT `price`.

        """

    def apply_fills(self, order: Order, fills: list, liquidity_side: Any, venue_position_id: PositionId | None | None=None, position: Position | None | None=None, protection_price: Price | None | None=None) -> None:
        """
        Apply the given list of fills to the given order. Optionally provide
        existing position details.

        - If the `fills` list is empty, an error will be logged.
        - Market orders will be rejected if no opposing orders are available to fulfill them.

        Parameters
        ----------
        order : Order
            The order to fill.
        fills : list[tuple[Price, Quantity]]
            The fills to apply to the order.
        liquidity_side : LiquiditySide
            The liquidity side for the fill(s).
        venue_position_id :  PositionId, optional
            The current venue position ID related to the order (if assigned).
        position : Position, optional
            The current position related to the order (if any).
        protection_price : Price, optional
            The protection price boundary for market/stop-market orders.

        Raises
        ------
        ValueError
            If `liquidity_side` is ``NO_LIQUIDITY_SIDE``.

        Warnings
        --------
        The `liquidity_side` will override anything previously set on the order.

        """

    def fill_order(self, order: Order, last_px: Price, last_qty: Quantity, liquidity_side: Any, venue_position_id: PositionId | None | None=None, position: Position | None | None=None) -> None:
        """
        Apply the given list of fills to the given order. Optionally provide
        existing position details.

        Parameters
        ----------
        order : Order
            The order to fill.
        last_px : Price
            The fill price for the order.
        last_qty : Quantity
            The fill quantity for the order.
        liquidity_side : LiquiditySide
            The liquidity side for the fill.
        venue_position_id :  PositionId, optional
            The current venue position ID related to the order (if assigned).
        position : Position, optional
            The current position related to the order (if any).

        Raises
        ------
        ValueError
            If `liquidity_side` is ``NO_LIQUIDITY_SIDE``.

        Warnings
        --------
        The `liquidity_side` will override anything previously set on the order.

        """

    def accept_order(self, order: Order) -> None:
        ...

    def expire_order(self, order: Order) -> None:
        ...

    def cancel_order(self, order: Order, cancel_contingencies: bool=True) -> None:
        ...

    def update_order(self, order: Order, qty: Quantity, price: Price | None=None, trigger_price: Price | None=None, update_contingencies: bool=True) -> None:
        ...

    def trigger_stop_order(self, order: Order) -> None:
        ...