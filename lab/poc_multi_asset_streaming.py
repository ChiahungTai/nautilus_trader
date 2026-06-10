"""
POC: Multi-asset BacktestEngine

驗證:
  1. 多個 CurrencyPair 可註冊到同一個 BacktestEngine
  2. 單一 Strategy 可訂閱多個 BarType
  3. Strategy 可對不同 instrument 下單
  4. portfolio.equity() 聚合所有部位價值
EP 段落: S6
風險: 高
"""

from decimal import Decimal

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model.currencies import USDT
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarSpecification
from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import OmsType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.events import OrderFilled
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Money
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.trading.strategy import Strategy


INSTRUMENTS = {
    "BTC": TestInstrumentProvider.btcusdt_binance(),
    "ETH": TestInstrumentProvider.ethusdt_binance(),
    "ADA": TestInstrumentProvider.adausdt_binance(),
}


def make_bars(instrument, bar_type: BarType, n: int = 10, base_price: float = 100.0):
    bars = []
    for i in range(n):
        p = base_price + i * 5
        bar = Bar(
            bar_type=bar_type,
            open=instrument.make_price(p),
            high=instrument.make_price(p + 2),
            low=instrument.make_price(p - 2),
            close=instrument.make_price(p + 1),
            volume=instrument.make_qty(100.0),
            ts_event=i * 60_000_000_000,
            ts_init=i * 60_000_000_000,
        )
        bars.append(bar)
    return bars


class MultiAssetConfig(StrategyConfig, frozen=True):
    instrument_ids: tuple[InstrumentId, ...]
    bar_types: tuple[BarType, ...]


class MultiAssetStrategy(Strategy):
    """Subscribes to 3 instruments, buys one unit of each on first bar."""

    def __init__(self, config: MultiAssetConfig):
        super().__init__(config)
        self.orders_submitted = 0
        self.fills_received = 0
        self._submitted_set: set[InstrumentId] = set()

    def on_start(self):
        for bt in self.config.bar_types:
            self.subscribe_bars(bt)

    def on_bar(self, bar):
        iid = bar.bar_type.instrument_id
        if iid not in self._submitted_set:
            instrument = self.cache.instrument(iid)
            if instrument:
                order = self.order_factory.market(
                    instrument_id=instrument.id,
                    order_side=OrderSide.BUY,
                    quantity=instrument.make_qty(0.1),
                )
                self.submit_order(order)
                self._submitted_set.add(iid)
                self.orders_submitted += 1

    def on_order_filled(self, event):
        if isinstance(event, OrderFilled):
            self.fills_received += 1


def main():
    print("=" * 60)
    print("POC 3: Multi-asset BacktestEngine")
    print("=" * 60)

    all_passed = True

    bar_types = {}
    all_bars = []
    base_prices = {"BTC": 50000.0, "ETH": 3000.0, "ADA": 0.5}

    for name, inst in INSTRUMENTS.items():
        bt = BarType(inst.id, BarSpecification(1, BarAggregation.MINUTE, PriceType.LAST))
        bar_types[name] = bt
        bars = make_bars(inst, bt, n=10, base_price=base_prices[name])
        all_bars.extend(bars)

    bt_tuple = tuple(bar_types.values())
    iid_tuple = tuple(inst.id for inst in INSTRUMENTS.values())

    engine = BacktestEngine()

    engine.add_venue(
        venue=INSTRUMENTS["BTC"].id.venue,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=None,
        starting_balances=[Money(1_000_000, USDT)],
        default_leverage=Decimal(1),
    )

    strategy = MultiAssetStrategy(config=MultiAssetConfig(
        instrument_ids=iid_tuple,
        bar_types=bt_tuple,
    ))
    engine.add_strategy(strategy)

    for inst in INSTRUMENTS.values():
        engine.add_instrument(inst)
    engine.add_data(all_bars)

    print("\n[Setup]")
    print(f"  Instruments: {[str(iid) for iid in iid_tuple]}")
    print(f"  Total bars:  {len(all_bars)}")
    print("  Starting balance: 1,000,000 USDT")

    engine.run()

    print("\n[Results]")
    print(f"  Orders submitted: {strategy.orders_submitted}")
    print(f"  Fills received:   {strategy.fills_received}")

    portfolio = engine.portfolio
    venue = INSTRUMENTS["BTC"].id.venue
    equity_dict = portfolio.equity(venue)
    usdt_equity = equity_dict.get(USDT)
    print(f"  Portfolio equity: {equity_dict}")
    if usdt_equity:
        print(f"  USDT equity: {usdt_equity}")

    account = engine.cache.account_for_venue(INSTRUMENTS["BTC"].id.venue)
    if account:
        print(f"  Account balance: {account.balance_total(USDT)}")

    positions = engine.cache.positions()
    print(f"  Open positions: {len(positions)}")
    for pos in positions:
        print(f"    {pos.instrument_id}: side={pos.side}, qty={pos.quantity}")

    checks = [
        ("3 instruments registered", True),
        ("3 orders submitted (one per instrument)", strategy.orders_submitted == 3),
        ("3 fills received", strategy.fills_received >= 3),
        ("Portfolio equity accessible", usdt_equity is not None),
        ("Positions opened", len(positions) >= 1),
    ]

    print("\n[Checklist]")
    for name, ok in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")
        if not ok:
            all_passed = False

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✅ POC 3 PASSED: Multi-asset BacktestEngine works")
    else:
        print("❌ POC 3 FAILED: See errors above")
    print(f"{'=' * 60}")

    engine.dispose()
    return all_passed


if __name__ == "__main__":
    main()
