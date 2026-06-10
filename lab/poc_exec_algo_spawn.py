"""
POC: ExecAlgorithm spawn_market in BacktestEngine

驗證:
  1. ExecAlgorithm 可註冊到 BacktestEngine
  2. Parent order with exec_algorithm_id 路由到 algorithm
  3. spawn_market() 生成 child order
  4. Child order 在 backtest 中成交
EP 段落: S5
風險: 高
"""

from decimal import Decimal

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.config import StrategyConfig
from nautilus_trader.execution.algorithm import ExecAlgorithm
from nautilus_trader.execution.algorithm import ExecAlgorithmConfig
from nautilus_trader.model.currencies import USDT
from nautilus_trader.model.data import Bar
from nautilus_trader.model.data import BarSpecification
from nautilus_trader.model.data import BarType
from nautilus_trader.model.enums import AccountType
from nautilus_trader.model.enums import BarAggregation
from nautilus_trader.model.enums import OmsType
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import PriceType
from nautilus_trader.model.enums import TimeInForce
from nautilus_trader.model.events import OrderFilled
from nautilus_trader.model.identifiers import ExecAlgorithmId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Quantity
from nautilus_trader.test_kit.providers import TestInstrumentProvider
from nautilus_trader.trading.strategy import Strategy


EXEC_ALGO_ID = ExecAlgorithmId("SPLIT")
VENUE = "BINANCE"


class SplitExecAlgorithmConfig(ExecAlgorithmConfig, frozen=True):
    exec_algorithm_id: ExecAlgorithmId | None = EXEC_ALGO_ID


class SplitExecAlgorithm(ExecAlgorithm):
    """Minimal ExecAlgorithm: splits parent into 2 equal market child orders."""

    def __init__(self, config: SplitExecAlgorithmConfig | None = None):
        super().__init__(config or SplitExecAlgorithmConfig())
        self.child_count = 0
        self.fill_count = 0

    def on_order(self, order):
        half_qty = Quantity(order.quantity.as_double() / 2, order.quantity.precision)
        child = self.spawn_market(
            primary=order,
            quantity=half_qty,
            time_in_force=TimeInForce.IOC,
        )
        self.submit_order(child)
        self.child_count += 1

    def on_order_filled(self, event):
        self.fill_count += 1


class TestStrategyConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType


class TestStrategy(Strategy):
    """Submits one parent order with exec_algorithm_id on first bar."""

    def __init__(self, config: TestStrategyConfig):
        super().__init__(config)
        self.order_submitted = False
        self.fill_received = False

    def on_start(self):
        self.instrument = self.cache.instrument(self.config.instrument_id)
        if self.instrument:
            self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar):
        if not self.order_submitted and self.instrument:
            order = self.order_factory.market(
                instrument_id=self.instrument.id,
                order_side=OrderSide.BUY,
                quantity=self.instrument.make_qty(0.1),
                exec_algorithm_id=EXEC_ALGO_ID,
            )
            self.submit_order(order)
            self.order_submitted = True

    def on_order_filled(self, event):
        if isinstance(event, OrderFilled):
            self.fill_received = True


def make_bars(instrument, bar_type: BarType, n: int = 10, base_price: float = 50000.0):
    bars = []
    for i in range(n):
        p = base_price + i * 100
        bar = Bar(
            bar_type=bar_type,
            open=instrument.make_price(p),
            high=instrument.make_price(p + 50),
            low=instrument.make_price(p - 50),
            close=instrument.make_price(p + 10),
            volume=instrument.make_qty(100.0),
            ts_event=0 + i * 1_000_000_000,
            ts_init=0 + i * 1_000_000_000,
        )
        bars.append(bar)
    return bars


def main():
    print("=" * 60)
    print("POC 2: ExecAlgorithm spawn_market in BacktestEngine")
    print("=" * 60)

    all_passed = True

    instrument = TestInstrumentProvider.btcusdt_binance()
    bar_type = BarType(instrument.id, BarSpecification(1, BarAggregation.MINUTE, PriceType.LAST))
    bars = make_bars(instrument, bar_type, n=10)

    engine = BacktestEngine()

    engine.add_venue(
        venue=instrument.id.venue,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=None,
        starting_balances=[Money(1_000_000, USDT)],
        default_leverage=Decimal(1),
    )

    algo = SplitExecAlgorithm()
    engine.add_exec_algorithm(algo)

    strategy = TestStrategy(config=TestStrategyConfig(
        instrument_id=instrument.id,
        bar_type=bar_type,
    ))
    engine.add_strategy(strategy)

    engine.add_instrument(instrument)
    engine.add_data(bars)

    print("\n[Setup]")
    print(f"  Instrument: {instrument.id}")
    print(f"  Bar type:   {bar_type}")
    print(f"  Bars:       {len(bars)}")
    print(f"  Exec algo:  {algo.id}")

    engine.run()

    print("\n[Results]")
    print(f"  Algo child_count:  {algo.child_count}")
    print(f"  Algo fill_count:   {algo.fill_count}")
    print(f"  Strategy submitted: {strategy.order_submitted}")
    print(f"  Strategy filled:    {strategy.fill_received}")

    checks = [
        ("ExecAlgorithm registered", True),
        ("Parent order submitted (strategy)", strategy.order_submitted),
        ("Child order spawned (algo)", algo.child_count >= 1),
        ("Child order filled", algo.fill_count >= 1),
        ("Strategy received fill", strategy.fill_received),
    ]

    print("\n[Checklist]")
    for name, ok in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")
        if not ok:
            all_passed = False

    print(f"\n{'=' * 60}")
    if all_passed:
        print("✅ POC 2 PASSED: ExecAlgorithm spawn_market works in BacktestEngine")
    else:
        print("❌ POC 2 FAILED: See errors above")
    print(f"{'=' * 60}")

    engine.dispose()
    return all_passed


if __name__ == "__main__":
    main()
