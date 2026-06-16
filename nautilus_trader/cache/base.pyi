# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class CacheFacade:
    """
    Provides a read-only facade for the common `Cache`.
    """

    def get(self, key: str) -> bytes:
        """Abstract method (implement in subclass)."""

    def add(self, key: str, value: bytes) -> None:
        """Abstract method (implement in subclass)."""

    def quote_ticks(self, instrument_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def trade_ticks(self, instrument_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def mark_prices(self, instrument_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def index_prices(self, instrument_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def funding_rates(self, instrument_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def instrument_statuses(self, instrument_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def bars(self, bar_type: Any) -> list:
        """Abstract method (implement in subclass)."""

    def price(self, instrument_id: Any, price_type: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def prices(self, price_type: Any) -> dict:
        """Abstract method (implement in subclass)."""

    def order_book(self, instrument_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def own_order_book(self, instrument_id: Any) -> object:
        """Abstract method (implement in subclass)."""

    def own_bid_orders(self, instrument_id: Any, status: set | None=None, accepted_buffer_ns: int=0, ts_now: int=0) -> dict:
        """Abstract method (implement in subclass)."""

    def own_ask_orders(self, instrument_id: Any, status: set | None=None, accepted_buffer_ns: int=0, ts_now: int=0) -> dict:
        """Abstract method (implement in subclass)."""

    def quote_tick(self, instrument_id: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def trade_tick(self, instrument_id: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def mark_price(self, instrument_id: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def index_price(self, instrument_id: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def funding_rate(self, instrument_id: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def instrument_status(self, instrument_id: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def bar(self, bar_type: Any, index: int=0) -> Any:
        """Abstract method (implement in subclass)."""

    def book_update_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def quote_tick_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def trade_tick_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def mark_price_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def index_price_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def funding_rate_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def instrument_status_count(self, instrument_id: Any) -> int:
        """Abstract method (implement in subclass)."""

    def bar_count(self, bar_type: Any) -> int:
        """Abstract method (implement in subclass)."""

    def has_order_book(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_quote_ticks(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_trade_ticks(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_mark_prices(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_index_prices(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_funding_rates(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_instrument_statuses(self, instrument_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def has_bars(self, bar_type: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def get_xrate(self, venue: Any, from_currency: Any, to_currency: Any, price_type: Any=...):
        """Abstract method (implement in subclass)."""

    def get_mark_xrate(self, from_currency: Any, to_currency: Any) -> object:
        """Abstract method (implement in subclass)."""

    def set_mark_xrate(self, from_currency: Any, to_currency: Any, xrate: float) -> None:
        """Abstract method (implement in subclass)."""

    def clear_mark_xrate(self, from_currency: Any, to_currency: Any) -> None:
        """Abstract method (implement in subclass)."""

    def clear_mark_xrates(self) -> None:
        """Abstract method (implement in subclass)."""

    def instrument(self, instrument_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def instrument_ids(self, venue: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def instruments(self, venue: Any=None, underlying: str | None=None) -> list:
        """Abstract method (implement in subclass)."""

    def synthetic(self, instrument_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def synthetic_ids(self) -> list:
        """Abstract method (implement in subclass)."""

    def synthetics(self) -> list:
        """Abstract method (implement in subclass)."""

    def set_specific_venue(self, venue: Any) -> None:
        """Abstract method (implement in subclass)."""

    def account(self, account_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def account_for_venue(self, venue: Any=None, account_id: Any=None) -> Any:
        """Abstract method (implement in subclass)."""

    def account_id(self, venue: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def set_account_id_for_venue(self, venue: Any, account_id: Any) -> None:
        """Abstract method (implement in subclass)."""

    def accounts(self) -> list:
        """Abstract method (implement in subclass)."""

    def client_order_ids(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def client_order_ids_open(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def client_order_ids_closed(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def client_order_ids_emulated(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def client_order_ids_inflight(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def order_list_ids(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def position_ids(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def position_open_ids(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def position_closed_ids(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def actor_ids(self) -> set:
        """Abstract method (implement in subclass)."""

    def strategy_ids(self) -> set:
        """Abstract method (implement in subclass)."""

    def exec_algorithm_ids(self) -> set:
        """Abstract method (implement in subclass)."""

    def order(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def client_order_id(self, venue_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def venue_order_id(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def client_id(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def orders(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def orders_open(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def orders_closed(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def orders_emulated(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def orders_inflight(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def orders_for_position(self, position_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def order_exists(self, client_order_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def is_order_open(self, client_order_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def is_order_closed(self, client_order_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def is_order_emulated(self, client_order_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def is_order_inflight(self, client_order_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def is_order_pending_cancel_local(self, client_order_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def orders_open_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def orders_closed_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def orders_emulated_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def orders_inflight_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def orders_total_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def order_list(self, order_list_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def order_lists(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def order_list_exists(self, order_list_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def orders_for_exec_algorithm(self, exec_algorithm_id: Any, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def orders_for_exec_spawn(self, exec_spawn_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def exec_spawn_total_quantity(self, exec_spawn_id: Any, active_only: bool=False) -> Any:
        """Abstract method (implement in subclass)."""

    def exec_spawn_total_filled_qty(self, exec_spawn_id: Any, active_only: bool=False) -> Any:
        """Abstract method (implement in subclass)."""

    def exec_spawn_total_leaves_qty(self, exec_spawn_id: Any, active_only: bool=False) -> Any:
        """Abstract method (implement in subclass)."""

    def position(self, position_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def position_for_order(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def position_id(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def position_snapshot_ids(self, instrument_id: Any=None, account_id: Any=None) -> set:
        """Abstract method (implement in subclass)."""

    def position_snapshots(self, position_id: Any=None, account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def position_snapshot_bytes(self, position_id: Any) -> list:
        """Abstract method (implement in subclass)."""

    def positions(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def position_exists(self, position_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def positions_open(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def positions_closed(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> list:
        """Abstract method (implement in subclass)."""

    def is_position_open(self, position_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def is_position_closed(self, position_id: Any) -> bool:
        """Abstract method (implement in subclass)."""

    def positions_open_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def positions_closed_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def positions_total_count(self, venue: Any=None, instrument_id: Any=None, strategy_id: Any=None, side: Any=..., account_id: Any=None) -> int:
        """Abstract method (implement in subclass)."""

    def strategy_id_for_order(self, client_order_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def strategy_id_for_position(self, position_id: Any) -> Any:
        """Abstract method (implement in subclass)."""

    def add_greeks(self, greeks: object) -> None:
        """Abstract method (implement in subclass)."""

    def add_yield_curve(self, yield_curve: object) -> None:
        """Abstract method (implement in subclass)."""

    def greeks(self, instrument_id: Any) -> object:
        """Abstract method (implement in subclass)."""

    def yield_curve(self, curve_name: str) -> object:
        """Abstract method (implement in subclass)."""