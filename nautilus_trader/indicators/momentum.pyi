"""Minimal type stubs for nautilus_trader.indicators.momentum.

Self-contained: no imports from other Cython modules.
Cross-module types (PriceType, MovingAverageType, etc.) are annotated as Any.

Parameter names are unmangled from the Cython __text_signature__ form
(e.g. `intperiod` -> `period`, `intperiod_k` -> `period_k`,
`MovingAverageTypema_type` -> `ma_type`) by reading the real `def __init__`
signatures in momentum.pyx.
"""

from typing import Any
from nautilus_trader.indicators.base import Indicator


class RelativeStrengthIndex(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, ma_type: Any = ...) -> None: ...


class RateOfChange(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, use_log: bool = ...) -> None: ...


class ChandeMomentumOscillator(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, ma_type: Any = ...) -> None: ...


class Stochastics(Indicator):
    period_k: int
    period_d: int
    slowing: int
    ma_type: Any  # MovingAverageType
    d_method: str
    value_k: float
    value_d: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period_k: int,
        period_d: int,
        slowing: int = ...,
        ma_type: Any = ...,
        d_method: str = ...,
    ) -> None: ...


class CommodityChannelIndex(Indicator):
    period: int
    scalar: float
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        scalar: float = ...,
        ma_type: Any = ...,
    ) -> None: ...


class EfficiencyRatio(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int) -> None: ...


class RelativeVolatilityIndex(Indicator):
    period: int
    scalar: float
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        scalar: float = ...,
        ma_type: Any = ...,
    ) -> None: ...


class PsychologicalLine(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int, ma_type: Any = ...) -> None: ...
