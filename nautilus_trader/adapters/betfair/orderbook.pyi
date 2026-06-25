# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.model.book import OrderBook
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Price, Quantity

def create_betfair_order_book(instrument_id: InstrumentId) -> OrderBook:
    ...

def betfair_float_to_price(value: float) -> Price:
    ...

def betfair_float_to_quantity(value: float) -> Quantity:
    ...