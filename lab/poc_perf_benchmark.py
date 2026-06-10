"""
POC: Performance benchmark for NT Gym step() and reset()

測量:
  1. step() 延遲：add_data → run(streaming=True) → clear_data
  2. reset() 延遲：new BacktestEngine + venue + instrument + strategy
  3. 對比：純 numpy 計算的 step()（理想上限）

EP 段落: S1
風險: 中（效能敏感路徑）
"""

import time
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


def make_btc_instrument():
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


def make_bar(bar_type, ts_event, price):
    return Bar(
        bar_type=bar_type,
        open=Price.from_str(f"{price - 50:.2f}"),
        high=Price.from_str(f"{price + 100:.2f}"),
        low=Price.from_str(f"{price - 100:.2f}"),
        close=Price.from_str(f"{price:.2f}"),
        volume=Quantity.from_str("1000.000000"),
        ts_event=ts_event,
        ts_init=ts_event,
    )


class NoOpStrategy(Strategy):
    def __init__(self):
        super().__init__(config=StrategyConfig(order_id_tag="BENCH"))

    def on_bar(self, bar):
        pass


def create_engine(instrument, bar_type):
    engine = BacktestEngine(config=BacktestEngineConfig(trader_id=TraderId("BENCH-001")))
    engine.add_venue(
        venue=Venue("SIM"),
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
        fee_model=MakerTakerFeeModel(),
    )
    engine.add_instrument(instrument)
    strategy = NoOpStrategy()
    engine.add_strategy(strategy)
    return engine


def benchmark_step():
    print("=" * 60)
    print("Bench 1: step() latency (no order)")
    print("=" * 60)

    instrument = make_btc_instrument()
    bar_type = BarType(
        instrument.id,
        BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
        AggregationSource.EXTERNAL,
    )

    engine = create_engine(instrument, bar_type)

    base_ts = 1_700_000_000_000_000_000
    day_ns = 86_400_000_000_000

    N = 500
    latencies = []

    for i in range(N):
        ts = base_ts + i * day_ns
        price = 50000.0 + (i % 100) * 100.0
        bar = make_bar(bar_type, ts, price)

        t0 = time.perf_counter_ns()
        engine.add_data([bar], validate=False)
        engine.run(streaming=True)
        engine.clear_data()
        t1 = time.perf_counter_ns()

        latencies.append((t1 - t0) / 1_000_000)

    engine.end()

    avg_ms = sum(latencies) / len(latencies)
    p50 = sorted(latencies)[len(latencies) // 2]
    p99 = sorted(latencies)[int(len(latencies) * 0.99)]
    max_ms = max(latencies)
    min_ms = min(latencies)

    print(f"  Steps: {N}")
    print(f"  Avg:   {avg_ms:.2f} ms")
    print(f"  P50:   {p50:.2f} ms")
    print(f"  P99:   {p99:.2f} ms")
    print(f"  Min:   {min_ms:.2f} ms")
    print(f"  Max:   {max_ms:.2f} ms")
    print(f"  Steps/sec: {1000 / avg_ms:.0f}")

    return avg_ms


def benchmark_step_with_order():
    print("\n" + "=" * 60)
    print("Bench 2: step() latency (with order per step)")
    print("=" * 60)

    instrument = make_btc_instrument()

    class AlwaysBuyStrategy(Strategy):
        def __init__(self):
            super().__init__(config=StrategyConfig(order_id_tag="BUY"))
            self._count = 0

        def on_bar(self, bar):
            if self._count % 2 == 0:
                qty = Quantity(0.1, precision=instrument.size_precision)
                order = self.order_factory.market(instrument.id, OrderSide.BUY, qty)
                self.submit_order(order)
            self._count += 1

    bar_type = BarType(
        instrument.id,
        BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
        AggregationSource.EXTERNAL,
    )

    engine = BacktestEngine(config=BacktestEngineConfig(trader_id=TraderId("BENCH-002")))
    engine.add_venue(
        venue=Venue("SIM"),
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money(1_000_000, Currency.from_str("USD"))],
        fee_model=MakerTakerFeeModel(),
    )
    engine.add_instrument(instrument)
    strategy = AlwaysBuyStrategy()
    engine.add_strategy(strategy)

    base_ts = 1_700_000_000_000_000_000
    day_ns = 86_400_000_000_000

    N = 500
    latencies = []

    for i in range(N):
        ts = base_ts + i * day_ns
        price = 50000.0 + (i % 100) * 100.0
        bar = make_bar(bar_type, ts, price)

        t0 = time.perf_counter_ns()
        engine.add_data([bar], validate=False)
        engine.run(streaming=True)
        engine.clear_data()
        t1 = time.perf_counter_ns()

        latencies.append((t1 - t0) / 1_000_000)

    engine.end()

    avg_ms = sum(latencies) / len(latencies)
    p50 = sorted(latencies)[len(latencies) // 2]
    p99 = sorted(latencies)[int(len(latencies) * 0.99)]

    print(f"  Steps: {N}")
    print(f"  Avg:   {avg_ms:.2f} ms")
    print(f"  P50:   {p50:.2f} ms")
    print(f"  P99:   {p99:.2f} ms")
    print(f"  Steps/sec: {1000 / avg_ms:.0f}")

    return avg_ms


def benchmark_reset():
    print("\n" + "=" * 60)
    print("Bench 3: reset() latency (new engine per episode)")
    print("=" * 60)

    instrument = make_btc_instrument()
    bar_type = BarType(
        instrument.id,
        BarSpecification(1, BarAggregation.DAY, PriceType.LAST),
        AggregationSource.EXTERNAL,
    )

    N = 50
    latencies = []

    for _ in range(N):
        t0 = time.perf_counter_ns()
        engine = create_engine(instrument, bar_type)
        engine.end()
        t1 = time.perf_counter_ns()
        latencies.append((t1 - t0) / 1_000_000)

    avg_ms = sum(latencies) / len(latencies)
    p50 = sorted(latencies)[len(latencies) // 2]

    print(f"  Resets: {N}")
    print(f"  Avg:    {avg_ms:.2f} ms")
    print(f"  P50:    {p50:.2f} ms")

    return avg_ms


def estimate_training_time(step_ms, reset_ms):
    print("\n" + "=" * 60)
    print("Estimated Training Time")
    print("=" * 60)

    steps_per_episode = 1000
    episodes = 100
    total_steps = steps_per_episode * episodes

    step_time = total_steps * step_ms / 1000
    reset_time = episodes * reset_ms / 1000
    total_time = step_time + reset_time

    print(f"  Steps/episode: {steps_per_episode}")
    print(f"  Episodes: {episodes}")
    print(f"  Total steps: {total_steps}")
    print(f"  Step time: {step_time:.1f}s")
    print(f"  Reset time: {reset_time:.1f}s")
    print(f"  Total: {total_time:.1f}s ({total_time/60:.1f}min)")

    steps_per_episode = 252  # 1 year daily bars
    episodes = 500
    total_steps = steps_per_episode * episodes
    step_time = total_steps * step_ms / 1000
    reset_time = episodes * reset_ms / 1000
    total_time = step_time + reset_time

    print("\n  Realistic scenario (1yr daily bars, 500 episodes):")
    print(f"  Steps/episode: {steps_per_episode}")
    print(f"  Episodes: {episodes}")
    print(f"  Total steps: {total_steps}")
    print(f"  Step time: {step_time:.1f}s")
    print(f"  Reset time: {reset_time:.1f}s")
    print(f"  Total: {total_time:.1f}s ({total_time/60:.1f}min)")


if __name__ == "__main__":
    step_ms = benchmark_step()
    step_order_ms = benchmark_step_with_order()
    reset_ms = benchmark_reset()
    estimate_training_time(step_order_ms, reset_ms)
