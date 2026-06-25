# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
'\nA cash account that cannot hold leveraged positions.\n\nBalance locking\n---------------\nThe account tracks locked balances per (InstrumentId, Currency) to support\ninstruments that lock different currencies depending on order side:\n\n- BUY orders lock quote currency (cost of purchase).\n- SELL orders lock base currency (assets being sold).\n\nCallers must clear all existing locks via `clear_balance_locked` before applying\nnew locks. This prevents stale currency entries when order compositions change.\n\nGraceful degradation\n--------------------\nWhen total locked exceeds total balance (e.g., due to venue/client state latency),\nthe account clamps locked to total rather than raising an error. This yields zero\nfree balance, preventing new orders while avoiding crashes in live trading.\n\n'
from nautilus_trader.accounting.accounts.base import Account

class CashAccount(Account):
    """
    Provides a cash account.

    Parameters
    ----------
    event : AccountState
        The initial account state event.
    calculate_account_state : bool, optional
        If the account state should be calculated from order fills.
    allow_borrowing : bool, optional
        If borrowing is allowed (negative balances).

    Raises
    ------
    ValueError
        If `event.account_type` is not equal to ``CASH``.

    """
    ACCOUNT_TYPE = Any
    allow_borrowing: bool

    def __init__(self, event: Any, calculate_account_state: bool=False, allow_borrowing: bool=False):
        ...

    @staticmethod
    def to_dict(obj: CashAccount):
        ...

    @staticmethod
    def from_dict(values: dict):
        ...

    def update_balances(self, balances: list) -> None:
        """
        Update the account balances.

        There is no guarantee that every account currency is included in the
        given balances, therefore we only update included balances.

        Parameters
        ----------
        balances : list[AccountBalance]
            The balances for the update. An empty list is treated as a no-op.

        Raises
        ------
        AccountBalanceNegative
            If borrowing is not allowed and balance is negative.

        """

    def apply(self, event: Any) -> None:
        """
        Apply the given account event to the account.

        Clears per-instrument locked balances only for externally reported state,
        since external state is authoritative. Internal state preserves lock tracking.

        Parameters
        ----------
        event : AccountState
            The account event to apply.

        Warnings
        --------
        System method (not intended to be called by user code).

        """

    def update_balance_locked(self, instrument_id: Any, locked: Any) -> None:
        """
        Update the balance locked for the given instrument ID and currency.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the update.
        locked : Money
            The locked balance for the instrument.

        Raises
        ------
        ValueError
            If `locked` is negative (< 0).

        Warnings
        --------
        System method (not intended to be called by user code).

        """

    def clear_balance_locked(self, instrument_id: Any) -> None:
        """
        Clear all balances locked for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for which to clear all locked balances.

        """

    def is_unleveraged(self, instrument_id: Any) -> bool:
        ...

    def calculate_commission(self, instrument: Any, last_qty: Any, last_px: Any, liquidity_side: Any, use_quote_for_inverse: bool=False) -> Any:
        """
        Calculate the commission generated from a transaction with the given
        parameters.

        Result will be in quote currency for standard instruments, or base
        currency for inverse instruments.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        last_qty : Quantity
            The transaction quantity.
        last_px : Price
            The transaction price.
        liquidity_side : LiquiditySide {``MAKER``, ``TAKER``}
            The liquidity side for the transaction.
        use_quote_for_inverse : bool
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money

        Raises
        ------
        ValueError
            If `liquidity_side` is ``NO_LIQUIDITY_SIDE``.

        """

    def calculate_balance_locked(self, instrument: Any, side: Any, quantity: Any, price: Any, use_quote_for_inverse: bool=False) -> Any:
        """
        Calculate the locked balance.

        Result will be in quote currency for standard instruments, or base
        currency for inverse instruments.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        side : OrderSide {``BUY``, ``SELL``}
            The order side.
        quantity : Quantity
            The order quantity.
        price : Price
            The order price.
        use_quote_for_inverse : bool
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money

        """

    def calculate_pnls(self, instrument: Any, fill: Any, position: Any | None | None=None) -> list:
        """
        Return the calculated PnL.

        The calculation does not include any commissions.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        fill : OrderFilled
            The fill for the calculation.
        position : Position, optional
            The position for the calculation (can be None).

        Returns
        -------
        list[Money]

        """

    def balance_impact(self, instrument: Any, quantity: Any, price: Any, order_side: Any) -> Any:
        ...