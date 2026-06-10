"""
Phase 2a: DQN from Scratch on CartPole-v1

Teaches:
  - Deep Q-Network (DQN) implementation with PyTorch
  - Experience replay buffer for breaking correlation
  - Target network for training stability
  - Epsilon-greedy exploration with decay
  - Q-learning update rule with neural network:
    loss = MSE(Q(s,a), r + gamma * Q_target(s', argmax_a Q(s',a)))
  - Soft update of target network: theta_target = tau * theta + (1-tau) * theta_target

Dependencies: numpy, torch, gymnasium
"""

from __future__ import annotations

import random
from collections import deque

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class QNetwork(nn.Module):
    """Simple MLP Q-network: state -> Q-values for each action."""

    def __init__(self, state_dim: int, action_dim: int, hidden: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ReplayBuffer:
    """Simple list-based experience replay buffer."""

    def __init__(self, capacity: int = 10000):
        self.buffer: deque = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)


def train_dqn(
    n_episodes: int = 500,
    batch_size: int = 64,
    gamma: float = 0.99,
    lr: float = 1e-3,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.05,
    epsilon_decay: int = 300,
    tau: float = 0.005,
    buffer_capacity: int = 10000,
    learn_start: int = 500,
    seed: int = 42,
):
    """
    Train DQN on CartPole-v1.

    Key hyperparameters and their roles:
      - gamma: discount factor (how much we value future rewards)
      - tau: soft update rate for target network (0 = never update, 1 = hard copy)
      - epsilon_decay: controls how fast exploration decreases (higher = slower decay)
      - learn_start: minimum buffer size before training starts
    """
    # Set seeds for reproducibility
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    env = gym.make("CartPole-v1")
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    q_net = QNetwork(state_dim, action_dim)
    target_net = QNetwork(state_dim, action_dim)
    target_net.load_state_dict(q_net.state_dict())

    optimizer = optim.Adam(q_net.parameters(), lr=lr)
    buffer = ReplayBuffer(buffer_capacity)

    # Epsilon schedule: exponential decay
    # epsilon = epsilon_end + (epsilon_start - epsilon_end) * exp(-step / epsilon_decay)
    def get_epsilon(step: int) -> float:
        return epsilon_end + (epsilon_start - epsilon_end) * np.exp(-step / epsilon_decay)

    print("=" * 60)
    print("Phase 2a: DQN from Scratch on CartPole-v1")
    print("=" * 60)
    print(f"  State dim: {state_dim}, Action dim: {action_dim}")
    print(f"  Q-Network: MLP ({state_dim} -> 128 -> 128 -> {action_dim})")
    print(f"  Gamma: {gamma}, LR: {lr}, Tau: {tau}")
    print(f"  Epsilon: {epsilon_start} -> {epsilon_end} (decay rate: {epsilon_decay})")
    print(f"  Buffer: {buffer_capacity}, Batch: {batch_size}")
    print(f"  Episodes: {n_episodes}")
    print("=" * 60)
    print()

    total_steps = 0
    rewards_history = []
    best_avg_reward = 0.0

    for ep in range(n_episodes):
        state, _ = env.reset(seed=seed + ep)
        episode_reward = 0.0
        done = False

        while not done:
            epsilon = get_epsilon(total_steps)

            # Epsilon-greedy action selection
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    state_t = torch.FloatTensor(state).unsqueeze(0)
                    q_values = q_net(state_t)
                    action = q_values.argmax(dim=1).item()

            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            buffer.push(state, action, reward, next_state, float(terminated))
            state = next_state
            episode_reward += reward
            total_steps += 1

            # Learn from replay buffer
            if len(buffer) >= learn_start:
                s_batch, a_batch, r_batch, ns_batch, d_batch = buffer.sample(batch_size)

                s_t = torch.FloatTensor(s_batch)
                a_t = torch.LongTensor(a_batch).unsqueeze(1)
                r_t = torch.FloatTensor(r_batch)
                ns_t = torch.FloatTensor(ns_batch)
                d_t = torch.FloatTensor(d_batch)

                # Current Q values: Q(s, a)
                q_values = q_net(s_t).gather(1, a_t).squeeze(1)

                # Target Q values: r + gamma * max_a' Q_target(s', a')
                with torch.no_grad():
                    next_q_max = target_net(ns_t).max(dim=1)[0]
                    td_targets = r_t + gamma * next_q_max * (1 - d_t)

                # MSE loss between predicted Q and target
                loss = nn.functional.mse_loss(q_values, td_targets)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # Soft update target network
                # theta_target = tau * theta + (1 - tau) * theta_target
                for target_param, param in zip(target_net.parameters(), q_net.parameters()):
                    target_param.data.copy_(
                        tau * param.data + (1 - tau) * target_param.data
                    )

        rewards_history.append(episode_reward)

        if (ep + 1) % 50 == 0:
            avg_reward = np.mean(rewards_history[-50:])
            eps_now = get_epsilon(total_steps)
            print(
                f"  Episode {ep+1:4d} | "
                f"Avg Reward (50): {avg_reward:6.1f} | "
                f"Epsilon: {eps_now:.3f} | "
                f"Steps: {total_steps}"
            )
            if avg_reward > best_avg_reward:
                best_avg_reward = avg_reward

    # Final evaluation
    print()
    print("--- Final Evaluation (20 episodes, greedy policy) ---")
    eval_rewards = []
    for i in range(20):
        state, _ = env.reset(seed=9999 + i)
        done = False
        ep_reward = 0.0
        while not done:
            with torch.no_grad():
                state_t = torch.FloatTensor(state).unsqueeze(0)
                action = q_net(state_t).argmax(dim=1).item()
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            ep_reward += reward
        eval_rewards.append(ep_reward)

    avg_eval = np.mean(eval_rewards)
    std_eval = np.std(eval_rewards)
    print(f"  Evaluation: {avg_eval:.1f} +/- {std_eval:.1f} (over 20 episodes)")
    print(f"  Best training avg reward (50-ep window): {best_avg_reward:.1f}")
    print(f"  Total training steps: {total_steps}")

    # Print learned Q-values for a sample state
    print()
    print("--- Sample Q-Values (cart at center, pole upright) ---")
    sample_state = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float32)
    with torch.no_grad():
        q_vals = q_net(torch.FloatTensor(sample_state).unsqueeze(1).T).numpy()[0]
    print(f"  State: {sample_state}")
    print(f"  Q(push left)  = {q_vals[0]:.3f}")
    print(f"  Q(push right) = {q_vals[1]:.3f}")
    print(f"  Best action: {'RIGHT' if q_vals[1] > q_vals[0] else 'LEFT'}")

    env.close()

    print()
    print("=" * 60)
    print("  DQN Training Complete!")
    print("=" * 60)
    return q_net


if __name__ == "__main__":
    train_dqn()
