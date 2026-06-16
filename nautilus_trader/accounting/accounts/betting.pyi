# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any

class BettingAccount(Any):
    """
    Provides a betting account.
    """
    ACCOUNT_TYPE = Any

    def calculate_balance_locked(self, instrument: Any, side: Any, quantity: Any, price: Any, use_quote_for_inverse: bool=False) -> Any:
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

    def balance_impact(self, instrument: Any, quantity: Any, price: Any, order_side: Any) -> Any:
        ...

def stake(quantity: Any, price: Any):
    ...

def liability(quantity: Any, price: Any, side: Any):
    ...

def win_payoff(quantity: Any, price: Any, side: Any):
    ...

def lose_payoff(quantity: Any, side: Any):
    ...

def exposure(quantity: Any, price: Any, side: Any):
    ...