# Self-contained stub: cross-Cython types -> Any (auto-postprocessed from stubgen-pyx)
from typing import Any, Callable
from nautilus_trader.data.messages import RequestBars, RequestData, RequestForwardPrices, RequestFundingRates, RequestInstrument, RequestInstruments, RequestOrderBookDeltas, RequestOrderBookSnapshot, RequestQuoteTicks, RequestTradeTicks, SubscribeBars, SubscribeData, SubscribeFundingRates, SubscribeIndexPrices, SubscribeInstrument, SubscribeInstrumentClose, SubscribeInstruments, SubscribeInstrumentStatus, SubscribeMarkPrices, SubscribeOptionGreeks, SubscribeOrderBook, SubscribeQuoteTicks, SubscribeTradeTicks, UnsubscribeBars, UnsubscribeData, UnsubscribeFundingRates, UnsubscribeIndexPrices, UnsubscribeInstrument, UnsubscribeInstrumentClose, UnsubscribeInstruments, UnsubscribeInstrumentStatus, UnsubscribeMarkPrices, UnsubscribeOptionGreeks, UnsubscribeOrderBook, UnsubscribeQuoteTicks, UnsubscribeTradeTicks

class DataClient(Any):
    """
    The base class for all data clients.

    Parameters
    ----------
    client_id : ClientId
        The data client ID.
    msgbus : MessageBus
        The message bus for the client.
    clock : Clock
        The clock for the client.
    venue : Venue, optional
        The client venue. If multi-venue then can be ``None``.
    config : NautilusConfig, optional
        The configuration for the instance.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    venue: Any
    is_connected: bool

    def __init__(self, client_id: Any, msgbus: Any, cache: Any, clock: Any, venue: Any | None | None=None, config: Any | None | None=None) -> None:
        ...

    def __repr__(self) -> str:
        ...

    def subscribed_custom_data(self) -> list:
        """
        Return the custom data types subscribed to.

        Returns
        -------
        list[DataType]

        """

    def subscribe(self, command: SubscribeData) -> None:
        """
        Subscribe to data for the given data type.

        Parameters
        ----------
        data_type : DataType
            The data type for the subscription.

        """

    def unsubscribe(self, command: UnsubscribeData) -> None:
        """
        Unsubscribe from data for the given data type.

        Parameters
        ----------
        data_type : DataType
            The data type for the subscription.

        """

    def request(self, request: RequestData) -> None:
        """
        Request data for the given data type.

        Parameters
        ----------
        request : RequestData
            The message for the data request.

        """

class MarketDataClient(DataClient):
    """
    The base class for all market data clients.

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
    venue : Venue, optional
        The client venue. If multi-venue then can be ``None``.
    config : NautilusConfig, optional
        The configuration for the instance.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    def __init__(self, client_id: Any, msgbus: Any, cache: Any, clock: Any, venue: Any | None | None=None, config: Any | None | None=None) -> None:
        ...

    def subscribed_custom_data(self) -> list:
        """
        Return the custom data types subscribed to.

        Returns
        -------
        list[DataType]

        """

    def subscribed_instruments(self) -> list:
        """
        Return the instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_order_book_deltas(self) -> list:
        """
        Return the order book delta instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_order_book_depth(self) -> list:
        """
        Return the order book depth instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_quote_ticks(self) -> list:
        """
        Return the quote tick instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_trade_ticks(self) -> list:
        """
        Return the trade tick instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_mark_prices(self) -> list:
        """
        Return the mark price update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_index_prices(self) -> list:
        """
        Return the index price update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_funding_rates(self) -> list:
        """
        Return the funding rate update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_bars(self) -> list:
        """
        Return the bar types subscribed to.

        Returns
        -------
        list[BarType]

        """

    def subscribed_instrument_status(self) -> list:
        """
        Return the status update instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_instrument_close(self) -> list:
        """
        Return the instrument closes subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribed_option_greeks(self) -> list:
        """
        Return the option greeks instruments subscribed to.

        Returns
        -------
        list[InstrumentId]

        """

    def subscribe(self, command: SubscribeData) -> None:
        """
        Subscribe to data for the given data type.

        Parameters
        ----------
        data_type : DataType
            The data type for the subscription.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_instruments(self, command: SubscribeInstruments) -> None:
        """
        Subscribe to all `Instrument` data.

        Parameters
        ----------
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_instrument(self, command: SubscribeInstrument) -> None:
        """
        Subscribe to the `Instrument` with the given instrument ID.

        Parameters
        ----------
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_order_book_deltas(self, command: SubscribeOrderBook) -> None:
        """
        Subscribe to `OrderBookDeltas` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The order book instrument to subscribe to.
        book_type : BookType {``L1_MBP``, ``L2_MBP``, ``L3_MBO``}
            The order book type.
        depth : int, optional, default None
            The maximum depth for the subscription.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_order_book_depth(self, command: SubscribeOrderBook) -> None:
        """
        Subscribe to `OrderBookDepth10` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The order book instrument to subscribe to.
        depth : int, optional
            The maximum depth for the order book (defaults to 10).
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_quote_ticks(self, command: SubscribeQuoteTicks) -> None:
        """
        Subscribe to `QuoteTick` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_trade_ticks(self, command: SubscribeTradeTicks) -> None:
        """
        Subscribe to `TradeTick` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_mark_prices(self, command: SubscribeMarkPrices) -> None:
        """
        Subscribe to `MarkPriceUpdate` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_index_prices(self, command: SubscribeIndexPrices) -> None:
        """
        Subscribe to `IndexPriceUpdate` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_funding_rates(self, command: SubscribeFundingRates) -> None:
        """
        Subscribe to `FundingRateUpdate` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_instrument_status(self, command: SubscribeInstrumentStatus) -> None:
        """
        Subscribe to `InstrumentStatus` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_instrument_close(self, command: SubscribeInstrumentClose) -> None:
        """
        Subscribe to `InstrumentClose` updates for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def subscribe_option_greeks(self, command: SubscribeOptionGreeks) -> None:
        """
        Subscribe to `OptionGreeks` data for the given instrument ID.

        Parameters
        ----------
        command : SubscribeOptionGreeks
            The subscribe command.

        """

    def subscribe_bars(self, command: SubscribeBars) -> None:
        """
        Subscribe to `Bar` data for the given bar type.

        Parameters
        ----------
        bar_type : BarType
            The bar type to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe(self, command: UnsubscribeData) -> None:
        """
        Unsubscribe from data for the given data type.

        Parameters
        ----------
        data_type : DataType
            The data type for the subscription.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_instruments(self, command: UnsubscribeInstruments) -> None:
        """
        Unsubscribe from all `Instrument` data.

        Parameters
        ----------
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_instrument(self, command: UnsubscribeInstrument) -> None:
        """
        Unsubscribe from `Instrument` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_order_book_deltas(self, command: UnsubscribeOrderBook) -> None:
        """
        Unsubscribe from `OrderBookDeltas` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The order book instrument to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_order_book_depth(self, command: UnsubscribeOrderBook) -> None:
        """
        Unsubscribe from `OrderBookDepth10` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The order book instrument to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_quote_ticks(self, command: UnsubscribeQuoteTicks) -> None:
        """
        Unsubscribe from `QuoteTick` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_trade_ticks(self, command: UnsubscribeTradeTicks) -> None:
        """
        Unsubscribe from `TradeTick` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_mark_prices(self, command: UnsubscribeMarkPrices) -> None:
        """
        Unsubscribe from `MarkPriceUpdate` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_index_prices(self, command: UnsubscribeIndexPrices) -> None:
        """
        Unsubscribe from `IndexPriceUpdate` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_funding_rates(self, command: UnsubscribeFundingRates) -> None:
        """
        Unsubscribe from `FundingRateUpdate` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument to subscribe to.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_bars(self, command: UnsubscribeBars) -> None:
        """
        Unsubscribe from `Bar` data for the given bar type.

        Parameters
        ----------
        bar_type : BarType
            The bar type to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_instrument_status(self, command: UnsubscribeInstrumentStatus) -> None:
        """
        Unsubscribe from `InstrumentStatus` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument status updates to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_instrument_close(self, command: UnsubscribeInstrumentClose) -> None:
        """
        Unsubscribe from `InstrumentClose` data for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The tick instrument to unsubscribe from.
        params : dict[str, Any], optional
            Additional params for the subscription.

        """

    def unsubscribe_option_greeks(self, command: UnsubscribeOptionGreeks) -> None:
        """
        Unsubscribe from `OptionGreeks` data for the given instrument ID.

        Parameters
        ----------
        command : UnsubscribeOptionGreeks
            The unsubscribe command.

        """

    def request_instrument(self, request: RequestInstrument) -> None:
        """
        Request `Instrument` data for the given instrument ID.

        Parameters
        ----------
        request : RequestInstrument
            The message for the data request.

        """

    def request_instruments(self, request: RequestInstruments) -> None:
        """
        Request all `Instrument` data for the given venue.

        Parameters
        ----------
        request : RequestInstruments
            The message for the data request.

        """

    def request_order_book_deltas(self, request: RequestOrderBookDeltas) -> None:
        """
        Request historical `OrderBookDeltas` data.

        Parameters
        ----------
        request : RequestOrderBookDeltas
            The message for the data request.

        """

    def request_order_book_snapshot(self, request: RequestOrderBookSnapshot) -> None:
        """
        Request order book snapshot data.

        Parameters
        ----------
        request : RequestOrderBookSnapshot
            The message for the data request.

        """

    def request_quote_ticks(self, request: RequestQuoteTicks) -> None:
        """
        Request historical `QuoteTick` data.

        Parameters
        ----------
        request : RequestQuoteTicks
            The message for the data request.

        """

    def request_trade_ticks(self, request: RequestTradeTicks) -> None:
        """
        Request historical `TradeTick` data.

        Parameters
        ----------
        request : RequestTradeTicks
            The message for the data request.

        """

    def request_funding_rates(self, request: RequestFundingRates) -> None:
        """
        Request historical `FundingRateUpdate` data.

        Parameters
        ----------
        request : RequestFundingRates
            The message for the data request.

        """

    def request_bars(self, request: RequestBars) -> None:
        """
        Request historical `Bar` data. To load historical data from a catalog, you can pass a list[DataCatalogConfig] to the TradingNodeConfig or the BacktestEngineConfig.

        Parameters
        ----------
        request : RequestBars
            The message for the data request.

        """

    def request_forward_prices(self, request: RequestForwardPrices) -> None:
        """
        Request forward prices for option chain ATM determination.

        Parameters
        ----------
        request : RequestForwardPrices
            The message for the data request.

        """