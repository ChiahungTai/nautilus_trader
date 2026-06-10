"""
POC: Strategy subclass bypass + order fill in streaming mode

驗證:
  1. Strategy 子類可用自訂 __init__ 繞過 frozen StrategyConfig
  2. subscribe_bars(BarType) 在 streaming 模式中正確觸發 on_bar
  3. submit_order 在 streaming 模式中正確撮合
  4. on_order_filled 回調正確觸發
  5. 成交後 equity 變化可從 portfolio API 取得（含手續費）

EP 段落: S2
風險: 高
"""

from decimal import Decimal

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.engine import BacktestEngineConfig
from nautilus_trader.backtest.models import MakerTakerFeeModel
from nautilus_trader.core.rust.model import AccountType
from nautilus_trader.core.rust.model import OmsType
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarSpecification
from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import AggregationSource
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.events import OrderFilled
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from nautilus_trader.trading.config import StrategyConfig
from nautilus_trader.trading.strategy import Strategy


def make_btc_instrument() -> CurrencyPair:
    return CurrencyPair(
        instrument_id=InstrumentId.from_str("BTC-USD.SIM"),
        raw_symbol=Symbol("BTCUSD"),
        base_currency=Currency.from_str("BTC"),
        quote_currency=Currency.from_str("USD"),
        price_precision=2,
        size_precision=6,
        price_increment=Price.from_str("0.01"),
        size_increment=Quantity.from_str("0.000001"),
        lot_size=None,
        max_quantity=Quantity.from_str("1000000"),
        min_quantity=Quantity.from_str("0.000001"),
        max_notional=None,
        min_notional=None,
        margin_init=Decimal("0.5"),
        margin_maint=Decimal("0.25"),
        maker_fee=Decimal("0.001"),
        taker_fee=Decimal("0.002"),
        ts_event=0,
        ts_init=0,
    )


def make_bar(bar_type: BarType, ts_event: int, close: str, volume: str = "1000.000000") -> Bar:
    price_f = float(close)
    return Bar(
        bar_type=bar_type,
        open=Price.from_str(f"{price_f - 50:.2f}"),
        high=Price.from_str(f"{price_f + 100:.2f}"),
        low=Price.from_str(f"{price_f - 100:.2f}"),
        close=Price.from_str(close),
        volume=Quantity.from_str(volume),
        ts_event=ts_event,
        ts_init=ts_event,
    )


class TestStrategy(Strategy):
    """Test strategy that bypasses frozen StrategyConfig."""

    def __init__(self, bar_type: BarType, instrument_id: InstrumentId):
        config = StrategyConfig(order_id_tag="TEST")
        super().__init__(config=config)
        self._bar_type = bar_type
        self._instrument_id = instrument_id
        self._bar_count = 0
        self._fill_count = 0
        self._fills: list[OrderFilled] = []
        self._ordered = False

    def on_start(self):
        self.subscribe_bars(self._bar_type)
        print(f"  [Strategy] on_start: subscribed to {self._bar_type}")

    def on_bar(self, bar: Bar):
        self._bar_count += 1
        print(f"  [Strategy] on_bar #{self._bar_count}: close={float(bar.close)}")

        if not self._ordered and self._bar_count == 1:
            instrument = self.cache.instrument(self._instrument_id)
            qty = Quantity(1.0, precision=instrument.size_precision)
            order = self.order_factory.market(
                instrument_id=self._instrument_id,
                order_side=OrderSide.BUY,
                quantity=qty,
            )
            self.submit_order(order)
            self._ordered = True
            print(f"  [Strategy] Submitted BUY order: qty={qty}")

    def on_order_filled(self, event: OrderFilled):
        self._fill_count += 1
        self._fills.append(event)
        print(f"  [Strategy] on_order_filled #{self._fill_count}: "
              f"side={event.order_side}, qty={event.last_qty}, "
              f"price={event.last_px}")

    def on_stop(self):
        print(f"  [Strategy] on_stop: bars={self._bar_count}, fills={self._fill_count}")


def main():
    print("=" * 60)
    print("POC 2: Strategy Subclass + Order Fill in Streaming Mode")
    print("=" * 60)

    all_passed = True

    instrument = make_btc_instrument()
    inst_id = instrument.id

    bar_type = BarType(
        inst_id,
        BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
        AggregationSource.EXTERNAL,
    )
    print(f"\n[1] BarType: {bar_type}")

    base_ts = 1_700_000_000_000_000_000
    day_ns = 86_400_000_000_000

    bars = [
        make_bar(bar_type, base_ts, "50000.00"),
        make_bar(bar_type, base_ts + day_ns, "51000.00"),
        make_bar(bar_type, base_ts + 2 * day_ns, "49000.00"),
    ]
    print(f"[2] Created {len(bars)} bars")

    engine = BacktestEngine(config=BacktestEngineConfig(trader_id=TraderId("POC-002")))
    engine.add_venue(
        venue=Venue("SIM"),
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
        fee_model=MakerTakerFeeModel(),
    )
    engine.add_instrument(instrument)

    strategy = TestStrategy(bar_type, inst_id)
    engine.add_strategy(strategy)
    print("[3] Strategy added")

    print("\n" + "-" * 60)
    print("Streaming Mode: step-by-step with strategy")
    print("-" * 60)

    for i, bar in enumerate(bars):
        print(f"\n--- Step {i + 1} ---")

        engine.add_data([bar], validate=False)
        engine.run(streaming=True)
        engine.clear_data()

        equity_dict = engine.portfolio.equity(venue=Venue("SIM"))
        usd = Currency.from_str("USD")
        equity_val = equity_dict[usd]
        equity_float = float(equity_val.as_double())
        print(f"  Equity: {equity_float:.2f}")

        positions = engine.cache.positions_open()
        print(f"  Open positions: {len(positions)}")
        for p in positions:
            print(f"    {p}")

    print("\n" + "-" * 60)
    print("Results")
    print("-" * 60)

    print(f"  Bars received: {strategy._bar_count}")
    print(f"  Fills received: {strategy._fill_count}")
    print(f"  Final equity: {equity_float:.2f}")

    if strategy._bar_count == 3:
        print("  ✅ All 3 bars received by strategy")
    else:
        print(f"  ❌ Expected 3 bars, got {strategy._bar_count}")
        all_passed = False

    if strategy._fill_count >= 1:
        print("  ✅ Order filled in streaming mode")
    else:
        print("  ❌ No fills — order did not execute")
        all_passed = False

    equity_dict = engine.portfolio.equity(venue=Venue("SIM"))
    final_equity = float(equity_dict[Currency.from_str("USD")].as_double())
    if final_equity < 1_000_000:
        print(f"  ✅ Equity decreased (fees paid): {final_equity:.2f}")
    else:
        print(f"  ⚠️  Equity unchanged: {final_equity:.2f} (expected decrease from fees)")

    engine.end()

    if all_passed:
        print("\n✅ POC 2 PASSED: Strategy subclass + order fill work in streaming mode")
    else:
        print("\n❌ POC 2 FAILED: See errors above")

    return all_passed


if __name__ == "__main__":
    main()
