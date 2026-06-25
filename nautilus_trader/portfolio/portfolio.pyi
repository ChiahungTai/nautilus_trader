# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.portfolio.base import PortfolioFacade

class Portfolio(PortfolioFacade):
    """
    Provides a trading portfolio.

    Currently there is a limitation of one account per ``ExecutionClient``
    instance.

    Parameters
    ----------
    msgbus : MessageBus
        The message bus for the engine.
    cache : CacheFacade
        The read-only cache for the portfolio.
    clock : Clock
        The clock for the portfolio.
    config : PortfolioConfig
       The configuration for the instance.

    Raises
    ------
    TypeError
        If `config` is not of type `PortfolioConfig`.
    """

    def __init__(self, msgbus: Any, cache: Any, clock: Any, config: Any | None | None=None) -> None:
        ...

    def set_use_mark_prices(self, value: bool) -> None:
        """
        Set the `use_mark_prices` setting with the given `value`.

        Parameters
        ----------
        value : bool
            The value to set.

        """

    def set_use_mark_xrates(self, value: bool) -> None:
        """
        Set the `use_mark_xrates` setting with the given `value`.

        Parameters
        ----------
        value : bool
            The value to set.

        """

    def initialize_orders(self) -> None:
        """
        Initialize the portfolios orders.

        Performs all account calculations for the current orders state.
        """

    def initialize_positions(self) -> None:
        """
        Initialize the portfolios positions.

        Performs all account calculations for the current position state.
        """

    def update_quote_tick(self, tick: Any) -> None:
        """
        Update the portfolio with the given quote tick.

        Clears the cached unrealized PnL for the associated instrument, and
        performs any initialization calculations which may have been pending
        an update.

        Parameters
        ----------
        quote_tick : QuoteTick
            The quote tick to update with.

        """

    def update_mark_price(self, mark_price: object) -> None:
        """
        Update the portfolio with the given mark price.
        """

    def update_bar(self, bar: Any) -> None:
        """
        Update the portfolio with the given bar.

        Clears the cached unrealized PnL for the associated instrument, and
        performs any initialization calculations which may have been pending
        an update.

        Parameters
        ----------
        bar : Bar
            The bar to update with.

        """

    def update_account(self, event: Any) -> None:
        """
        Apply the given account state.

        Parameters
        ----------
        event : AccountState
            The account state to apply.

        """

    def update_order(self, event: Any) -> None:
        """
        Update the portfolio with the given order.

        Parameters
        ----------
        event : OrderEvent
            The event to update with.

        """

    def update_position(self, event: Any) -> None:
        """
        Update the portfolio with the given position event.

        Parameters
        ----------
        event : PositionEvent
            The event to update with.

        """

    def on_order_event(self, event: Any) -> None:
        """
        Actions to be performed on receiving an order event.

        Parameters
        ----------
        event : OrderEvent
            The event received.

        """

    def on_position_event(self, event: Any) -> None:
        """
        Actions to be performed on receiving a position event.

        Parameters
        ----------
        event : PositionEvent
            The event received.

        """

    def reset(self) -> None:
        """
        Reset the portfolio.

        All stateful fields are reset to their initial value.

        """

    def dispose(self) -> None:
        """
        Dispose of the portfolio.

        All stateful fields are reset to their initial value.

        """

    def account(self, venue: Any=None, account_id: Any=None) -> Any:
        """
        Return the account for the given venue or account ID (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the account.
        account_id : AccountId, optional
            The account ID (takes priority if both venue and account_id are provided).

        Returns
        -------
        Account or ``None``

        """

    def balances_locked(self, venue: Any=None, account_id: Any=None) -> dict:
        """
        Return the balances locked for the given venue or account ID (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the account.
        account_id : AccountId, optional
            The account ID (takes priority if both venue and account_id are provided).

        Returns
        -------
        dict[Currency, Money] or ``None``

        """

    def margins_init(self, venue: Any=None, account_id: Any=None) -> dict:
        """
        Return the initial (order) margins for the given venue or account ID (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the account.
        account_id : AccountId, optional
            The account ID (takes priority if both venue and account_id are provided).

        Returns
        -------
        dict[InstrumentId, Money] or ``None``

        """

    def margins_maint(self, venue: Any=None, account_id: Any=None) -> dict:
        """
        Return the maintenance (position) margins for the given venue or account ID (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the account.
        account_id : AccountId, optional
            The account ID (takes priority if both venue and account_id are provided).

        Returns
        -------
        dict[InstrumentId, Money] or ``None``

        """

    def realized_pnls(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """
        Return the realized PnLs for the given venue (if found).

        If no positions exist for the venue or if any lookups fail internally,
        an empty dictionary is returned.

        Parameters
        ----------
        venue : Venue, optional
            The venue for the realized PnLs.
        account_id : AccountId, optional
            The account ID for the realized PnLs.
        target_currency : Currency, optional
            The currency to convert the PnLs into.

        Returns
        -------
        dict[Currency, Money]

        """

    def unrealized_pnls(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """
        Return the unrealized PnLs for the given venue (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the unrealized PnLs.
        account_id : AccountId, optional
            The account ID for the unrealized PnLs.
        target_currency : Currency, optional
            The currency to convert the PnLs into.

        Returns
        -------
        dict[Currency, Money]

        """

    def total_pnls(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """
        Return the total PnLs for the given venue (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the total PnLs.
        account_id : AccountId, optional
            The account ID for the total PnLs.
        target_currency : Currency, optional
            The currency to convert the PnLs into.

        Returns
        -------
        dict[Currency, Money]

        """

    def net_exposures(self, venue: Any=None, account_id: Any=None, target_currency: Any=None) -> dict:
        """
        Return the net exposures for the given venue (if found).

        Parameters
        ----------
        venue : Venue, optional
            The venue for the market value.
        account_id : AccountId, optional
            The account ID for the net exposures.
        target_currency : Currency, optional
            The currency to convert the exposures into.

        Returns
        -------
        dict[Currency, Money] or ``None``

        """

    def mark_values(self, venue: Any=None, account_id: Any=None) -> dict:
        """
        Return the per-currency mark-to-market value of open positions for the
        given venue or account (if found).

        Longs contribute positive notional, shorts contribute negative notional.
        Instruments that cannot be priced are tracked via `missing_price_instruments`.

        Parameters
        ----------
        venue : Venue, optional
            The venue for the open positions.
        account_id : AccountId, optional
            The account ID for the open positions. The missing-price tracker is
            venue-scoped, so filtering by `account_id` does not narrow the tracker.

        Returns
        -------
        dict[Currency, Money]

        """

    def equity(self, venue: Any=None, account_id: Any=None) -> dict:
        """
        Return the per-currency total equity for the given venue or account (if found).

        For cash and betting accounts: ``balance.total + Σ mark_value(open positions)``.
        For margin accounts: ``balance.total + Σ unrealized_pnl(open positions)``.

        Instruments that cannot be priced are tracked via `missing_price_instruments`,
        so equity understatement surfaces via a warn-once log.

        Parameters
        ----------
        venue : Venue, optional
            The venue for the account.
        account_id : AccountId, optional
            The account ID (takes priority if both venue and account_id are provided).

        Returns
        -------
        dict[Currency, Money]

        """

    def missing_price_instruments(self, venue: Any) -> list:
        """
        Return the instruments currently flagged as unpriced for the given venue.

        An entry is added the first time `mark_values` or `equity` cannot source a
        price, mark xrate, or cached instrument for an open position (after also
        emitting a warn log), and removed once the instrument is priced again so a
        subsequent drop re-warns.

        Parameters
        ----------
        venue : Venue
            The venue to query.

        Returns
        -------
        list[InstrumentId]

        """

    def realized_pnl(self, instrument_id: Any, account_id: Any=None, target_currency: Any=None) -> Any:
        """
        Return the realized PnL for the given instrument ID (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the realized PnL.
        account_id : AccountId, optional
            The account ID for the realized PnL. If None, aggregates across all accounts.
        target_currency : Currency, optional
            The currency to convert the PnL into.

        Returns
        -------
        Money or ``None``

        """

    def unrealized_pnl(self, instrument_id: Any, price: Any=None, account_id: Any=None, target_currency: Any=None) -> Any:
        """
        Return the unrealized PnL for the given instrument ID (if found).

        - If `price` is provided, a fresh calculation is performed without using or
          updating the cache.
        - If `price` is omitted, the method returns the cached PnL if available, or
          computes and caches it if not.

        Returns `None` if the calculation fails (e.g., the account or instrument cannot
        be found), or zero-valued `Money` if no positions are open. Otherwise, it returns
        a `Money` object (usually in the account's base currency or the instrument's
        settlement currency).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the unrealized PnL.
        price : Price, optional
            The reference price for the calculation. This could be the last, mid, bid, ask,
            a mark-to-market price, or any other suitably representative value.
        account_id : AccountId, optional
            The account ID for the unrealized PnL. If None, aggregates across all accounts.
        target_currency : Currency, optional
            The currency to convert the PnL into.

        Returns
        -------
        Money or ``None``
            The unrealized PnL or None if the calculation cannot be performed.

        """

    def total_pnl(self, instrument_id: Any, price: Any=None, account_id: Any=None, target_currency: Any=None) -> Any:
        """
        Return the total PnL for the given instrument ID (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the total PnL.
        price : Price, optional
            The reference price for the calculation. This could be the last, mid, bid, ask,
            a mark-to-market price, or any other suitably representative value.
        account_id : AccountId, optional
            The account ID for the total PnL.
        target_currency : Currency, optional
            The currency to convert the PnL into.

        Returns
        -------
        Money or ``None``

        """

    def net_exposure(self, instrument_id: Any, price: Any=None, account_id: Any=None, target_currency: Any=None) -> Any:
        """
        Return the net exposure for the given instrument (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the calculation.
        price : Price, optional
            The reference price for the calculation. This could be the last, mid, bid, ask,
            a mark-to-market price, or any other suitably representative value.
        account_id : AccountId, optional
            The account ID for the net exposure.
        target_currency : Currency, optional
            The currency to convert the exposure into.

        Returns
        -------
        Money or ``None``

        """

    def net_position(self, instrument_id: Any, account_id: Any=None) -> object:
        """
        Return the net position for the given instrument ID.
        If account_id is provided, returns the net position for that account.
        If account_id is None, aggregates across all accounts.
        If no positions for instrument_id then will return `Decimal('0')`.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the query.
        account_id : AccountId, optional
            The account ID. If None, aggregates across all accounts.

        Returns
        -------
        Decimal

        """

    def is_net_long(self, instrument_id: Any, account_id: Any=None) -> bool:
        """
        Return a value indicating whether the portfolio is net long the given
        instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the query.
        account_id : AccountId, optional
            The account ID. If None, aggregates across all accounts.

        Returns
        -------
        bool
            True if net long, else False.

        """

    def is_net_short(self, instrument_id: Any, account_id: Any=None) -> bool:
        """
        Return a value indicating whether the portfolio is net short the given
        instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the query.
        account_id : AccountId, optional
            The account ID. If None, aggregates across all accounts.

        Returns
        -------
        bool
            True if net short, else False.

        """

    def is_flat(self, instrument_id: Any, account_id: Any=None) -> bool:
        """
        Return a value indicating whether the portfolio is flat for the given
        instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument query filter.
        account_id : AccountId, optional
            The account ID. If None, aggregates across all accounts.

        Returns
        -------
        bool
            True if net flat, else False.

        """

    def is_completely_flat(self, account_id: Any=None) -> bool:
        """
        Return a value indicating whether the portfolio is completely flat.

        Parameters
        ----------
        account_id : AccountId, optional
            The account ID. If None, checks across all accounts.

        Returns
        -------
        bool
            True if net flat across all instruments, else False.

        """