"""Minimal type stubs for nautilus_trader.model.data.

Cross-module types (Price, Quantity, InstrumentId, etc.) are annotated as Any.
Data is imported from core.data so that Bar/QuoteTick/TradeTick/etc. are
recognized as Data subtypes (matches runtime `cdef class Bar(Data)`).
"""

from typing import Any

from nautilus_trader.core.data import Data


class Bar(Data):
    bar_type: BarType
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
        bar_type: BarType,
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
    def is_time_aggregated(self) -> bool: ...


class BarType:
    instrument_id: Any  # InstrumentId
    spec: BarSpecification
    aggregation_source: Any
    def __init__(self, instrument_id: Any, bar_spec: BarSpecification, aggregation_source: Any = ...) -> None: ...
    @staticmethod
    def from_str(value: str) -> BarType: ...
    def is_composite(self) -> bool: ...
    def composite(self) -> BarType: ...
    def is_internally_aggregated(self) -> bool: ...


class BookOrder:
    order_id: int
    price: Any  # Price
    side: Any  # OrderSide
    size: Any  # Quantity
    def __init__(self, side: Any, price: Any, size: Any, order_id: int) -> None: ...


class QuoteTick(Data):
    instrument_id: Any  # InstrumentId
    bid_price: Any  # Price
    ask_price: Any  # Price
    bid_size: Any  # Quantity
    ask_size: Any  # Quantity
    ts_event: int
    ts_init: int
    def __init__(
        self,
        instrument_id: Any,
        bid_price: Any,
        ask_price: Any,
        bid_size: Any,
        ask_size: Any,
        ts_event: int,
        ts_init: int,
    ) -> None: ...


class TradeTick(Data):
    instrument_id: Any  # InstrumentId
    price: Any  # Price
    size: Any  # Quantity
    aggressor_side: Any  # AggressorSide
    trade_id: Any  # TradeId
    ts_event: int
    ts_init: int
    def __init__(
        self,
        instrument_id: Any,
        price: Any,
        size: Any,
        aggressor_side: Any,
        trade_id: Any,
        ts_event: int,
        ts_init: int,
    ) -> None: ...


class OrderBookDelta(Data):
    action: Any  # BookAction
    flags: int
    instrument_id: Any  # InstrumentId
    order: BookOrder
    sequence: int
    ts_event: int
    ts_init: int
    is_add: Any  # BookAction
    is_update: Any  # BookAction
    is_delete: Any  # BookAction
    is_clear: Any  # BookAction
    def __init__(
        self,
        instrument_id: Any,
        action: Any,
        order: Any,
        flags: int,
        sequence: int,
        ts_event: int,
        ts_init: int,
    ) -> None: ...


class OrderBookDeltas(Data):
    deltas: list[OrderBookDelta]
    flags: int
    instrument_id: Any  # InstrumentId
    sequence: int
    ts_event: int
    ts_init: int
    is_snapshot: Any  # bool
    def __init__(self, instrument_id: Any, deltas: list[Any]) -> None: ...


class InstrumentStatus(Data):
    instrument_id: Any  # InstrumentId
    action: Any  # MarketStatusAction
    is_trading: bool
    is_quoting: bool
    is_short_sell_restricted: Any  # bool | None
    ts_event: int
    ts_init: int
    reason: Any  # str | None
    trading_event: Any  # str | None
    def __init__(
        self,
        instrument_id: Any,
        action: Any,
        ts_event: int,
        ts_init: int,
        reason: Any = ...,
        trading_event: Any = ...,
        is_trading: Any = ...,
        is_quoting: Any = ...,
        is_short_sell_restricted: Any = ...,
    ) -> None: ...


class DataType:
    type: Any
    topic: Any
    metadata: dict
    identifier: Any
    def __init__(self, type: Any, metadata: Any = ..., identifier: Any = ...) -> None: ...
