# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.accounting.accounts.cash import CashAccount
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Money, Price, Quantity

class BettingAccount(CashAccount):
    """
    Provides a betting account.
    """
    ACCOUNT_TYPE = Any

    def calculate_balance_locked(self, instrument: Instrument, side: Any, quantity: Quantity, price: Price, use_quote_for_inverse: bool=False) -> Money:
        """
        Calculate the locked balance.

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
            Not applicable for betting accounts.

        Returns
        -------
        Money

        """

    def balance_impact(self, instrument: Instrument, quantity: Quantity, price: Price, order_side: Any) -> Money:
        ...

def stake(quantity: Quantity, price: Price):
    ...

def liability(quantity: Quantity, price: Price, side: Any):
    ...

def win_payoff(quantity: Quantity, price: Price, side: Any):
    ...

def lose_payoff(quantity: Quantity, side: Any):
    ...

def exposure(quantity: Quantity, price: Price, side: Any):
    ...