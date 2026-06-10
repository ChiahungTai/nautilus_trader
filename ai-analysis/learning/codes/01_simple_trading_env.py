"""
Phase 1: Gym Environment — Minimal Trading Environment

Teaches:
  - Building a custom gymnasium.Env from scratch
  - Discrete action space: BUY(0), HOLD(1), SELL(2)
  - State representation: [normalized_price, position, cash_ratio]
  - Reward design: realized PnL on SELL + unrealized PnL change
  - Episode termination logic
  - How a random agent interacts with a trading environment

Dependencies: numpy, gymnasium
"""

from __future__ import annotations

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class SimpleTradingEnv(gym.Env):
    """
    A minimal single-asset trading environment.

    Observation: [normalized_price, position, cash_ratio]
      - normalized_price: current price / initial_price (0~2 range typically)
      - position: 0 or 1 (flat or holding one share)
      - cash_ratio: remaining cash / initial_cash

    Actions: BUY(0), HOLD(1), SELL(2)
    Reward: realized PnL on sell + change in unrealized PnL
    """

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        initial_cash: float = 10000.0,
        n_steps: int = 100,
        price_start: float = 100.0,
        seed: int = 42,
    ):
        super().__init__()
        self.initial_cash = initial_cash
        self.n_steps = n_steps
        self.price_start = price_start

        # Action space: 0=BUY, 1=HOLD, 2=SELL
        self.action_space = spaces.Discrete(3)

        # Observation: [normalized_price, position, cash_ratio]
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            high=np.array([10.0, 1.0, 1.0], dtype=np.float32),
            dtype=np.float32,
        )

        self._rng = np.random.default_rng(seed)
        self.action_names = {0: "BUY", 1: "HOLD", 2: "SELL"}
        self._reset_state()

    def _reset_state(self):
        self.cash = self.initial_cash
        self.position = 0  # 0=flat, 1=holding
        self.shares = 0
        self.entry_price = 0.0
        self.current_step = 0

        # Generate random price series with geometric random walk
        returns = self._rng.normal(0.0001, 0.02, self.n_steps + 1)
        self.prices = self.price_start * np.cumprod(1 + returns)
        self.prices = np.clip(self.prices, 1.0, None)  # no zero/negative prices

        self.prev_unrealized_pnl = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)
        self._reset_state()
        return self._get_obs(), self._get_info()

    def _get_obs(self) -> np.ndarray:
        price = self.prices[self.current_step]
        normalized_price = price / self.price_start
        cash_ratio = self.cash / self.initial_cash
        return np.array(
            [normalized_price, float(self.position), cash_ratio], dtype=np.float32
        )

    def _get_info(self) -> dict:
        price = self.prices[self.current_step]
        portfolio_value = self.cash + self.shares * price
        unrealized_pnl = (price - self.entry_price) * self.shares if self.position else 0.0
        return {
            "step": self.current_step,
            "price": price,
            "cash": self.cash,
            "position": self.position,
            "portfolio_value": portfolio_value,
            "unrealized_pnl": unrealized_pnl,
        }

    def step(self, action: int):
        price = self.prices[self.current_step]
        # Execute action
        reward = 0.0
        if action == 0:  # BUY
            if self.position == 0 and self.cash >= price:
                self.shares = 1
                self.cash -= price
                self.position = 1
                self.entry_price = price
        elif action == 1:  # HOLD
            pass
        elif action == 2:  # SELL
            if self.position == 1:
                realized_pnl = price - self.entry_price
                reward += realized_pnl
                self.cash += price * self.shares
                self.shares = 0
                self.position = 0
                self.entry_price = 0.0

        self.current_step += 1
        terminated = self.current_step >= self.n_steps
        truncated = False

        # Add unrealized PnL change to reward
        new_price = self.prices[min(self.current_step, self.n_steps)]
        new_unrealized = (new_price - self.entry_price) * self.shares if self.position else 0.0
        reward += new_unrealized - self.prev_unrealized_pnl
        self.prev_unrealized_pnl = new_unrealized

        new_portfolio = self.cash + self.shares * new_price
        info = self._get_info()
        info["portfolio_value"] = new_portfolio
        info["reward"] = reward

        return self._get_obs(), reward, terminated, truncated, info


def run_random_agent():
    """Run one episode with a random action agent."""
    env = SimpleTradingEnv(n_steps=100, seed=42)

    print("=" * 60)
    print("Phase 1: Minimal Trading Environment — Random Agent")
    print("=" * 60)
    print(f"  Action space: {env.action_space} (0=BUY, 1=HOLD, 2=SELL)")
    print(f"  Observation space: {env.observation_space}")
    print(f"  Initial cash: ${env.initial_cash:,.2f}")
    print(f"  Steps per episode: {env.n_steps}")
    print()

    obs, info = env.reset()
    print(f"  Initial price: ${info['price']:.2f}")
    print(f"  Initial portfolio: ${info['portfolio_value']:,.2f}")
    print()
    print(f"  {'Step':>4}  {'Action':>6}  {'Price':>8}  {'Pos':>4}  {'Cash':>10}  {'PortVal':>10}  {'Reward':>8}")
    print("  " + "-" * 62)

    total_reward = 0.0
    step_count = 0
    rng = np.random.default_rng(123)

    while True:
        action = int(rng.integers(0, 3))
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        step_count += 1

        if action != 1 or step_count % 10 == 0 or terminated:
            print(
                f"  {info['step']:4d}  {env.action_names[action]:>6}  "
                f"${info['price']:7.2f}  {info['position']:4d}  "
                f"${info['cash']:9.2f}  ${info['portfolio_value']:9.2f}  "
                f"{reward:8.2f}"
            )

        if terminated:
            break

    initial_value = env.initial_cash
    final_value = info["portfolio_value"]
    pnl = final_value - initial_value

    print()
    print("  --- Episode Summary ---")
    print(f"  Total steps:        {step_count}")
    print(f"  Total reward:       {total_reward:.2f}")
    print(f"  Initial portfolio:  ${initial_value:,.2f}")
    print(f"  Final portfolio:    ${final_value:,.2f}")
    print(f"  PnL:               ${pnl:+,.2f} ({pnl / initial_value * 100:+.2f}%)")
    print()

    # Verify environment properties
    print("  --- Environment Verification ---")
    obs2, _ = env.reset()
    print(f"  Reset returns observation shape: {obs2.shape} (expected (3,))")
    print(f"  Observation dtype: {obs2.dtype} (expected float32)")
    print(f"  Observation bounds check: {np.all(obs2 >= 0)} (all non-negative)")

    # Run a quick second episode to verify reset works
    total_reward_2 = 0.0
    done = False
    while not done:
        _, r, terminated, truncated, _ = env.step(0)
        total_reward_2 += r
        done = terminated or truncated
    print(f"  Second episode (always BUY) total reward: {total_reward_2:.2f}")
    print("  Episode terminates correctly: True")

    env.close()
    print()
    print("=" * 60)
    print("  Environment validation complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_random_agent()
