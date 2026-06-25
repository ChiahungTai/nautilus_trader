"""Minimal type stubs for nautilus_trader.indicators.volatility.

Self-contained: no imports from other Cython modules.
Cross-module types (PriceType, MovingAverageType, etc.) are annotated as Any.

Parameter names are unmangled from the Cython __text_signature__ form
(e.g. `intperiod` -> `period`, `MovingAverageTypema_type` -> `ma_type`) by
reading the real `def __init__` signatures in volatility.pyx.
"""

from typing import Any
from nautilus_trader.indicators.base import Indicator


class AverageTrueRange(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        ma_type: Any = ...,  # MovingAverageType
        use_previous: bool = ...,
        value_floor: float = ...,
    ) -> None: ...


class BollingerBands(Indicator):
    period: int
    k: float
    upper: float
    middle: float
    lower: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        k: float,
        ma_type: Any = ...,  # MovingAverageType
    ) -> None: ...


class DonchianChannel(Indicator):
    period: int
    upper: float
    middle: float
    lower: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int) -> None: ...


class KeltnerChannel(Indicator):
    period: int
    k_multiplier: float
    upper: float
    middle: float
    lower: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        k_multiplier: float,
        ma_type: Any = ...,  # MovingAverageType
        ma_type_atr: Any = ...,  # MovingAverageType
        use_previous: bool = ...,
        atr_floor: float = ...,
    ) -> None: ...


class VerticalHorizontalFilter(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        ma_type: Any = ...,  # MovingAverageType
    ) -> None: ...


class VolatilityRatio(Indicator):
    fast_period: int
    slow_period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        ma_type: Any = ...,  # MovingAverageType
        use_previous: bool = ...,
        value_floor: float = ...,
    ) -> None: ...


class KeltnerPosition(Indicator):
    period: int
    k_multiplier: float
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        k_multiplier: float,
        ma_type: Any = ...,  # MovingAverageType
        ma_type_atr: Any = ...,  # MovingAverageType
        use_previous: bool = ...,
        atr_floor: float = ...,
    ) -> None: ...
