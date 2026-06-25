"""Minimal type stubs for nautilus_trader.indicators.trend.

Self-contained: no imports from other Cython modules.
Cross-module types (PriceType, MovingAverageType, datetime, etc.) are annotated as Any.

Parameter names are unmangled from the Cython __text_signature__ form
(e.g. `intperiod` -> `period`, `intfast_period` -> `fast_period`) by
reading the real `def __init__` signatures in trend.pyx.
"""

from typing import Any
from nautilus_trader.indicators.base import Indicator


class ArcherMovingAveragesTrends(Indicator):
    fast_period: int
    slow_period: int
    signal_period: int
    long_run: int
    short_run: int
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        signal_period: int,
        ma_type: Any = ...,
    ) -> None: ...


class AroonOscillator(Indicator):
    period: int
    value: float
    aroon_up: float
    aroon_down: float
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int) -> None: ...


class DirectionalMovement(Indicator):
    period: int
    value: float
    pos: float
    neg: float
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        ma_type: Any = ...,
    ) -> None: ...


class MovingAverageConvergenceDivergence(Indicator):
    fast_period: int
    slow_period: int
    value: float
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        ma_type: Any = ...,
        price_type: Any = ...,
    ) -> None: ...


class IchimokuCloud(Indicator):
    tenkan_period: int
    kijun_period: int
    senkou_period: int
    displacement: int
    tenkan_sen: float
    kijun_sen: float
    senkou_span_a: float
    senkou_span_b: float
    chikou_span: float
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        tenkan_period: int = ...,
        kijun_period: int = ...,
        senkou_period: int = ...,
        displacement: int = ...,
    ) -> None: ...


class LinearRegression(Indicator):
    period: int
    slope: float
    intercept: float
    degree: float
    cfo: float
    R2: float
    value: float
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int = ...) -> None: ...


class Bias(Indicator):
    period: int
    value: float
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        ma_type: Any = ...,
    ) -> None: ...


class Swings(Indicator):
    period: int
    direction: int
    changed: bool
    high_datetime: Any  # datetime
    low_datetime: Any  # datetime
    high_price: float
    low_price: float
    length: float
    duration: int
    since_high: int
    since_low: int
    count: int
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int) -> None: ...
