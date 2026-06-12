# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2026 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from typing import Any

from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarType
from nautilus_trader.model.data import QuoteTick
from nautilus_trader.model.data import TradeTick
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import ClientId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import PositionId
from nautilus_trader.model.identifiers import StrategyId
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity

# -- Types without .pyi stubs remain as Any --
_StrategyConfig = Any
_ImportableStrategyConfig = Any
_OrderId = Any
_Order = Any
_OrderList = Any
_Position = Any
_Instrument = Any
_Indicator = Any
_Clock = Any
_Logger = Any
_MessageBus = Any
_CacheFacade = Any
_PortfolioFacade = Any
_OrderFactory = Any
_OmsType = Any
_OrderSide = Any
_PositionSide = Any
_TimeInForce = Any
_OrderEvent = Any
_OrderInitialized = Any
_OrderDenied = Any
_OrderEmulated = Any
_OrderReleased = Any
_OrderSubmitted = Any
_OrderRejected = Any
_OrderAccepted = Any
_OrderCanceled = Any
_OrderExpired = Any
_OrderTriggered = Any
_OrderPendingUpdate = Any
_OrderPendingCancel = Any
_OrderModifyRejected = Any
_OrderCancelRejected = Any
_OrderUpdated = Any
_OrderFilled = Any
_PositionEvent = Any
_PositionOpened = Any
_PositionChanged = Any
_PositionClosed = Any
_UUID4 = Any
_ComponentState = Any


class Strategy:
    """
    The base class for all trading strategies.

    Users subclass this and override the ``on_*`` event handler methods to
    implement custom trading logic.
    """

    def __init__(self, config: _StrategyConfig | None = ...) -> None: ...

    # -- Properties ----------------------------------------------------------

    @property
    def id(self) -> StrategyId: ...
    @property
    def trader_id(self) -> TraderId: ...
    @property
    def state(self) -> _ComponentState: ...
    @property
    def config(self) -> _StrategyConfig: ...
    @property
    def order_factory(self) -> _OrderFactory: ...
    @property
    def order_id_tag(self) -> str: ...
    @property
    def oms_type(self) -> _OmsType: ...
    @property
    def clock(self) -> _Clock: ...
    @property
    def log(self) -> _Logger: ...
    @property
    def msgbus(self) -> _MessageBus: ...
    @property
    def cache(self) -> _CacheFacade: ...
    @property
    def portfolio(self) -> _PortfolioFacade: ...

    # -- Lifecycle -----------------------------------------------------------

    def on_start(self) -> None:
        """Actions to be performed on strategy start. Override in subclass."""
        ...

    def on_stop(self) -> None:
        """Actions to be performed on strategy stop. Override in subclass."""
        ...

    def on_resume(self) -> None:
        """Actions to be performed on strategy resume. Override in subclass."""
        ...

    def on_reset(self) -> None:
        """Actions to be performed on strategy reset. Override in subclass."""
        ...

    def on_dispose(self) -> None:
        """Actions to be performed on strategy dispose. Override in subclass."""
        ...

    def on_degrade(self) -> None:
        """Actions to be performed on strategy degrade. Override in subclass."""
        ...

    def on_fault(self) -> None:
        """Actions to be performed on strategy fault. Override in subclass."""
        ...

    def stop(self) -> None: ...

    # -- Data Event Handlers -------------------------------------------------

    def on_instrument(self, instrument: _Instrument) -> None: ...
    def on_bar(self, bar: Bar) -> None: ...
    def on_quote_tick(self, tick: QuoteTick) -> None: ...
    def on_trade_tick(self, tick: TradeTick) -> None: ...

    # -- Order Event Handlers ------------------------------------------------

    def on_order_event(self, event: _OrderEvent) -> None: ...
    def on_order_initialized(self, event: _OrderInitialized) -> None: ...
    def on_order_denied(self, event: _OrderDenied) -> None: ...
    def on_order_emulated(self, event: _OrderEmulated) -> None: ...
    def on_order_released(self, event: _OrderReleased) -> None: ...
    def on_order_submitted(self, event: _OrderSubmitted) -> None: ...
    def on_order_rejected(self, event: _OrderRejected) -> None: ...
    def on_order_accepted(self, event: _OrderAccepted) -> None: ...
    def on_order_canceled(self, event: _OrderCanceled) -> None: ...
    def on_order_expired(self, event: _OrderExpired) -> None: ...
    def on_order_triggered(self, event: _OrderTriggered) -> None: ...
    def on_order_pending_update(self, event: _OrderPendingUpdate) -> None: ...
    def on_order_pending_cancel(self, event: _OrderPendingCancel) -> None: ...
    def on_order_modify_rejected(self, event: _OrderModifyRejected) -> None: ...
    def on_order_cancel_rejected(self, event: _OrderCancelRejected) -> None: ...
    def on_order_updated(self, event: _OrderUpdated) -> None: ...
    def on_order_filled(self, event: _OrderFilled) -> None: ...

    # -- Position Event Handlers ---------------------------------------------

    def on_position_event(self, event: _PositionEvent) -> None: ...
    def on_position_opened(self, event: _PositionOpened) -> None: ...
    def on_position_changed(self, event: _PositionChanged) -> None: ...
    def on_position_closed(self, event: _PositionClosed) -> None: ...

    # -- Market Exit ---------------------------------------------------------

    def on_market_exit(self) -> None: ...
    def post_market_exit(self) -> None: ...
    def market_exit(self) -> None: ...
    def is_exiting(self) -> bool: ...

    # -- Trading Commands ----------------------------------------------------

    def submit_order(
        self,
        order: _Order,
        position_id: PositionId | None = ...,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def submit_order_list(
        self,
        order_list: _OrderList,
        position_id: PositionId | None = ...,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def modify_order(
        self,
        order: _Order,
        quantity: Quantity | None = ...,
        price: Price | None = ...,
        trigger_price: Price | None = ...,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def cancel_order(
        self,
        order: _Order,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def cancel_orders(
        self,
        orders: list[_Order],
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def cancel_all_orders(
        self,
        instrument_id: InstrumentId,
        order_side: _OrderSide = ...,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def close_position(
        self,
        position: _Position,
        client_id: ClientId | None = ...,
        tags: list[str] | None = ...,
        time_in_force: _TimeInForce = ...,
        reduce_only: bool = ...,
        quote_quantity: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def close_all_positions(
        self,
        instrument_id: InstrumentId,
        position_side: _PositionSide = ...,
        client_id: ClientId | None = ...,
        tags: list[str] | None = ...,
        time_in_force: _TimeInForce = ...,
        reduce_only: bool = ...,
        quote_quantity: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def query_account(
        self,
        account_id: AccountId,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def query_order(
        self,
        order: _Order,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    # -- Data Subscriptions (inherited from Actor) ---------------------------

    def subscribe_bars(
        self,
        bar_type: BarType,
        client_id: ClientId | None = ...,
        update_catalog: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def subscribe_quote_ticks(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = ...,
        update_catalog: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def subscribe_trade_ticks(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = ...,
        update_catalog: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def subscribe_instrument(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = ...,
        update_catalog: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def subscribe_instruments(
        self,
        venue: Venue,
        client_id: ClientId | None = ...,
        update_catalog: bool = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def unsubscribe_bars(
        self,
        bar_type: BarType,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def unsubscribe_quote_ticks(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def unsubscribe_trade_ticks(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    def unsubscribe_instrument(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> None: ...

    # -- Data Requests (inherited from Actor) --------------------------------

    def request_bars(
        self,
        bar_type: BarType,
        start: Any,  # datetime
        end: Any = ...,  # datetime
        limit: int = ...,
        client_id: ClientId | None = ...,
        callback: Any = ...,
        update_catalog: bool = ...,
        join_request: bool = ...,
        request_id: _UUID4 | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> _UUID4: ...

    def request_instrument(
        self,
        instrument_id: InstrumentId,
        start: Any = ...,  # datetime
        end: Any = ...,  # datetime
        client_id: ClientId | None = ...,
        callback: Any = ...,
        update_catalog: bool = ...,
        join_request: bool = ...,
        request_id: _UUID4 | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> _UUID4: ...

    def request_quote_ticks(
        self,
        instrument_id: InstrumentId,
        start: Any,  # datetime
        end: Any = ...,  # datetime
        limit: int = ...,
        client_id: ClientId | None = ...,
        callback: Any = ...,
        update_catalog: bool = ...,
        join_request: bool = ...,
        request_id: _UUID4 | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> _UUID4: ...

    def request_trade_ticks(
        self,
        instrument_id: InstrumentId,
        start: Any,  # datetime
        end: Any = ...,  # datetime
        limit: int = ...,
        client_id: ClientId | None = ...,
        callback: Any = ...,
        update_catalog: bool = ...,
        join_request: bool = ...,
        request_id: _UUID4 | None = ...,
        params: dict[str, Any] | None = ...,
    ) -> _UUID4: ...

    # -- Indicator Registration (inherited from Actor) -----------------------

    def register_indicator_for_bars(
        self,
        bar_type: BarType,
        indicator: _Indicator,
    ) -> None: ...

    def register_indicator_for_quote_ticks(
        self,
        instrument_id: InstrumentId,
        indicator: _Indicator,
    ) -> None: ...

    def register_indicator_for_trade_ticks(
        self,
        instrument_id: InstrumentId,
        indicator: _Indicator,
    ) -> None: ...

    def indicators_initialized(self) -> bool: ...

    # -- GTD Expiry ----------------------------------------------------------

    def cancel_gtd_expiry(self, order: _Order) -> None: ...

    # -- Config --------------------------------------------------------------

    def to_importable_config(self) -> _ImportableStrategyConfig: ...
