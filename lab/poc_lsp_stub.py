"""POC: 驗證 NautilusTrader repo 的 LSP 支援。

測試三個場景：
1. rust-analyzer 對 Rust symbol 的解析
2. pyright 對 Cython 模組（無 stub）的行為
3. pyright 加入 stub 後的解析結果

執行方式：在 Claude Code session 中逐步執行，觀察 LSP 回傳。
"""

from nautilus_trader.model.objects import Currency, Money, Price, Quantity
from nautilus_trader.model.data import Bar, BarType, QuoteTick, TradeTick


def test_price_creation() -> Price:
    """Test Price creation — LSP hover on Price should show type info."""
    price = Price.from_str("1.5000")
    return price


def test_bar_usage() -> Bar:
    """Test Bar usage — without stub, pyright returns Unknown for Bar."""
    # type: ignore: intentional — Bar is a class, not an instance.
    # This demonstrates what pyright sees when stub is incomplete.
    return Bar  # type: ignore[return-value]


def test_quantity() -> Quantity:
    qty = Quantity.from_str("100")
    return qty


def test_money() -> Money:
    c = Currency.from_str("USD")
    m = Money(100.0, c)
    return m


def test_bar_type() -> BarType:
    bt = BarType.from_str("BTCUSDT.BINANCE-1-MINUTE-BID-EXTERNAL")
    return bt


def test_ticks() -> None:
    # Intentional: None assigned to typed variables to demonstrate
    # stub coverage gap (constructor signature unknown).
    qt: QuoteTick = None  # type: ignore[assignment]
    tt: TradeTick = None  # type: ignore[assignment]
