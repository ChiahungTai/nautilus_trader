"""Minimal type stubs for nautilus_trader.indicators.averages.

Self-contained: no imports from other Cython modules.
Cross-module types (PriceType, etc.) are annotated as Any; MovingAverageType
is defined here as IntFlag (from averages.pxd:25 cpdef enum).

Parameter names are unmangled from the Cython __text_signature__ form
(e.g. `intperiod` -> `period`, `PriceTypeprice_type` -> `price_type`) by
reading the real `def __init__` signatures in averages.pyx.
"""

from enum import IntFlag
from typing import Any


class MovingAverageType(IntFlag):
    SIMPLE = 0
    EXPONENTIAL = 1
    DOUBLE_EXPONENTIAL = 2
    WILDER = 3
    HULL = 4
    ADAPTIVE = 5
    WEIGHTED = 6
    VARIABLE_INDEX_DYNAMIC = 7


class MovingAverage:
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, params: list[Any], price_type: Any) -> None: ...
    def update_raw(self, value: float) -> None: ...


class SimpleMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, price_type: Any = ...) -> None: ...


class ExponentialMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, price_type: Any = ...) -> None: ...


class DoubleExponentialMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, price_type: Any = ...) -> None: ...


class WeightedMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, weights: Any = ..., price_type: Any = ...) -> None: ...


class HullMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, price_type: Any = ...) -> None: ...


class AdaptiveMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period_er: int,
        period_alpha_fast: int,
        period_alpha_slow: int,
        price_type: Any = ...,
    ) -> None: ...


class WilderMovingAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, price_type: Any = ...) -> None: ...


class VariableIndexDynamicAverage(MovingAverage):
    period: int
    value: float
    count: int
    price_type: Any  # PriceType
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        price_type: Any = ...,
        cmo_ma_type: Any = ...,
    ) -> None: ...


class MovingAverageFactory:
    @staticmethod
    def create(period: int, ma_type: Any, **kwargs: Any) -> Any: ...
