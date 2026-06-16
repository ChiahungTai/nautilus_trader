# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from datetime import datetime

class CacheDatabaseFacade:
    """
    The base class for all cache databases.

    Parameters
    ----------
    config : CacheConfig, optional
        The configuration for the database.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    def __init__(self, config: Any | None | None=None) -> None:
        ...

    def close(self) -> None:
        """Abstract method (implement in subclass)."""

    def flush(self) -> None:
        """Abstract method (implement in subclass)."""

    def keys(self, pattern: str='*') -> list:
        """Abstract method (implement in subclass)."""

    def load_all(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_currencies(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_instruments(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_synthetics(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_accounts(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_orders(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_positions(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_index_order_position(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_index_order_client(self) -> dict:
        """Abstract method (implement in subclass)."""

    def load_currency(self, code: str) -> Any:
        """Abstract method (implement in subclass)."""

    def load_instrument(self, instrument_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def load_synthetic(self, instrument_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def load_account(self, account_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def load_order(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def load_position(self, position_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def load_actor(self, component_id: Any) -> dict:
        """Abstract method (implement in subclass)."""

    def load_strategy(self, strategy_id: Any) -> dict:
        """Abstract method (implement in subclass)."""

    def add(self, key: str, value: bytes) -> None:
        """Abstract method (implement in subclass)."""

    def add_currency(self, currency: Any) -> None:
        """Abstract method (implement in subclass)."""

    def add_instrument(self, instrument: Any) -> None:
        """Abstract method (implement in subclass)."""

    def add_synthetic(self, synthetic: Any) -> None:
        """Abstract method (implement in subclass)."""

    def add_account(self, account: Any) -> None:
        """Abstract method (implement in subclass)."""

    def add_order(self, order: Any, position_id: Any=None, client_id: Any=None) -> None:
        """Abstract method (implement in subclass)."""

    def add_position(self, position: Any) -> None:
        """Abstract method (implement in subclass)."""

    def index_venue_order_id(self, client_order_id: Any, venue_order_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def index_order_position(self, client_order_id: Any, position_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def update_account(self, event: Any) -> None:
        """Abstract method (implement in subclass)."""

    def update_order(self, order: Any) -> None:
        """Abstract method (implement in subclass)."""

    def update_position(self, position: Any) -> None:
        """Abstract method (implement in subclass)."""

    def update_actor(self, actor: Any) -> None:
        """Abstract method (implement in subclass)."""

    def update_strategy(self, strategy: Any) -> None:
        """Abstract method (implement in subclass)."""

    def snapshot_order_state(self, order: Any) -> None:
        """Abstract method (implement in subclass)."""

    def snapshot_position_state(self, position: Any, ts_snapshot: int, unrealized_pnl: Any=None) -> None:
        """Abstract method (implement in subclass)."""

    def delete_order(self, client_order_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def delete_position(self, position_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def delete_account_event(self, account_id: Any, event_id: str) -> None:
        """Abstract method (implement in subclass)."""

    def delete_actor(self, component_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def delete_strategy(self, strategy_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def heartbeat(self, timestamp: datetime) -> None:
        """Abstract method (implement in subclass)."""