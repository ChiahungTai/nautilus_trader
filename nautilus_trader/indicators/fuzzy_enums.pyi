# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
'\nThis module exports the fuzzy candle enums for use from Python.\n\nThe enums are defined in the .pxd file for use in Cython code,\nand this .pyx file makes them available to Python code.\n'

class CandleDirection:
    DIRECTION_BEAR: int
    DIRECTION_NONE: int
    DIRECTION_BULL: int

class CandleSize:
    SIZE_NONE: int
    SIZE_VERY_SMALL: int
    SIZE_SMALL: int
    SIZE_MEDIUM: int
    SIZE_LARGE: int
    SIZE_VERY_LARGE: int
    SIZE_EXTREMELY_LARGE: int

class CandleBodySize:
    BODY_NONE: int
    BODY_SMALL: int
    BODY_MEDIUM: int
    BODY_LARGE: int
    BODY_TREND: int

class CandleWickSize:
    WICK_NONE: int
    WICK_SMALL: int
    WICK_MEDIUM: int
    WICK_LARGE: int
__all__ = ['CandleDirection', 'CandleSize', 'CandleBodySize', 'CandleWickSize']