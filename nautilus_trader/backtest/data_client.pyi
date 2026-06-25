# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
'\nThis module provides a data client for backtesting.\n'

class BacktestDataClient(Any):
    """
    Provides an implementation of `DataClient` for backtesting.

    Parameters
    ----------
    client_id : ClientId
        The data client ID.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache for the client.
    clock : Clock
        The clock for the client.
    config : NautilusConfig, optional
        The configuration for the instance.
    """

    def __init__(self, client_id: Any, msgbus: Any, cache: Any, clock: Any, config: Any | None | None=None) -> None:
        ...

    def subscribe(self, command: Any) -> None:
        ...

    def unsubscribe(self, command: Any) -> None:
        ...

    def request(self, request: Any) -> None:
        ...

class BacktestMarketDataClient(Any):
    """
    Provides an implementation of `MarketDataClient` for backtesting.

    Parameters
    ----------
    client_id : ClientId
        The data client ID.
    msgbus : MessageBus
        The message bus for the client.
    cache : Cache
        The cache for the client.
    clock : Clock
        The clock for the client.
    """

    def __init__(self, client_id: Any, msgbus: Any, cache: Any, clock: Any) -> None:
        ...

    def subscribe(self, command: Any) -> None:
        ...

    def unsubscribe(self, command: Any) -> None:
        ...

    def subscribe_instruments(self, command: Any) -> None:
        ...

    def subscribe_instrument(self, command: Any) -> None:
        ...

    def subscribe_order_book_deltas(self, command: Any) -> None:
        ...

    def subscribe_order_book_depth(self, command: Any) -> None:
        ...

    def subscribe_quote_ticks(self, command: Any) -> None:
        ...

    def subscribe_trade_ticks(self, command: Any) -> None:
        ...

    def subscribe_mark_prices(self, command: Any) -> None:
        ...

    def subscribe_index_prices(self, command: Any) -> None:
        ...

    def subscribe_funding_rates(self, command: Any) -> None:
        ...

    def subscribe_bars(self, command: Any) -> None:
        ...

    def subscribe_instrument_status(self, command: Any) -> None:
        ...

    def subscribe_option_greeks(self, command: Any) -> None:
        ...

    def subscribe_instrument_close(self, command: Any) -> None:
        ...

    def unsubscribe_instruments(self, command: Any) -> None:
        ...

    def unsubscribe_instrument(self, command: Any) -> None:
        ...

    def unsubscribe_order_book_deltas(self, command: Any) -> None:
        ...

    def unsubscribe_order_book_depth(self, command: Any) -> None:
        ...

    def unsubscribe_quote_ticks(self, command: Any) -> None:
        ...

    def unsubscribe_trade_ticks(self, command: Any) -> None:
        ...

    def unsubscribe_mark_prices(self, command: Any) -> None:
        ...

    def unsubscribe_index_prices(self, command: Any) -> None:
        ...

    def unsubscribe_funding_rates(self, command: Any) -> None:
        ...

    def unsubscribe_bars(self, command: Any) -> None:
        ...

    def unsubscribe_instrument_status(self, command: Any) -> None:
        ...

    def unsubscribe_option_greeks(self, command: Any) -> None:
        ...

    def unsubscribe_instrument_close(self, command: Any) -> None:
        ...

    def request_instrument(self, request: Any) -> None:
        ...

    def request_instruments(self, request: Any) -> None:
        ...

    def request_order_book_snapshot(self, request: Any) -> None:
        ...

    def request_quote_ticks(self, request: Any) -> None:
        ...

    def request_trade_ticks(self, request: Any) -> None:
        ...

    def request_bars(self, request: Any) -> None:
        ...

    def request_forward_prices(self, request: Any) -> None:
        ...