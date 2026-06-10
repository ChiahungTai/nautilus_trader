"""
Phase 2b: SAC with Stable-Baselines3 on Pendulum-v1

Teaches:
  - Using Stable-Baselines3 (SB3) for production-grade RL
  - Soft Actor-Critic (SAC): off-policy algorithm for continuous action spaces
  - Why SAC fits continuous control:
      * DQN requires discretizing actions, infeasible for high-dim continuous spaces
      * SAC learns a stochastic policy pi(a|s) with reparameterization trick
      * Actor (policy) outputs mean+log_std for a Gaussian distribution
      * Critic (Q-function) uses twin Q-networks to reduce overestimation
      * Entropy regularization encourages exploration (alpha auto-tuned)
  - SB3 training loop abstraction: model.learn(total_timesteps)
  - Evaluation with deterministic policy

Dependencies: stable-baselines3, gymnasium, numpy
"""

from __future__ import annotations

import gymnasium as gym
import numpy as np
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import BaseCallback


class ProgressCallback(BaseCallback):
    """Custom callback to print training progress."""

    def __init__(self, print_every: int = 1000, verbose: int = 0):
        super().__init__(verbose)
        self.print_every = print_every
        self.episode_rewards = []
        self.current_ep_reward = 0.0

    def _on_step(self) -> bool:
        self.current_ep_reward += self.locals["rewards"][0]

        if self.locals["dones"][0]:
            self.episode_rewards.append(self.current_ep_reward)
            self.current_ep_reward = 0.0

        if self.num_timesteps % self.print_every == 0 and self.num_timesteps > 0:
            recent = self.episode_rewards[-20:] if len(self.episode_rewards) >= 20 else self.episode_rewards
            if recent:
                avg_r = np.mean(recent)
                print(
                    f"  Timesteps: {self.num_timesteps:6d} | "
                    f"Episodes: {len(self.episode_rewards):4d} | "
                    f"Avg Reward (last 20): {avg_r:8.1f}"
                )
        return True


def train_sac():
    env = gym.make("Pendulum-v1")

    print("=" * 60)
    print("Phase 2b: SAC (Stable-Baselines3) on Pendulum-v1")
    print("=" * 60)
    print()
    print("  Why SAC for continuous action spaces?")
    print("  - Pendulum action: torque in [-2.0, 2.0] (continuous)")
    print("  - DQN cannot handle continuous actions without discretization")
    print("  - SAC learns a Gaussian policy: pi(a|s) = N(mu(s), sigma(s))")
    print("  - Twin Q-networks reduce value overestimation")
    print("  - Automatic entropy tuning balances exploration/exploitation")
    print()
    print(f"  Observation space: {env.observation_space.shape} (cos(theta), sin(theta), angular_vel)")
    print(f"  Action space: {env.action_space.shape} (torque in [{env.action_space.low[0]:.1f}, {env.action_space.high[0]:.1f}])")
    print()

    # Create SAC agent
    # Key SB3 SAC hyperparameters:
    #   - learning_rate: 3e-4 (standard for SAC)
    #   - buffer_size: 50000 (replay buffer, enough for Pendulum)
    #   - batch_size: 256 (larger batch helps stability)
    #   - tau: 0.005 (soft update coefficient, same as DQN)
    #   - ent_coef: "auto" (automatic entropy tuning)
    model = SAC(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        buffer_size=50000,
        batch_size=256,
        tau=0.005,
        ent_coef="auto",
        verbose=0,
        seed=42,
    )

    print("--- Training (5000 timesteps) ---")
    print()
    callback = ProgressCallback(print_every=1000)
    model.learn(total_timesteps=5000, callback=callback, progress_bar=False)

    print()
    print("--- Evaluation (3 episodes, deterministic policy) ---")
    eval_rewards = []
    for ep in range(3):
        obs, _ = env.reset(seed=100 + ep)
        done = False
        ep_reward = 0.0
        steps = 0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            ep_reward += reward
            steps += 1
        eval_rewards.append(ep_reward)
        print(
            f"  Episode {ep+1}: Reward = {ep_reward:8.2f} "
            f"(steps: {steps})"
        )

    avg_eval = np.mean(eval_rewards)
    std_eval = np.std(eval_rewards)
    print()
    print(f"  Average Evaluation Reward: {avg_eval:.2f} +/- {std_eval:.2f}")
    print()
    print("  Note: Pendulum-v1 reward range is approx [-1600, 0].")
    print("  Rewards above -200 indicate the agent is learning to balance.")
    print("  With only 5000 steps, the agent shows initial learning.")
    print("  Production training typically uses 50000-200000 steps.")

    # Print policy network info
    print()
    print("--- SAC Policy Architecture ---")
    print("  Actor (policy) network layers:")
    actor = model.policy.actor
    for name, param in actor.named_parameters():
        if param.requires_grad:
            print(f"    {name}: {param.shape}")
    print("  Critic (Q-function, twin networks):")
    critic = model.policy.critic
    for name, param in critic.named_parameters():
        if param.requires_grad:
            print(f"    {name}: {param.shape}")

    # Show a sample action
    obs, _ = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    print()
    print("--- Sample Action ---")
    print(f"  Observation: {obs}")
    print(f"  Action (torque): {action[0]:.4f}")

    env.close()

    print()
    print("=" * 60)
    print("  SAC Training Complete!")
    print("=" * 60)
    return model


if __name__ == "__main__":
    train_sac()
