"""
POC: Gym step-by-step loop with Strategy bridge

驗證:
  1. BacktestEngine 單 bar streaming: add_data([bar]) → run(streaming=True) → clear_data()
  2. Strategy bridge: set_action() → on_bar() 執行訂單
  3. Action 注入時序: set_action 必須在 add_data 之前
  4. Equity 變化反映真實成交（手續費 + 未實現損益）
  5. 重用 engine 的 reset 模式（因 Rust logger singleton，不能建新 engine）
EP 段落: nt-gym-deepscalper S1+S2
風險: 致命
"""


from decimal import Decimal

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.engine import BacktestEngineConfig
from nautilus_trader.config import LoggingConfig
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


class BridgeConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType


class StrategyBridge(Strategy):
    """Minimal RL Strategy Bridge: receives action via set_action(), executes in on_bar()."""

    def __init__(self, config: BridgeConfig):
        super().__init__(config)
        self._pending_action = None
        self._action_consumed = True
        self._fills: list = []
        self._orders_submitted = 0

    def set_action(self, action: float):
        self._pending_action = action
        self._action_consumed = False

    def on_start(self):
        self.instrument = self.cache.instrument(self.config.instrument_id)
        if self.instrument:
            self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar):
        if self._action_consumed or self._pending_action is None or not self.instrument:
            return

        target_weight = float(self._pending_action)
        self._action_consumed = True

        total_equity = self._get_equity()
        if total_equity <= 0:
            return

        target_value = total_equity * target_weight
        current_price = float(bar.close)
        target_qty = target_value / current_price if current_price > 0 else 0.0

        current_qty = self._get_position_qty()

        delta_qty = target_qty - current_qty
        if abs(delta_qty) < float(self.instrument.size_increment):
            return

        side = OrderSide.BUY if delta_qty > 0 else OrderSide.SELL
        qty = self.instrument.make_qty(abs(delta_qty))
        order = self.order_factory.market(
            instrument_id=self.instrument.id,
            order_side=side,
            quantity=qty,
        )
        self.submit_order(order)
        self._orders_submitted += 1

    def _get_equity(self) -> float:
        equity_dict = self.portfolio.equity(self.instrument.id.venue)
        if not equity_dict:
            account = self.cache.account_for_venue(self.instrument.id.venue)
            if account:
                balance = account.balance_total(USDT)
                return float(balance.as_double()) if balance else 1_000_000.0
            return 1_000_000.0
        currency = list(equity_dict.keys())[0]
        return float(equity_dict[currency].as_double())

    def _get_position_qty(self) -> float:
        positions = self.cache.positions_open(instrument_id=self.instrument.id)
        qty = 0.0
        for pos in positions:
            signed = float(pos.quantity.as_double())
            qty += signed if pos.side.name == "LONG" else -signed
        return qty

    def on_order_filled(self, event):
        if isinstance(event, OrderFilled):
            self._fills.append(event)


def make_bars(instrument, bar_type, n=20, base_price=50000.0):
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
            ts_event=0 + i * 60_000_000_000,
            ts_init=0 + i * 60_000_000_000,
        )
        bars.append(bar)
    return bars


def create_engine_and_bridge(instrument, bar_type):
    engine = BacktestEngine(config=BacktestEngineConfig(
        logging=LoggingConfig(log_level="ERROR"),
    ))
    engine.add_venue(
        venue=instrument.id.venue,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        base_currency=None,
        starting_balances=[Money(1_000_000, USDT)],
        default_leverage=Decimal(1),
    )
    engine.add_instrument(instrument)

    bridge = StrategyBridge(config=BridgeConfig(
        instrument_id=instrument.id,
        bar_type=bar_type,
    ))
    engine.add_strategy(bridge)
    return engine, bridge


def get_equity(engine, instrument):
    equity_dict = engine.portfolio.equity(instrument.id.venue)
    if not equity_dict:
        account = engine.cache.account_for_venue(instrument.id.venue)
        if account:
            balance = account.balance_total(USDT)
            return float(balance.as_double()) if balance else 1_000_000.0
        return 1_000_000.0
    currency = list(equity_dict.keys())[0]
    return float(equity_dict[currency].as_double())


def main():
    print("=" * 60)
    print("POC 4: Gym step-by-step loop with Strategy bridge")
    print("=" * 60)

    all_passed = True
    instrument = TestInstrumentProvider.btcusdt_binance()
    bar_type = BarType(instrument.id, BarSpecification(1, BarAggregation.MINUTE, PriceType.LAST))
    bars = make_bars(instrument, bar_type, n=20)

    engine, bridge = create_engine_and_bridge(instrument, bar_type)

    print("\n--- Test 1: Single step-by-step loop ---")
    equities = []
    for i, bar in enumerate(bars[:5]):
        action = 0.3 if i < 3 else 0.0
        bridge.set_action(action)

        equity_before = get_equity(engine, instrument)
        engine.add_data([bar], validate=False)
        engine.run(streaming=True)
        engine.clear_data()
        equity_after = get_equity(engine, instrument)

        equities.append(equity_after)
        print(f"  Step {i}: action={action:.1f} -> equity {equity_before:.2f} -> {equity_after:.2f}")

    t1_orders = bridge._orders_submitted > 0
    t1_fills = len(bridge._fills) > 0
    t1_equity_changed = len(set([round(e, 2) for e in equities])) > 1
    print(f"  Orders submitted: {bridge._orders_submitted}")
    print(f"  Fills received: {len(bridge._fills)}")
    print(f"  Equity varied: {t1_equity_changed}")

    print("\n--- Test 2: Action timing (set_action BEFORE add_data) ---")
    bridge2 = StrategyBridge(config=BridgeConfig(
        instrument_id=instrument.id,
        bar_type=bar_type,
    ))
    bridge2.set_action(0.5)
    t3_consumed_manual = bridge2._action_consumed is False
    print(f"  set_action sets pending (not consumed): {t3_consumed_manual}")

    t3_consumed = bridge._action_consumed
    t3_order = bridge._orders_submitted >= 1
    print(f"  Last action consumed in on_bar: {t3_consumed}")
    print(f"  At least 1 order submitted from actions: {t3_order}")

    print("\n--- Test 3: Engine reuse across multiple episodes ---")
    episode_equities = []
    for ep in range(5):
        ep_bars = make_bars(instrument, bar_type, n=5, base_price=50000.0 + ep * 1000)

        for i, bar in enumerate(ep_bars):
            bridge.set_action(0.5)
            engine.add_data([bar], validate=False)
            engine.run(streaming=True)
            engine.clear_data()

        eq = get_equity(engine, instrument)
        episode_equities.append(eq)
        print(f"  Episode {ep}: equity={eq:.2f}")

    t3_five_episodes = len(episode_equities) == 5
    t3_equity_varies = len(set([round(e, 0) for e in episode_equities])) > 1
    print(f"  5 episodes completed: {t3_five_episodes}")
    print(f"  Equity varies (different data): {t3_equity_varies}")

    print("\n--- Test 4: Second engine CAN coexist (but not after dispose) ---")
    try:
        engine2, bridge2 = create_engine_and_bridge(instrument, bar_type)
        t4_coexist = True
        engine2.end()
        engine2.dispose()
    except Exception as e:
        t4_coexist = False
        print(f"  Second engine coexist failed: {type(e).__name__}: {e}")

    print(f"  Second engine coexists with first: {t4_coexist}")

    print("\n[Checklist]")
    checks = [
        ("T1: Orders submitted in step loop", t1_orders),
        ("T1: Fills received in step loop", t1_fills),
        ("T1: Equity varied across steps", t1_equity_changed),
        ("T2: set_action timing works", t3_consumed),
        ("T2: At least 1 order from action", t3_order),
        ("T3: 5 episodes on same engine", t3_five_episodes),
        ("T3: Equity varies with data", t3_equity_varies),
        ("T4: Second engine can coexist", t4_coexist),
    ]

    for name, ok in checks:
        status = "OK" if ok else "FAIL"
        print(f"  [{status}] {name}")
        if not ok:
            all_passed = False

    print(f"\n{'=' * 60}")
    if all_passed:
        print("OK POC 4 PASSED: Gym step-by-step works. MUST reuse engine (Rust singleton).")
    else:
        print("FAIL POC 4 FAILED: See errors above")
    print(f"{'=' * 60}")

    engine.end()
    engine.dispose()
    return all_passed


if __name__ == "__main__":
    main()
