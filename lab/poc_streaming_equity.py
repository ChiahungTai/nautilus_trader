"""
POC: BacktestEngine streaming mode step-by-step + equity API

驗證:
  1. add_data([single_bar]) -> run(streaming=True) -> clear_data() 循環可行
  2. CurrencyPair + AccountType.MARGIN 可正確設置
  3. portfolio.equity(venue=...) 回傳型別是 dict[Currency, float]（非 Money）

EP 段落: S1
風險: 致命
"""

from decimal import Decimal

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.engine import BacktestEngineConfig
from nautilus_trader.core.rust.model import AccountType
from nautilus_trader.core.rust.model import OmsType
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarSpecification
from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import AggregationSource
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import TraderId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity


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


def make_bar(bar_type: BarType, ts_event: int, open_: str, high: str, low: str, close: str, volume: str) -> Bar:
    return Bar(
        bar_type=bar_type,
        open=Price.from_str(open_),
        high=Price.from_str(high),
        low=Price.from_str(low),
        close=Price.from_str(close),
        volume=Quantity.from_str(volume),
        ts_event=ts_event,
        ts_init=ts_event,
    )


def main():
    print("=" * 60)
    print("POC 1: BacktestEngine Streaming Mode + Equity API")
    print("=" * 60)

    instrument = make_btc_instrument()
    inst_id = instrument.id
    print(f"\n[1] Instrument: {inst_id}")
    print(f"    base={instrument.base_currency}, quote={instrument.quote_currency}")
    print(f"    price_precision={instrument.price_precision}, size_precision={instrument.size_precision}")

    bar_type = BarType(
        inst_id,
        BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
        AggregationSource.EXTERNAL,
    )
    print(f"\n[2] BarType: {bar_type}")
    print(f"    aggregation_source={bar_type.aggregation_source}")

    engine = BacktestEngine(config=BacktestEngineConfig(trader_id=TraderId("POC-001")))
    print("\n[3] Engine created")

    engine.add_venue(
        venue=Venue("SIM"),
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
    )
    print("[4] Venue added: SIM, MARGIN, $1,000,000")

    engine.add_instrument(instrument)
    print("[5] Instrument added")

    base_ts = 1_700_000_000_000_000_000
    day_ns = 86_400_000_000_000
    prices = ["50000.00", "51000.00", "49000.00", "52000.00", "50500.00"]

    bars = []
    for i, close in enumerate(prices):
        ts = base_ts + i * day_ns
        price_f = float(close)
        bar = make_bar(
            bar_type, ts,
            open_=f"{price_f - 100:.2f}",
            high=f"{price_f + 200:.2f}",
            low=f"{price_f - 200:.2f}",
            close=close,
            volume="1000.000000",
        )
        bars.append(bar)

    print(f"\n[6] Created {len(bars)} bars")

    print("\n" + "-" * 60)
    print("Streaming Mode: step-by-step")
    print("-" * 60)

    all_passed = True

    for i, bar in enumerate(bars):
        print(f"\n--- Step {i + 1} ---")
        print(f"  Bar close={float(bar.close)} ts={bar.ts_event}")

        engine.add_data([bar], validate=False)
        engine.run(streaming=True)
        engine.clear_data()

        equity_dict = engine.portfolio.equity(venue=Venue("SIM"))
        print(f"  equity() result: {equity_dict}")

        if not equity_dict:
            print("  ❌ FAIL: equity dict is empty")
            all_passed = False
            continue

        usd_key = Currency.from_str("USD")
        val = equity_dict.get(usd_key)
        if val is None:
            keys = list(equity_dict.keys())
            val = equity_dict[keys[0]]
            usd_key = keys[0]

        val_type = type(val).__name__
        print(f"  Equity value type: {val_type}")
        print(f"  Equity value: {val}")

        if isinstance(val, float):
            print("  ✅ Equity is float (EP assumes Money.as_double() — WRONG)")
        else:
            print(f"  ❌ Equity is {val_type}, not float — unexpected")
            all_passed = False

        positions = engine.cache.positions_open()
        print(f"  Open positions: {len(positions)}")
        for p in positions:
            print(f"    {p}")

    print("\n" + "-" * 60)
    print("Cleanup")
    print("-" * 60)

    engine.end()
    print("engine.end() OK")

    if all_passed:
        print("\n✅ POC 1 PASSED: Streaming mode works + equity returns dict[Currency, float]")
        print("   EP CORRECTION NEEDED: _get_equity() must use float directly, NOT .as_double()")
    else:
        print("\n❌ POC 1 FAILED: See errors above")

    return all_passed


if __name__ == "__main__":
    main()
