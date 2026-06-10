"""
Phase 1: Market Event Tokenizer
=================================
Teaches how to convert raw market data (OHLCV bars) into discrete token
sequences suitable for a foundation model (like Mamba).

Key concepts:
1. EventVocabulary: Define ~30 tokens covering market states and events
2. Bar data: Namedtuple with open/high/low/close/volume
3. MarketEventTokenizer: Accumulate bars, compute MA/ATR, classify into tokens
4. Token sequences capture: trend, volatility, volume regime, and discrete events

This is the "tokenizer" for market data - analogous to BPE tokenization for text.
"""

import math
from collections import Counter
from collections import namedtuple
from typing import List


# ============================================================================
# 1. Bar data structure
# ============================================================================

Bar = namedtuple("Bar", ["open", "high", "low", "close", "volume"])


# ============================================================================
# 2. Event Vocabulary
# ============================================================================

class EventVocabulary:
    """
    Market event vocabulary with ~30 tokens.

    Token categories:
        - Special: PAD (0), BOS (1), EOS (2), SEP (3)
        - Trend: STRONG_UP, TREND_UP, SIDEWAY, TREND_DOWN, STRONG_DOWN
        - Volatility: VOL_LOW, VOL_NORMAL, VOL_HIGH, VOL_EXTREME
        - Volume: VOL_DRY, VOL_NORMAL_VOL, VOL_ACTIVE, VOL_SURGE
        - Events: GAP_UP, GAP_DOWN, BREAKOUT_UP, BREAKOUT_DOWN,
                  REVERSAL_UP, REVERSAL_DOWN, NEW_HIGH, NEW_LOW, DOJI, HAMMER
    """

    # Token definitions: (id, name)
    TOKENS = {
        # Special tokens
        "PAD": 0,
        "BOS": 1,
        "EOS": 2,
        "SEP": 3,
        # Trend states (5)
        "STRONG_UP": 4,
        "TREND_UP": 5,
        "SIDEWAY": 6,
        "TREND_DOWN": 7,
        "STRONG_DOWN": 8,
        # Volatility states (4)
        "VOL_LOW": 9,
        "VOL_NORMAL": 10,
        "VOL_HIGH": 11,
        "VOL_EXTREME": 12,
        # Volume states (4)
        "VOL_DRY": 13,
        "VOL_NORMAL_VOL": 14,
        "VOL_ACTIVE": 15,
        "VOL_SURGE": 16,
        # Discrete events (12)
        "GAP_UP": 17,
        "GAP_DOWN": 18,
        "BREAKOUT_UP": 19,
        "BREAKOUT_DOWN": 20,
        "REVERSAL_UP": 21,
        "REVERSAL_DOWN": 22,
        "NEW_HIGH": 23,
        "NEW_LOW": 24,
        "DOJI": 25,
        "HAMMER": 26,
        "SHOOTING_STAR": 27,
        "ENGULFING_BULL": 28,
        "ENGULFING_BEAR": 29,
    }

    def __init__(self):
        self.id_to_name = {v: k for k, v in self.TOKENS.items()}
        self.vocab_size = len(self.TOKENS)

    def get_id(self, name: str) -> int:
        return self.TOKENS[name]

    def get_name(self, token_id: int) -> str:
        return self.id_to_name.get(token_id, f"UNKNOWN_{token_id}")

    def encode_sequence(self, names: List[str]) -> List[int]:
        return [self.TOKENS[n] for n in names]

    def decode_sequence(self, ids: List[int]) -> List[str]:
        return [self.get_name(i) for i in ids]


# ============================================================================
# 3. Market Event Tokenizer
# ============================================================================

class MarketEventTokenizer:
    """
    Convert raw OHLCV bars into discrete token sequences.

    Processing pipeline:
        1. Accumulate bars into a sliding window
        2. Compute technical indicators (MA, ATR, volume stats)
        3. Classify each bar into: trend_token, vol_token, volume_token, event_token
        4. Return token sequence: [BOS, t1_trend, t1_vol, t1_volume, t1_event, SEP, ..., EOS]
    """

    def __init__(self, vocab: EventVocabulary, window: int = 20):
        self.vocab = vocab
        self.window = window

    def compute_sma(self, closes: List[float], period: int) -> float:
        if len(closes) < period:
            return closes[-1] if closes else 0.0
        return sum(closes[-period:]) / period

    def compute_atr(self, bars: List[Bar], period: int = 14) -> float:
        if len(bars) < 2:
            return 0.01
        trs = []
        for i in range(1, min(len(bars), period + 1)):
            bar = bars[-i]
            prev = bars[-i - 1]
            tr = max(
                bar.high - bar.low,
                abs(bar.high - prev.close),
                abs(bar.low - prev.close),
            )
            trs.append(tr)
        return sum(trs) / len(trs) if trs else 0.01

    def compute_volume_stats(self, bars: List[Bar], period: int = 20):
        if not bars:
            return 0.0, 0.0
        volumes = [b.volume for b in bars[-period:]]
        mean_vol = sum(volumes) / len(volumes)
        std_vol = math.sqrt(sum((v - mean_vol) ** 2 for v in volumes) / len(volumes))
        return mean_vol, std_vol

    def classify_trend(self, bar: Bar, sma_short: float, sma_long: float) -> str:
        """Classify trend based on price vs moving averages."""
        diff_pct = (bar.close - sma_long) / sma_long if sma_long > 0 else 0.0

        if bar.close > sma_short > sma_long and diff_pct > 0.03:
            return "STRONG_UP"
        elif bar.close > sma_short and diff_pct > 0.01:
            return "TREND_UP"
        elif bar.close < sma_short < sma_long and diff_pct < -0.03:
            return "STRONG_DOWN"
        elif bar.close < sma_short and diff_pct < -0.01:
            return "TREND_DOWN"
        else:
            return "SIDEWAY"

    def classify_volatility(self, atr: float, avg_atr: float) -> str:
        """Classify volatility based on ATR relative to average."""
        if avg_atr <= 0:
            return "VOL_NORMAL"
        ratio = atr / avg_atr
        if ratio < 0.5:
            return "VOL_LOW"
        elif ratio < 1.5:
            return "VOL_NORMAL"
        elif ratio < 2.5:
            return "VOL_HIGH"
        else:
            return "VOL_EXTREME"

    def classify_volume(self, bar: Bar, mean_vol: float, std_vol: float) -> str:
        """Classify volume regime."""
        if mean_vol <= 0:
            return "VOL_NORMAL_VOL"
        ratio = bar.volume / mean_vol
        if ratio < 0.3:
            return "VOL_DRY"
        elif ratio < 0.7:
            return "VOL_NORMAL_VOL"
        elif ratio < 1.5:
            return "VOL_ACTIVE"
        else:
            return "VOL_SURGE"

    def detect_events(self, bars: List[Bar]) -> List[str]:
        """Detect discrete candlestick events for the latest bar."""
        events = []
        if len(bars) < 2:
            return events

        bar = bars[-1]
        prev = bars[-2]
        body = abs(bar.close - bar.open)
        full_range = bar.high - bar.low

        # Gap detection
        if bar.open > prev.close * 1.005:
            events.append("GAP_UP")
        elif bar.open < prev.close * 0.995:
            events.append("GAP_DOWN")

        # Doji: very small body relative to range
        if full_range > 0 and body / full_range < 0.1:
            events.append("DOJI")

        # Hammer: small body at top, long lower shadow
        lower_shadow = min(bar.open, bar.close) - bar.low
        upper_shadow = bar.high - max(bar.open, bar.close)
        if full_range > 0 and body / full_range < 0.3 and lower_shadow > body * 2:
            events.append("HAMMER")

        # Shooting star: small body at bottom, long upper shadow
        if full_range > 0 and body / full_range < 0.3 and upper_shadow > body * 2:
            events.append("SHOOTING_STAR")

        # Bullish engulfing
        if (prev.close < prev.open and bar.close > bar.open
                and bar.open <= prev.close and bar.close >= prev.open):
            events.append("ENGULFING_BULL")

        # Bearish engulfing
        if (prev.close > prev.open and bar.close < bar.open
                and bar.open >= prev.close and bar.close <= prev.open):
            events.append("ENGULFING_BEAR")

        # Reversal detection (simplified)
        if len(bars) >= 3:
            # Upside reversal: bar0 down, bar1 down, bar2 up strongly
            b0, b1, b2 = bars[-3], bars[-2], bars[-1]
            if b0.close < b0.open and b1.close < b1.open and b2.close > b2.open:
                events.append("REVERSAL_UP")
            elif b0.close > b0.open and b1.close > b1.open and b2.close < b2.open:
                events.append("REVERSAL_DOWN")

        # New high/low in window
        closes = [b.close for b in bars]
        if bar.close == max(closes):
            events.append("NEW_HIGH")
        elif bar.close == min(closes):
            events.append("NEW_LOW")

        return events

    def tokenize(self, bars: List[Bar]) -> List[int]:
        """
        Convert a sequence of bars into token IDs.

        For each bar (starting from bar index where we have enough history):
            [trend_token, vol_token, volume_token, event_token(s)]

        Full sequence: [BOS, bar1_tokens..., SEP, bar2_tokens..., SEP, ..., EOS]
        """
        if len(bars) < 3:
            return [self.vocab.get_id("BOS"), self.vocab.get_id("EOS")]

        tokens = [self.vocab.get_id("BOS")]

        # Compute average ATR for volatility classification
        all_atrs = []
        for i in range(1, len(bars)):
            tr = max(
                bars[i].high - bars[i].low,
                abs(bars[i].high - bars[i - 1].close),
                abs(bars[i].low - bars[i - 1].close),
            )
            all_atrs.append(tr)
        avg_atr = sum(all_atrs) / len(all_atrs) if all_atrs else 0.01

        mean_vol, std_vol = self.compute_volume_stats(bars)

        for i in range(2, len(bars)):
            window_bars = bars[:i + 1]
            closes = [b.close for b in window_bars]

            sma_short = self.compute_sma(closes, min(5, len(closes)))
            sma_long = self.compute_sma(closes, min(20, len(closes)))
            atr = self.compute_atr(window_bars)

            bar = window_bars[-1]

            # Classify
            trend = self.classify_trend(bar, sma_short, sma_long)
            vol = self.classify_volatility(atr, avg_atr)
            volume = self.classify_volume(bar, mean_vol, std_vol)

            tokens.append(self.vocab.get_id(trend))
            tokens.append(self.vocab.get_id(vol))
            tokens.append(self.vocab.get_id(volume))

            # Events
            events = self.detect_events(window_bars)
            if events:
                for event in events:
                    tokens.append(self.vocab.get_id(event))
            else:
                # Use PAD when no event detected (simplification)
                pass

            tokens.append(self.vocab.get_id("SEP"))

        tokens.append(self.vocab.get_id("EOS"))
        return tokens

    def tokenize_to_names(self, bars: List[Bar]) -> List[str]:
        """Tokenize and return human-readable token names."""
        ids = self.tokenize(bars)
        return self.vocab.decode_sequence(ids)


# ============================================================================
# 4. Synthetic Data Generators
# ============================================================================

def generate_uptrend_bars(n: int = 30, start_price: float = 100.0, noise: float = 0.5) -> List[Bar]:
    """Generate bars in an uptrend."""
    bars = []
    price = start_price
    for i in range(n):
        o = price
        change = abs(math.sin(i * 0.3) * 0.5) + 0.2  # Positive bias
        c = o + change + (hash(str(i)) % 100 - 50) * noise * 0.01
        h = max(o, c) + abs(hash(str(i * 7)) % 100) * noise * 0.02
        l = min(o, c) - abs(hash(str(i * 3)) % 100) * noise * 0.01
        v = 1000 + abs(hash(str(i * 11)) % 5000)
        bars.append(Bar(o, h, l, c, v))
        price = c
    return bars


def generate_downtrend_bars(n: int = 30, start_price: float = 100.0, noise: float = 0.5) -> List[Bar]:
    """Generate bars in a downtrend."""
    bars = []
    price = start_price
    for i in range(n):
        o = price
        change = -abs(math.sin(i * 0.3) * 0.5) - 0.2  # Negative bias
        c = o + change + (hash(str(i + 100)) % 100 - 50) * noise * 0.01
        h = max(o, c) + abs(hash(str(i * 13)) % 100) * noise * 0.01
        l = min(o, c) - abs(hash(str(i * 5)) % 100) * noise * 0.02
        v = 1000 + abs(hash(str(i * 17)) % 5000)
        bars.append(Bar(o, h, l, c, v))
        price = c
    return bars


def generate_consolidation_bars(n: int = 30, base_price: float = 100.0, noise: float = 0.3) -> List[Bar]:
    """Generate bars in a consolidation (sideways) pattern."""
    bars = []
    for i in range(n):
        o = base_price
        change = math.sin(i * 0.5) * noise + (hash(str(i + 200)) % 100 - 50) * 0.01
        c = o + change
        h = max(o, c) + abs(hash(str(i * 19)) % 100) * noise * 0.005
        l = min(o, c) - abs(hash(str(i * 23)) % 100) * noise * 0.005
        v = 800 + abs(hash(str(i * 29)) % 2000)
        bars.append(Bar(o, h, l, c, v))
    return bars


def print_token_distribution(tokens: List[str], title: str):
    """Print token frequency distribution."""
    non_special = [t for t in tokens if t not in ("BOS", "EOS", "SEP", "PAD")]
    counter = Counter(non_special)
    total = len(non_special)

    print(f"\n  {title}")
    print(f"  Total tokens: {len(tokens)} (non-special: {total})")
    print("  Distribution:")
    for token, count in counter.most_common(10):
        pct = count / total * 100 if total > 0 else 0
        bar_str = "#" * int(pct / 2)
        print(f"    {token:<20s} {count:>3d} ({pct:>5.1f}%) {bar_str}")


# ============================================================================
# 5. Main demonstration
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 1: Market Event Tokenizer")
    print("=" * 70)

    # ---- 1. Vocabulary ----
    vocab = EventVocabulary()
    print(f"\n--- EventVocabulary ({vocab.vocab_size} tokens) ---")
    print("  Token Name -> ID mapping:")
    for name, id_ in sorted(vocab.TOKENS.items(), key=lambda x: x[1]):
        print(f"    {name:<20s} -> {id_:>2d}")

    # ---- 2. Tokenizer ----
    tokenizer = MarketEventTokenizer(vocab, window=20)

    # ---- 3. Test on 3 scenarios ----
    print("\n" + "=" * 70)
    print("Scenario Testing")
    print("=" * 70)

    # Scenario 1: Uptrend
    print("\n--- Scenario 1: UPTREND ---")
    up_bars = generate_uptrend_bars(30)
    up_tokens = tokenizer.tokenize_to_names(up_bars)
    print(f"  Generated {len(up_bars)} bars")
    print(f"  Token sequence (first 40): {up_tokens[:40]}")
    print(f"  Token sequence (last 20):  {up_tokens[-20:]}")
    print_token_distribution(up_tokens, "Uptrend Distribution")

    # Scenario 2: Downtrend
    print("\n--- Scenario 2: DOWNTREND ---")
    down_bars = generate_downtrend_bars(30)
    down_tokens = tokenizer.tokenize_to_names(down_bars)
    print(f"  Generated {len(down_bars)} bars")
    print(f"  Token sequence (first 40): {down_tokens[:40]}")
    print(f"  Token sequence (last 20):  {down_tokens[-20:]}")
    print_token_distribution(down_tokens, "Downtrend Distribution")

    # Scenario 3: Consolidation
    print("\n--- Scenario 3: CONSOLIDATION ---")
    side_bars = generate_consolidation_bars(30)
    side_tokens = tokenizer.tokenize_to_names(side_bars)
    print(f"  Generated {len(side_bars)} bars")
    print(f"  Token sequence (first 40): {side_tokens[:40]}")
    print(f"  Token sequence (last 20):  {side_tokens[-20:]}")
    print_token_distribution(side_tokens, "Consolidation Distribution")

    # ---- 4. Verification ----
    print("\n" + "=" * 70)
    print("Verification")
    print("=" * 70)

    # Deterministic: same input -> same output
    up_tokens_2 = tokenizer.tokenize_to_names(generate_uptrend_bars(30))
    assert up_tokens == up_tokens_2, "FAIL: Tokenizer is not deterministic!"
    print("  Deterministic: PASS (same input produces same output)")

    # Distribution not extreme (no single token > 80%)
    for scenario_name, tokens in [("Uptrend", up_tokens), ("Downtrend", down_tokens), ("Sideways", side_tokens)]:
        non_special = [t for t in tokens if t not in ("BOS", "EOS", "SEP", "PAD")]
        counter = Counter(non_special)
        max_pct = counter.most_common(1)[0][1] / len(non_special) * 100 if non_special else 0
        status = "PASS" if max_pct < 80 else "WARN"
        print(f"  {scenario_name} max token %: {max_pct:.1f}% -> {status}")

    # Token sequences are different for different scenarios
    assert up_tokens != down_tokens, "FAIL: Uptrend and downtrend produce same tokens!"
    assert up_tokens != side_tokens, "FAIL: Uptrend and sideways produce same tokens!"
    print("  Different scenarios produce different tokens: PASS")

    # All tokens in vocabulary
    all_token_ids = set()
    for tokens_list in [up_tokens, down_tokens, side_tokens]:
        for t in tokens_list:
            all_token_ids.add(vocab.get_id(t))
    vocab_coverage = len(all_token_ids) / vocab.vocab_size * 100
    print(f"  Vocabulary coverage: {len(all_token_ids)}/{vocab.vocab_size} tokens used ({vocab_coverage:.1f}%)")

    print("\n" + "=" * 70)
    print("Key Takeaways:")
    print("  1. Market data is continuous -> tokens are discrete (like BPE for text)")
    print("  2. Each bar produces: trend + volatility + volume + optional events")
    print("  3. Different market regimes produce different token distributions")
    print("  4. Tokenization is deterministic and invertible (decode available)")
    print("  5. This bridges raw market data and foundation model input")
    print("=" * 70)


if __name__ == "__main__":
    main()
