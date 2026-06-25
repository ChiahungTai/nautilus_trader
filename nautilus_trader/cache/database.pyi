# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from datetime import datetime
from nautilus_trader.cache.facade import CacheDatabaseFacade

class CacheDatabaseAdapter(CacheDatabaseFacade):
    """
    Provides a generic cache database adapter.

    Parameters
    ----------
    trader_id : TraderId
        The trader ID for the adapter.
    instance_id : UUID4
        The instance ID for the adapter.
    serializer : Serializer
        The serializer for database operations.
    config : CacheConfig, optional
        The configuration for the instance.

    Raises
    ------
    TypeError
        If `config` is not of type `CacheConfig`.

    Warnings
    --------
    Redis can only accurately store int64 types to 17 digits of precision.
    Therefore nanosecond timestamp int64's with 19 digits will lose 2 digits of
    precision when persisted. One way to solve this is to ensure the serializer
    converts timestamp int64's to strings on the way into Redis, and converts
    timestamp strings back to int64's on the way out. One way to achieve this is
    to set the `timestamps_as_str` flag to true for the `MsgSpecSerializer`, as
    per the default implementations for both `TradingNode` and `BacktestEngine`.
    """

    def __init__(self, trader_id: Any, instance_id: Any, serializer: Any, config: Any | None | None=None) -> None:
        ...

    def close(self) -> None:
        """
        Close the backing database adapter.

        """

    def flush(self) -> None:
        """
        Flush the database which clears all data.

        """

    def keys(self, pattern: str='*') -> list:
        """
        Return all keys in the database matching the given `pattern`.

        Parameters
        ----------
        pattern : str, default '*'
            The glob-style pattern to match against the keys in the database.

        Returns
        -------
        list[str]

        Raises
        ------
        ValueError
            If `pattern` is not a valid string.

        Warnings
        --------
        Using the default '*' pattern string can have serious performance implications and
        can take a long time to execute if many keys exist in the database. This operation
        can lead to high memory and CPU usage, and should be used with caution, especially
        in production environments.

        """

    def load_all(self) -> dict:
        """
        Load all cache data from the database.

        Returns
        -------
        dict[str, dict]
            A dictionary containing all cache data organized by category.

        """

    def load(self) -> dict:
        """
        Load all general objects from the database using bulk loading for efficiency.

        Returns
        -------
        dict[str, bytes]

        """

    def load_currencies(self) -> dict:
        """
        Load all currencies from the database using bulk loading for efficiency.

        Returns
        -------
        dict[str, Currency]

        """

    def load_instruments(self) -> dict:
        """
        Load all instruments from the database using bulk loading for efficiency.

        Returns
        -------
        dict[InstrumentId, Instrument]

        """

    def load_synthetics(self) -> dict:
        """
        Load all synthetic instruments from the database using bulk loading for efficiency.

        Returns
        -------
        dict[InstrumentId, SyntheticInstrument]

        """

    def load_accounts(self) -> dict:
        """
        Load all accounts from the database.

        Returns
        -------
        dict[AccountId, Account]

        """

    def load_orders(self) -> dict:
        """
        Load all orders from the database.

        Returns
        -------
        dict[ClientOrderId, Order]

        """

    def load_positions(self) -> dict:
        """
        Load all positions from the database.

        Returns
        -------
        dict[PositionId, Position]

        """

    def load_index_order_position(self) -> dict:
        """
        Load the order to position index from the database.

        Returns
        -------
        dict[ClientOrderId, PositionId]

        """

    def load_index_order_client(self) -> dict:
        """
        Load the order to execution client index from the database.

        Returns
        -------
        dict[ClientOrderId, ClientId]

        """

    def load_currency(self, code: str) -> Any:
        """
        Load the currency associated with the given currency code (if found).

        Parameters
        ----------
        code : str
            The currency code to load.

        Returns
        -------
        Currency or ``None``

        """

    def load_instrument(self, instrument_id: Any) -> Any:
        """
        Load the instrument associated with the given instrument ID
        (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID to load.

        Returns
        -------
        Instrument or ``None``

        """

    def load_synthetic(self, instrument_id: Any) -> Any:
        """
        Load the synthetic instrument associated with the given synthetic instrument ID
        (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The synthetic instrument ID to load.

        Returns
        -------
        SyntheticInstrument or ``None``

        Raises
        ------
        ValueError
            If `instrument_id` is not for a synthetic instrument.

        """

    def load_account(self, account_id: Any) -> Any:
        """
        Load the account associated with the given account ID (if found).

        Parameters
        ----------
        account_id : AccountId
            The account ID to load.

        Returns
        -------
        Account or ``None``

        """

    def load_order(self, client_order_id: Any) -> Any:
        """
        Load the order associated with the given client order ID (if found).

        Parameters
        ----------
        client_order_id : ClientOrderId
            The client order ID to load.

        Returns
        -------
        Order or ``None``

        """

    def load_position(self, position_id: Any) -> Any:
        """
        Load the position associated with the given ID (if found).

        Parameters
        ----------
        position_id : PositionId
            The position ID to load.

        Returns
        -------
        Position or ``None``

        """

    def load_actor(self, component_id: Any) -> dict:
        """
        Load the state for the given actor.

        Parameters
        ----------
        component_id : ComponentId
            The ID of the actor state dictionary to load.

        Returns
        -------
        dict[str, Any]

        """

    def delete_actor(self, component_id: Any) -> None:
        """
        Delete the given actor from the database.

        Parameters
        ----------
        component_id : ComponentId
            The ID of the actor state dictionary to delete.

        """

    def load_strategy(self, strategy_id: Any) -> dict:
        """
        Load the state for the given strategy.

        Parameters
        ----------
        strategy_id : StrategyId
            The ID of the strategy state dictionary to load.

        Returns
        -------
        dict[str, bytes]

        """

    def delete_strategy(self, strategy_id: Any) -> None:
        """
        Delete the given strategy from the database.

        Parameters
        ----------
        strategy_id : StrategyId
            The ID of the strategy state dictionary to delete.

        """

    def delete_order(self, client_order_id: Any) -> None:
        """
        Delete the given order from the database.

        Parameters
        ----------
        client_order_id : ClientOrderId
            The client order ID to delete.

        """

    def delete_position(self, position_id: Any) -> None:
        """
        Delete the given position from the database.

        Parameters
        ----------
        position_id : PositionId
            The position ID to delete.

        """

    def delete_account_event(self, account_id: Any, event_id: str) -> None:
        """
        Delete the given account event from the database.

        Parameters
        ----------
        account_id : AccountId
            The account ID to delete events for.
        event_id : str
            The event ID to delete.

        """

    def add(self, key: str, value: bytes) -> None:
        """
        Add the given general object value to the database.

        Parameters
        ----------
        key : str
            The key to write to.
        value : bytes
            The object value.

        """

    def add_currency(self, currency: Any) -> None:
        """
        Add the given currency to the database.

        Parameters
        ----------
        currency : Currency
            The currency to add.

        """

    def add_instrument(self, instrument: Any) -> None:
        """
        Add the given instrument to the database.

        Parameters
        ----------
        instrument : Instrument
            The instrument to add.

        """

    def add_synthetic(self, synthetic: Any) -> None:
        """
        Add the given synthetic instrument to the database.

        Parameters
        ----------
        synthetic : SyntheticInstrument
            The synthetic instrument to add.

        """

    def add_account(self, account: Any) -> None:
        """
        Add the given account to the database.

        Parameters
        ----------
        account : Account
            The account to add.

        """

    def add_order(self, order: Any, position_id: Any=None, client_id: Any=None) -> None:
        """
        Add the given order to the database.

        Parameters
        ----------
        order : Order
            The order to add.
        position_id : PositionId, optional
            The position ID to associate with this order.
        client_id : ClientId, optional
            The execution client ID to associate with this order.

        """

    def add_position(self, position: Any) -> None:
        """
        Add the given position to the database.

        Parameters
        ----------
        position : Position
            The position to add.

        """

    def index_venue_order_id(self, client_order_id: Any, venue_order_id: Any) -> None:
        """
        Add an index entry for the given `venue_order_id` to `client_order_id`.

        Parameters
        ----------
        client_order_id : ClientOrderId
            The client order ID to index.
        venue_order_id : VenueOrderId
            The venue order ID to index.

        """

    def index_order_position(self, client_order_id: Any, position_id: Any) -> None:
        """
        Add an index entry for the given `client_order_id` to `position_id`.

        Parameters
        ----------
        client_order_id : ClientOrderId
            The client order ID to index.
        position_id : PositionId
            The position ID to index.

        """

    def update_actor(self, actor: Any) -> None:
        """
        Update the given actor state in the database.

        Parameters
        ----------
        actor : Actor
            The actor to update.

        """

    def update_strategy(self, strategy: Any) -> None:
        """
        Update the given strategy state in the database.

        Parameters
        ----------
        strategy : Strategy
            The strategy to update.

        """

    def update_account(self, account: Any) -> None:
        """
        Update the given account in the database.

        Parameters
        ----------
        account : The account to update (from last event).

        """

    def update_order(self, order: Any) -> None:
        """
        Update the given order in the database.

        Parameters
        ----------
        order : Order
            The order to update (from last event).

        """

    def update_position(self, position: Any) -> None:
        """
        Update the given position in the database.

        Parameters
        ----------
        position : Position
            The position to update (from last event).

        """

    def snapshot_order_state(self, order: Any) -> None:
        """
        Snapshot the state of the given `order`.

        Parameters
        ----------
        order : Order
            The order for the state snapshot.

        """

    def snapshot_position_state(self, position: Any, ts_snapshot: int, unrealized_pnl: Any=None) -> None:
        """
        Snapshot the state of the given `position`.

        Parameters
        ----------
        position : Position
            The position for the state snapshot.
        ts_snapshot : uint64_t
            UNIX timestamp (nanoseconds) when the snapshot was taken.
        unrealized_pnl : Money, optional
            The unrealized PnL for the state snapshot.

        """

    def heartbeat(self, timestamp: datetime) -> None:
        """
        Add a heartbeat at the given `timestamp`.

        Parameters
        ----------
        timestamp : datetime
            The timestamp for the heartbeat.

        """