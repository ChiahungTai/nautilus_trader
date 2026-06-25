# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from decimal import Decimal
from nautilus_trader.core.data import Data
from nautilus_trader.model.identifiers import InstrumentId, Symbol
from nautilus_trader.model.objects import Currency, Money, Price, Quantity
EXPIRING_INSTRUMENT_CLASSES = {Any, Any, Any, Any}
ENGINE_EXPIRING_INSTRUMENT_CLASSES = {Any, Any, Any, Any}
NEGATIVE_PRICE_INSTRUMENT_CLASSES = (Any, Any, Any)

class Instrument(Data):
    """
    The base class for all instruments.

    Represents a tradable instrument. This class can be used to
    define an instrument, or act as a parent class for more specific instruments.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the instrument.
    raw_symbol : Symbol
        The raw/local/native symbol for the instrument, assigned by the venue.
    asset_class : AssetClass
        The instrument asset class.
    instrument_class : InstrumentClass
        The instrument class.
    quote_currency : Currency
        The quote currency.
    is_inverse : bool
        If the instrument costing is inverse (quantity expressed in quote currency units).
    price_precision : int
        The price decimal precision.
    size_precision : int
        The trading size decimal precision.
    size_increment : Quantity
        The minimum size increment.
    multiplier : Quantity
        The contract value multiplier (determines tick value).
    lot_size : Quantity, optional
        The rounded lot unit size (standard/board).
    margin_init : Decimal
        The initial (order) margin requirement in percentage of order value.
    margin_maint : Decimal
        The maintenance (position) margin in percentage of position value.
    maker_fee : Decimal
        The fee rate for liquidity makers as a percentage of order value (where 1.0 is 100%).
    taker_fee : Decimal
        The fee rate for liquidity takers as a percentage of order value (where 1.0 is 100%).
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the data event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the data object was initialized.
    price_increment : Price, optional
        The minimum price increment (tick size).
    max_quantity : Quantity, optional
        The maximum allowable order quantity.
    min_quantity : Quantity, optional
        The minimum allowable order quantity.
    max_notional : Money, optional
        The maximum allowable order notional value.
    min_notional : Money, optional
        The minimum allowable order notional value.
    max_price : Price, optional
        The maximum allowable quoted price.
    min_price : Price, optional
        The minimum allowable quoted price.
    tick_scheme_name : str, optional
        The name of the tick scheme.
    info : dict[str, object], optional
        The additional instrument information.

    Raises
    ------
    ValueError
        If `tick_scheme_name` is not a valid string.
    ValueError
        If `price_precision` is negative (< 0).
    ValueError
        If `size_precision` is negative (< 0).
    ValueError
        If `price_increment` is not positive (> 0).
    ValueError
        If `size_increment` is not positive (> 0).
    ValueError
        If `price_precision` is not equal to price_increment.precision.
    ValueError
        If `size_increment` is not equal to size_increment.precision.
    ValueError
        If `multiplier` is not positive (> 0).
    ValueError
        If `margin_init` is negative (< 0).
    ValueError
        If `margin_maint` is negative (< 0).
    ValueError
        If `lot size` is not positive (> 0).
    ValueError
        If `max_quantity` is not positive (> 0).
    ValueError
        If `min_quantity` is negative (< 0).
    ValueError
        If `max_notional` is not positive (> 0).
    ValueError
        If `min_notional` is negative (< 0).
    ValueError
        If `max_price` is not positive (> 0).
    ValueError
        If `min_price` is negative (< 0).

    """
    id: InstrumentId
    raw_symbol: Symbol
    asset_class: Any
    instrument_class: Any
    quote_currency: Currency
    is_inverse: bool
    price_precision: int
    size_precision: int
    price_increment: Price
    size_increment: Quantity
    multiplier: Quantity
    lot_size: Quantity
    max_quantity: Quantity
    min_quantity: Quantity
    max_notional: Money
    min_notional: Money
    max_price: Price
    min_price: Price
    margin_init: object
    margin_maint: object
    maker_fee: object
    taker_fee: object
    tick_scheme_name: str
    info: dict
    ts_event: int
    ts_init: int

    def __init__(self, instrument_id: InstrumentId, raw_symbol: Symbol, asset_class: Any, instrument_class: Any, quote_currency: Currency, is_inverse: bool, price_precision: int, size_precision: int, size_increment: Quantity, multiplier: Quantity, margin_init: Decimal, margin_maint: Decimal, maker_fee: Decimal, taker_fee: Decimal, ts_event: int, ts_init: int, price_increment: Price | None | None=None, lot_size: Quantity | None | None=None, max_quantity: Quantity | None | None=None, min_quantity: Quantity | None | None=None, max_notional: Money | None | None=None, min_notional: Money | None | None=None, max_price: Price | None | None=None, min_price: Price | None | None=None, tick_scheme_name: str | None=None, info: dict | None=None) -> None:
        ...

    def __eq__(self, other: Instrument) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __repr__(self) -> str:
        ...

    @staticmethod
    def base_from_dict(values: dict) -> Instrument:
        """
        Return an instrument from the given initialization values.

        Parameters
        ----------
        values : dict[str, object]
            The values to initialize the instrument with.

        Returns
        -------
        Instrument

        """

    @staticmethod
    def base_to_dict(obj: Instrument):
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """

    @property
    def symbol(self):
        """
        Return the instruments ticker symbol.

        Returns
        -------
        Symbol

        """

    @property
    def venue(self):
        """
        Return the instruments trading venue.

        Returns
        -------
        Venue

        """

    def is_spread(self) -> bool:
        """
        Return whether the instrument is a spread instrument.

        Returns
        -------
        bool

        """

    def legs(self) -> list:
        """
        Return the list of leg tuples (instrument_id, ratio) for this spread.

        Base implementation returns an empty list. Override in spread instrument
        classes to return the actual legs.

        Returns
        -------
        list[tuple[InstrumentId, int]]
            List of tuples containing (instrument_id, ratio) for each leg.

        """

    def get_base_currency(self) -> Currency | None:
        """
        Return the instruments base currency (if applicable).

        Returns
        -------
        Currency or ``None``

        """

    def get_settlement_currency(self) -> Currency:
        """
        Return the currency used to settle a trade of the instrument.

        - Standard linear instruments = quote_currency
        - Inverse instruments = base_currency
        - Quanto instruments = settlement_currency

        Returns
        -------
        Currency

        """

    def get_cost_currency(self) -> Currency:
        """
        Return the currency used for PnL calculations for the instrument.

        - Standard linear instruments = quote_currency
        - Inverse instruments = base_currency
        - Quanto instruments TBD

        Returns
        -------
        Currency

        """

    def set_tick_scheme(self, tick_scheme_name: str) -> None:
        """
        Set the tick scheme for the instrument.

        Sets both the `tick_scheme_name` and the corresponding tick scheme implementation
        used for price rounding and tick calculations.

        This will override any previously set tick scheme, including the `tick_scheme_name` field.

        Parameters
        ----------
        tick_scheme_name : str
            The name of the registered tick scheme.

        Raises
        ------
        ValueError
            If `tick_scheme_name` is not a valid string.
        ValueError
            If `tick_scheme_name` is not a registered tick scheme.

        """

    def make_price(self, value) -> Price:
        """
        Return a new price from the given value using the instruments price
        precision.

        Parameters
        ----------
        value : integer, float, str or Decimal
            The value of the price.

        Returns
        -------
        Price

        """

    def next_bid_price(self, value: float, num_ticks: int=0) -> Price:
        """
        Return the price `n` bid ticks away from value.

        If a given price is between two ticks, n=0 will find the nearest bid tick.

        Parameters
        ----------
        value : double
            The reference value.
        num_ticks : int, default 0
            The number of ticks to move.

        Returns
        -------
        Price

        Raises
        ------
        ValueError
            If a tick scheme is not initialized.

        """

    def next_ask_price(self, value: float, num_ticks: int=0) -> Price:
        """
        Return the price `n` ask ticks away from value.

        If a given price is between two ticks, n=0 will find the nearest ask tick.

        Parameters
        ----------
        value : double
            The reference value.
        num_ticks : int, default 0
            The number of ticks to move.

        Returns
        -------
        Price

        Raises
        ------
        ValueError
            If a tick scheme is not initialized.

        """

    def next_bid_prices(self, value: float, num_ticks: int=100) -> list:
        """
        Return a list of prices up to `num_ticks` bid ticks away from value.

        If a given price is between two ticks, the first price will be the nearest bid tick.
        Returns as many valid ticks as possible up to `num_ticks`. Will return an empty list
        if no valid ticks can be generated.

        Parameters
        ----------
        value : double
            The reference value.
        num_ticks : int, default 100
            The number of ticks to return.

        Returns
        -------
        list[Decimal]
            A list of bid prices as Decimal values.

        Raises
        ------
        ValueError
            If a tick scheme is not initialized.
        """

    def next_ask_prices(self, value: float, num_ticks: int=100) -> list:
        """
        Return a list of prices up to `num_ticks` ask ticks away from value.

        If a given price is between two ticks, the first price will be the nearest ask tick.
        Returns as many valid ticks as possible up to `num_ticks`. Will return an empty list
        if no valid ticks can be generated.

        Parameters
        ----------
        value : double
            The reference value.
        num_ticks : int, default 100
            The number of ticks to return.

        Returns
        -------
        list[Decimal]
            A list of ask prices as Decimal values.

        Raises
        ------
        ValueError
            If a tick scheme is not initialized.
        """

    def make_qty(self, value, round_down: bool=False) -> Quantity:
        """
        Return a new quantity from the given value using the instruments size
        precision.

        Parameters
        ----------
        value : integer, float, str or Decimal
            The value of the quantity.
        round_down : bool, default False
            If True, always rounds down to the nearest valid increment.
            If False, uses the `round` function (banker's rounding) which
            rounds to the nearest even digit when exactly halfway between two values.

        Returns
        -------
        Quantity

        Raises
        ------
        ValueError
            If a non zero `value` is rounded to zero due to the instruments size increment or size precision.

        """

    def notional_value(self, quantity: Quantity, price: Price, use_quote_for_inverse: bool=False, target_currency: Currency | None=None, conversion_price: Price | None=None) -> Money:
        """
        Calculate the notional value.

        Result will be in quote currency for standard instruments, or base
        currency for inverse instruments.

        If `target_currency` and `conversion_price` are provided, the notional
        value will be converted to the target currency.

        Parameters
        ----------
        quantity : Quantity
            The total quantity.
        price : Price
            The price for the calculation.
        use_quote_for_inverse : bool
            If inverse instrument calculations use quote currency (instead of base).
        target_currency : Currency, optional
            The target currency for conversion.
        conversion_price : Price, optional
            The price to use for currency conversion.

        Returns
        -------
        Money

        """

    def calculate_base_quantity(self, quantity: Quantity, last_px: Price) -> Quantity:
        """
        Calculate the base asset quantity from the given quote asset `quantity` and last price.

        Parameters
        ----------
        quantity : Quantity
            The quantity to convert from.
        last_px : Price
            The last price for the instrument.

        Returns
        -------
        Quantity

        """

def instruments_from_pyo3(pyo3_instruments: list) -> list:
    ...