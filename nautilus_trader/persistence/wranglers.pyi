"""Type stubs for nautilus_trader.persistence.wranglers.

Self-contained: no imports from other Cython modules.
Cross-module types (Instrument, Bar, etc.) are annotated as Any.
"""

from typing import Any

import numpy as np
import pandas as pd

_Instrument = Any
_BarType = Any
_Bar = Any
_QuoteTick = Any
_TradeTick = Any
_OrderBookDelta = Any
_Price = Any
_Quantity = Any


def preprocess_bar_data(data: pd.DataFrame, is_raw: bool) -> pd.DataFrame: ...

def calculate_bar_price_offsets(
    num_records: int,
    timestamp_is_close: bool,
    offset_interval_ms: int,
    random_seed: int | None = ...,
) -> dict[str, np.ndarray]: ...

def calculate_volume_quarter(
    volume: np.ndarray, precision: int, size_increment: float
) -> np.ndarray: ...

def align_bid_ask_bar_data(
    bid_data: pd.DataFrame, ask_data: pd.DataFrame
) -> pd.DataFrame: ...


class OrderBookDeltaDataWrangler:
    instrument: _Instrument

    def __init__(self, instrument: _Instrument) -> None: ...
    def process(
        self, data: pd.DataFrame, ts_init_delta: int = ..., is_raw: bool = ...
    ) -> list[_OrderBookDelta]: ...


class QuoteTickDataWrangler:
    instrument: _Instrument

    def __init__(self, instrument: _Instrument) -> None: ...
    def process(
        self,
        data: pd.DataFrame,
        default_volume: float = ...,
        ts_init_delta: int = ...,
    ) -> list[_QuoteTick]: ...
    def process_bar_data(
        self,
        bid_data: pd.DataFrame,
        ask_data: pd.DataFrame,
        default_volume: float = ...,
        ts_init_delta: int = ...,
    ) -> list[_QuoteTick]: ...


class TradeTickDataWrangler:
    instrument: _Instrument
    processed_data: Any

    def __init__(self, instrument: _Instrument) -> None: ...
    def process(
        self, data: pd.DataFrame, ts_init_delta: int = ..., is_raw: bool = ...
    ) -> list[_TradeTick]: ...
    def process_bar_data(
        self,
        data: pd.DataFrame,
        ts_init_delta: int = ...,
        offset_interval_ms: int = ...,
        timestamp_is_close: bool = ...,
    ) -> list[_TradeTick]: ...


class BarDataWrangler:
    bar_type: _BarType
    instrument: _Instrument

    def __init__(self, bar_type: _BarType, instrument: _Instrument) -> None: ...
    def process(
        self,
        data: pd.DataFrame,
        default_volume: float = ...,
        ts_init_delta: int = ...,
    ) -> list[_Bar]: ...
