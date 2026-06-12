"""Minimal type stubs for nautilus_trader.model.data.

Self-contained: no imports from other Cython modules.
Cross-module types (Price, Quantity, InstrumentId, etc.) are annotated as Any.
"""

from typing import Any


class Bar:
    bar_type: Any  # BarType
    open: Any  # Price
    high: Any  # Price
    low: Any  # Price
    close: Any  # Price
    volume: Any  # Quantity
    ts_event: int
    ts_init: int
    is_revision: bool
    def __init__(
        self,
        bar_type: Any,
        open: Any,
        high: Any,
        low: Any,
        close: Any,
        volume: Any,
        ts_event: int = ...,
        ts_init: int = ...,
        is_revision: bool = ...,
    ) -> None: ...
    @staticmethod
    def from_dict(values: dict[str, Any]) -> Bar: ...
    @staticmethod
    def to_dict(obj: Bar) -> dict[str, Any]: ...
    def is_single_price(self) -> bool: ...


class BarSpecification:
    step: int
    aggregation: Any  # BarAggregation
    price_type: Any  # PriceType
    timedelta: Any
    def __init__(self, step: int, aggregation: Any, price_type: Any) -> None: ...
    @staticmethod
    def from_str(value: str) -> BarSpecification: ...


class BarType:
    instrument_id: Any  # InstrumentId
    spec: BarSpecification
    aggregation_source: Any
    def __init__(self, instrument_id: Any, bar_spec: BarSpecification, aggregation_source: Any = ...) -> None: ...
    @staticmethod
    def from_str(value: str) -> BarType: ...


class BookOrder:
    order_id: int
    price: Any  # Price
    side: Any  # OrderSide
    size: Any  # Quantity


class QuoteTick:
    instrument_id: Any  # InstrumentId
    bid_price: Any  # Price
    ask_price: Any  # Price
    bid_size: Any  # Quantity
    ask_size: Any  # Quantity
    ts_event: int
    ts_init: int


class TradeTick:
    instrument_id: Any  # InstrumentId
    price: Any  # Price
    size: Any  # Quantity
    aggressor_side: Any  # AggressorSide
    trade_id: Any  # TradeId
    ts_event: int
    ts_init: int


class OrderBookDelta:
    action: Any  # BookAction
    flags: int
    instrument_id: Any  # InstrumentId
    order: BookOrder
    sequence: int


class OrderBookDeltas:
    deltas: list[OrderBookDelta]
    flags: int
    instrument_id: Any  # InstrumentId
    sequence: int


class InstrumentStatus:
    instrument_id: Any  # InstrumentId
    action: Any  # MarketStatusAction
    is_trading: bool
    is_quoting: bool


class DataType:
    type: Any
    topic: Any
    metadata: dict
    identifier: Any
