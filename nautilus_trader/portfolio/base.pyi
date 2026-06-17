# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable

class PortfolioFacade:
    """
    Provides a read-only facade for a `Portfolio`.
    """
    initialized: bool
    analyzer: Any

    def account(self, venue: Any=None, account_id: Any=None) -> Any:
        """Abstract method (implement in subclass)."""

    def balances_locked(self, venue: Any=None, account_id: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def margins_init(self, venue: Any=None, account_id: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def margins_maint(self, venue: Any=None, account_id: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def realized_pnls(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def unrealized_pnls(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def total_pnls(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def net_exposures(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def mark_values(self, venue: Any=None, account_id: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def equity(self, venue: Any=None, account_id: Any=None) -> dict:
        """Abstract method (implement in subclass)."""

    def missing_price_instruments(self, venue: Any) -> list:
        """Abstract method (implement in subclass)."""

    def realized_pnl(self, instrument_id: Any, account_id: Any=None, target_currency: Any=None) -> Any:
        """Abstract method (implement in subclass)."""

    def unrealized_pnl(self, instrument_id: Any, price: Any=None, account_id: Any=None, target_currency: Any=None) -> Any:
        """Abstract method (implement in subclass)."""

    def total_pnl(self, instrument_id: Any, price: Any=None, account_id: Any=None, target_currency: Any=None) -> Any:
        """Abstract method (implement in subclass)."""

    def net_exposure(self, instrument_id: Any, price: Any=None, account_id: Any=None, target_currency: Any=None) -> Any:
        """Abstract method (implement in subclass)."""

    def net_position(self, instrument_id: Any, account_id: Any=None) -> object:
        """Abstract method (implement in subclass)."""

    def is_net_long(self, instrument_id: Any, account_id: Any=None) -> bool:
        """Abstract method (implement in subclass)."""

    def is_net_short(self, instrument_id: Any, account_id: Any=None) -> bool:
        """Abstract method (implement in subclass)."""

    def is_flat(self, instrument_id: Any, account_id: Any=None) -> bool:
        """Abstract method (implement in subclass)."""

    def is_completely_flat(self, account_id: Any=None) -> bool:
        """Abstract method (implement in subclass)."""