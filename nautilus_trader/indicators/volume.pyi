"""Minimal type stubs for nautilus_trader.indicators.volume.

Self-contained: no imports from other Cython modules.
Cross-module types (PriceType, MovingAverageType, etc.) are annotated as Any.

Parameter names are unmangled from the Cython __text_signature__ form
(e.g. `intperiod` -> `period`, `MovingAverageTypema_type` -> `ma_type`) by
reading the real `def __init__` signatures in volume.pyx.
"""

from typing import Any
from nautilus_trader.indicators.base import Indicator


class OnBalanceVolume(Indicator):
    period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self, period: int = ...) -> None: ...


class VolumeWeightedAveragePrice(Indicator):
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(self) -> None: ...


class KlingerVolumeOscillator(Indicator):
    fast_period: int
    slow_period: int
    signal_period: int
    value: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        signal_period: int,
        ma_type: Any = ...,  # MovingAverageType
    ) -> None: ...


class Pressure(Indicator):
    period: int
    value: float
    value_cumulative: float
    has_inputs: bool
    initialized: bool
    def __init__(
        self,
        period: int,
        ma_type: Any = ...,  # MovingAverageType
        atr_floor: float = ...,
    ) -> None: ...
