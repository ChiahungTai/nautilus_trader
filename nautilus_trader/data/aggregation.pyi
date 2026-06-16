# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
import pandas as pd
from datetime import datetime, timedelta

class BarBuilder:
    """
    Provides a generic bar builder for aggregation.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the builder.
    bar_type : BarType
        The bar type for the builder.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """
    price_precision: int
    size_precision: int
    initialized: bool
    ts_last: int
    count: int

    def __init__(self, instrument: Any, bar_type: Any) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def update(self, price: Any, size: Any, ts_init: int) -> None:
        """
        Update the bar builder.

        Parameters
        ----------
        price : Price
            The update price.
        size : Decimal
            The update size.
        ts_init : uint64_t
            UNIX timestamp (nanoseconds) of the update.

        """

    def update_bar(self, bar: Any, volume: Any, ts_init: int) -> None:
        """
        Update the bar builder.

        Parameters
        ----------
        bar : Bar
            The update Bar.

        """

    def set_adjustment(self, adjustment: object, mode: object | None=None) -> None:
        ...

    def build_now(self) -> Any:
        """
        Return the aggregated bar and reset.

        Returns
        -------
        Bar

        """

    def build(self, ts_event: int, ts_init: int) -> Any:
        """
        Return the aggregated bar with the given closing timestamp, and reset.

        Parameters
        ----------
        ts_event : uint64_t
            UNIX timestamp (nanoseconds) for the bar event.
        ts_init : uint64_t
            UNIX timestamp (nanoseconds) for the bar initialization.

        Returns
        -------
        Bar

        """

    def reset(self) -> None:
        """
        Reset the bar builder.

        All per-bar OHLCV state is cleared. Adjustment configuration set via
        `set_adjustment` is retained across resets so it spans subsequent bars
        within the same continuous-future segment.
        """

class BarAggregator:
    """
    Provides a means of aggregating specified bars and sending to a registered handler.

    The aggregator maintains two state flags exposed as properties:
    - `historical_mode`: Indicates the aggregator is processing historical data.
    - `is_running`: Indicates the aggregator is receiving data from the message bus.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """
    bar_type: Any
    historical_mode: bool
    is_running: bool

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def set_historical_mode(self, historical_mode: bool, handler: Callable[[Any], None]) -> None:
        """
        Set the historical mode state of the aggregator.

        Parameters
        ----------
        historical_mode : bool
            Whether the aggregator is processing historical data.
        handler : Callable[[Bar], None]
            The bar handler to use in this mode.

        Raises
        ------
        TypeError
            If `handler` is ``None`` or not callable.

        """

    def set_running(self, is_running: bool) -> None:
        """
        Set the running state of the aggregator.

        Parameters
        ----------
        is_running : bool
            Whether the aggregator is running (receiving data from message bus).

        """

    def handle_quote_tick(self, tick: Any) -> None:
        """
        Update the aggregator with the given tick.

        Parameters
        ----------
        tick : QuoteTick
            The tick for the update.

        """

    def handle_trade_tick(self, tick: Any) -> None:
        """
        Update the aggregator with the given tick.

        Parameters
        ----------
        tick : TradeTick
            The tick for the update.

        """

    def handle_bar(self, bar: Any) -> None:
        """
        Update the aggregator with the given bar.

        Parameters
        ----------
        bar : Bar
            The bar for the update.

        """

class TickBarAggregator(BarAggregator):
    """
    Provides a means of building tick bars from ticks.

    When received tick count reaches the step threshold of the bar
    specification, then a bar is created and sent to the handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

class TickImbalanceBarAggregator(BarAggregator):
    """
    Provides a means of building tick imbalance bars from ticks.

    When the absolute difference between buy and sell ticks reaches the step
    threshold of the bar specification, then a bar is created and sent to the
    handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def handle_trade_tick(self, tick: Any) -> None:
        ...

class TickRunsBarAggregator(BarAggregator):
    """
    Provides a means of building tick runs bars from ticks.

    When consecutive ticks of the same aggressor side reach the step threshold
    of the bar specification, then a bar is created and sent to the handler.
    The run resets when the aggressor side changes.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def handle_trade_tick(self, tick: Any) -> None:
        ...

class VolumeBarAggregator(BarAggregator):
    """
    Provides a means of building volume bars from ticks.

    When received volume reaches the step threshold of the bar
    specification, then a bar is created and sent to the handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

class VolumeImbalanceBarAggregator(BarAggregator):
    """
    Provides a means of building volume imbalance bars from ticks.

    When the absolute difference between buy and sell volume reaches the step
    threshold of the bar specification, then a bar is created and sent to the
    handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def handle_trade_tick(self, tick: Any) -> None:
        ...

class VolumeRunsBarAggregator(BarAggregator):
    """
    Provides a means of building volume runs bars from ticks.

    When consecutive volume of the same aggressor side reaches the step
    threshold of the bar specification, then a bar is created and sent to the
    handler. The run resets when the aggressor side changes.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def handle_trade_tick(self, tick: Any) -> None:
        ...

class ValueBarAggregator(BarAggregator):
    """
    Provides a means of building value bars from ticks.

    When received value reaches the step threshold of the bar
    specification, then a bar is created and sent to the handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def get_cumulative_value(self) -> object:
        """
        Return the current cumulative value of the aggregator.

        Returns
        -------
        Decimal

        """

class ValueImbalanceBarAggregator(BarAggregator):
    """
    Provides a means of building value imbalance bars from ticks.

    When the absolute difference between buy and sell notional value reaches
    the step threshold of the bar specification, then a bar is created and
    sent to the handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def handle_trade_tick(self, tick: Any) -> None:
        ...

class ValueRunsBarAggregator(BarAggregator):
    """
    Provides a means of building value runs bars from ticks.

    When consecutive notional value of the same aggressor side reaches the
    step threshold of the bar specification, then a bar is created and sent
    to the handler. The run resets when the aggressor side changes.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

    def handle_trade_tick(self, tick: Any) -> None:
        ...

class RenkoBarAggregator(BarAggregator):
    """
    Provides a means of building Renko bars from ticks.

    Renko bars are created when the price moves by a fixed amount (brick size)
    regardless of time or volume. Each bar represents a price movement equal
    to the step size in the bar specification.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """
    brick_size: object

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None]) -> None:
        ...

class TimeBarAggregator(BarAggregator):
    """
    Provides a means of building time bars from ticks with an internal timer.

    When the time reaches the next time interval of the bar specification, then
    a bar is created and sent to the handler.

    Parameters
    ----------
    instrument : Instrument
        The instrument for the aggregator.
    bar_type : BarType
        The bar type for the aggregator.
    handler : Callable[[Bar], None]
        The bar handler for the aggregator.
    clock : Clock
        The clock for the aggregator.
    interval_type : str, default 'left-open'
        Determines the type of interval used for time aggregation.
        - 'left-open': start time is excluded and end time is included (default).
        - 'right-open': start time is included and end time is excluded.
    timestamp_on_close : bool, default True
        If True, then timestamp will be the bar close time.
        If False, then timestamp will be the bar open time.
    skip_first_non_full_bar : bool, default False
        If will skip emitting a bar if the aggregation starts mid-interval.
    build_with_no_updates : bool, default True
        If build and emit bars with no new market updates.
    time_bars_origin_offset : pd.Timedelta or pd.DateOffset, optional
        The origin time offset.
    bar_build_delay : int, default 0
        The time delay (microseconds) before building and emitting a composite bar type.

    Raises
    ------
    ValueError
        If `instrument.id` != `bar_type.instrument_id`.
    """
    interval: timedelta
    interval_ns: int
    next_close_ns: int
    stored_open_ns: int
    first_close_ns: int

    def __init__(self, instrument: Any, bar_type: Any, handler: Callable[[Any], None], clock: Any, interval_type: str='left-open', timestamp_on_close: bool=True, skip_first_non_full_bar: bool=False, build_with_no_updates: bool=True, time_bars_origin_offset: pd.Timedelta | pd.DateOffset | None=None, bar_build_delay: int=0) -> None:
        ...

    def __str__(self):
        ...

    def set_clock(self, clock: Any) -> None:
        ...

    def start_timer(self) -> None:
        ...

    def stop_timer(self) -> None:
        ...

    def get_start_time(self, now: datetime) -> datetime:
        """
        Return the start time for the aggregator's next bar.
        """

class SpreadQuoteAggregator:
    """
    Provides a spread quote generator for creating synthetic quotes from leg instruments.

    The generator receives quote ticks from leg instruments via handler callbacks and generates
    synthetic quotes for the spread instrument. Pricing logic differs by instrument type:

    - **Futures spreads**: Calculates weighted bid/ask prices based on leg ratios (positive ratios
      use bid/ask directly, negative ratios invert bid/ask).
    - **Option spreads**: Uses vega-weighted spread calculation to determine bid/ask spreads,
      then applies to the weighted mid-price based on leg ratios.

    The aggregator requires quotes from all legs before building a spread quote. It can operate
    in two modes:

    1. **Quote-driven mode** (`update_interval_seconds=None`): Receives quote tick updates via handler
       and builds spread quotes immediately when all legs have received quotes. This is the default
       and recommended mode for most use cases.

    2. **Timer-driven mode** (`update_interval_seconds=int`): Uses a periodic timer to read quotes
       from internal state and build spread quotes at regular intervals. In historical mode, timer
       events are processed when quotes arrive, ensuring all quotes for a given timestamp are
       received before processing timer events for that timestamp.

    In historical mode, the aggregator advances the provided clock independently with incoming
    data timestamps, similar to TimeBarAggregator. Timer events are generated by advancing the
    clock and are processed only when all legs have received quotes for the corresponding timestamp.

    Parameters
    ----------
    spread_instrument : Instrument
        The spread instrument to generate quotes for.
    handler : Callable[[QuoteTick], None]
        The quote handler callback that receives generated spread quotes.
    greeks_calculator : GreeksCalculator
        The greeks calculator for calculating option greeks (required for option spreads).
    clock : Clock
        The clock for timing operations and timer management.
    historical : bool
        Whether the aggregator is processing historical data. When True, the clock is advanced
        independently with incoming data timestamps.
    update_interval_seconds : int | None, default None
        The interval in seconds for timer-driven quote building. If None, uses quote-driven mode
        (builds immediately when all legs have quotes). If an integer, uses timer-driven mode
        (reads from internal state at the specified interval).
    quote_build_delay : int, default 0
        The time delay (microseconds) before building and emitting a quote.

    Raises
    ------
    ValueError
        If `spread_instrument` has one or fewer legs.
    """
    historical_mode: bool
    is_running: bool

    def __init__(self, spread_instrument: Any, handler: Callable[[Any], None], greeks_calculator: Any, clock: Any, historical: bool, update_interval_seconds: object | None=None, quote_build_delay: int=0):
        ...

    def set_historical_mode(self, historical_mode: bool, handler: Callable[[Any], None], greeks_calculator: Any) -> None:
        ...

    def set_running(self, is_running: bool) -> None:
        ...

    def set_clock(self, clock: Any) -> None:
        ...

    def start_timer(self) -> None:
        ...

    def stop_timer(self) -> None:
        ...

    def handle_quote_tick(self, tick: Any) -> None:
        ...

    def flush_pending_historical_quotes(self) -> None:
        ...

def find_closest_smaller_time(now: pd.Timestamp, daily_time_origin: pd.Timedelta, period: pd.Timedelta) -> pd.Timestamp:
    """Find the closest bar start_time <= now"""