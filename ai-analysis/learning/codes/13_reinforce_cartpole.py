"""
Phase 3: REINFORCE Policy Gradient on CartPole-v1
===================================================
Teaches the fundamental policy gradient method (REINFORCE) from scratch.

Key concepts:
1. PolicyNetwork: MLP that maps observations -> action probabilities (softmax)
2. REINFORCE algorithm: Monte Carlo policy gradient
3. Advantage = reward - baseline (mean of episode rewards)
4. Policy gradient loss = -sum(log_prob * advantage)
5. Training on CartPole-v1 (gymnasium) for 500 episodes

REINFORCE Formula (in comments):
    J(theta) = E[sum_t R_t * log pi(a_t | s_t; theta)]
    grad J(theta) ~= sum_t (R_t - b) * grad log pi(a_t | s_t; theta)
    where b = baseline (mean reward) reduces variance

Comparison with DQN (in comments):
    DQN: value-based, off-policy, experience replay, epsilon-greedy
    REINFORCE: policy-based, on-policy, full episodes, direct optimization
"""

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical


# ============================================================================
# 1. Policy Network
# ============================================================================

class PolicyNetwork(nn.Module):
    """
    Policy network: maps observation -> action probabilities.

    Architecture:
        Input: observation (4 dims for CartPole)
        Hidden 1: 128 units + ReLU
        Hidden 2: 128 units + ReLU
        Output: action logits (2 for CartPole) -> softmax -> probabilities

    This is a STOCHASTIC policy: outputs a distribution over actions.
    We SAMPLE from this distribution during training (exploration).
    """

    def __init__(self, obs_dim: int = 4, act_dim: int = 2, hidden: int = 128):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, hidden)
        self.fc2 = nn.Linear(hidden, hidden)
        self.fc3 = nn.Linear(hidden, act_dim)

    def forward(self, x: torch.Tensor) -> Categorical:
        """
        Args:
            x: (batch, obs_dim) observations
        Returns:
            Categorical distribution over actions
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        logits = self.fc3(x)
        return Categorical(logits=logits)

    def get_action(self, obs: np.ndarray) -> tuple:
        """
        Sample an action from the policy.

        Returns:
            action: int, the sampled action
            log_prob: float, log probability of the action (for gradient)
        """
        obs_t = torch.FloatTensor(obs).unsqueeze(0)  # (1, obs_dim)
        dist = self.forward(obs_t)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        return action.item(), log_prob


# ============================================================================
# 2. REINFORCE Agent
# ============================================================================

class REINFORCEAgent:
    """
    REINFORCE (Monte Carlo Policy Gradient) agent.

    Algorithm:
        For each episode:
            1. Collect full trajectory: (s_0, a_0, r_0), (s_1, a_1, r_1), ...
            2. Compute returns: G_t = sum_{k=t}^{T} gamma^k * r_k
            3. Compute advantage: A_t = G_t - mean(G)  (baseline reduces variance)
            4. Loss = -sum_t A_t * log pi(a_t | s_t)
            5. Backprop and update

    REINFORCE Formula:
        J(theta) = E_pi [ sum_{t=0}^{T} gamma^t * r_t ]
        grad J(theta) ~= (1/N) sum_i sum_t (G_t^i - b) * grad log pi(a_t^i | s_t^i; theta)

    Key properties:
        - ON-POLICY: must collect fresh data each update
        - MONTE CARLO: uses full episode returns (no bootstrapping)
        - HIGH VARIANCE: baseline (mean reward) helps reduce variance

    Comparison with DQN:
    +-----------+-------------------+-------------------+
    | Aspect    | REINFORCE         | DQN               |
    +-----------+-------------------+-------------------+
    | Type      | Policy-based      | Value-based       |
    | Policy    | Stochastic        | Epsilon-greedy    |
    | Updates   | On-policy         | Off-policy        |
    | Data      | Full episodes     | Experience replay |
    | Variance  | High              | Lower             |
    | Continuous| Yes (natural)     | No (discrete only)|
    | Function  | Directly optimizes| Learns Q(s,a)     |
    |           | policy pi(a|s)    | then derives pi   |
    +-----------+-------------------+-------------------+
    """

    def __init__(self, obs_dim: int = 4, act_dim: int = 2,
                 lr: float = 1e-3, gamma: float = 0.99):
        self.policy = PolicyNetwork(obs_dim, act_dim)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma

        # Episode buffers
        self.log_probs: list = []
        self.rewards: list = []

    def select_action(self, obs: np.ndarray) -> int:
        """Select action by sampling from policy."""
        action, log_prob = self.policy.get_action(obs)
        self.log_probs.append(log_prob)
        return action

    def store_reward(self, reward: float):
        """Store reward from environment."""
        self.rewards.append(reward)

    def update(self) -> dict:
        """
        Update policy using REINFORCE with baseline.

        Steps:
            1. Compute discounted returns G_t
            2. Normalize (advantage = returns - mean)
            3. Compute policy gradient loss
            4. Backprop

        Returns:
            dict with loss, mean_return, episode_reward
        """
        if not self.rewards:
            return {"loss": 0.0, "mean_return": 0.0, "episode_reward": 0.0}

        # Step 1: Compute discounted returns
        returns = []
        G = 0.0
        for r in reversed(self.rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns, dtype=torch.float32)
        episode_reward = sum(self.rewards)

        # Step 2: Advantage = returns - baseline (mean)
        # Baseline reduces variance without introducing bias
        advantage = returns - returns.mean()

        # Step 3: Policy gradient loss
        # L = -sum_t A_t * log pi(a_t | s_t)
        # Negative because we MAXIMIZE expected return (gradient ascent)
        log_probs_tensor = torch.cat(self.log_probs)
        loss = -(log_probs_tensor * advantage).sum()

        # Step 4: Backprop
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy.parameters(), 1.0)
        self.optimizer.step()

        # Clear buffers
        result = {
            "loss": loss.item(),
            "mean_return": returns.mean().item(),
            "episode_reward": episode_reward,
        }
        self.log_probs = []
        self.rewards = []

        return result


# ============================================================================
# 3. Training Loop
# ============================================================================

def train_reinforce(
    n_episodes: int = 500,
    print_every: int = 50,
    gamma: float = 0.99,
    lr: float = 1e-3,
    seed: int = 42,
):
    """
    Train REINFORCE agent on CartPole-v1.

    CartPole-v1:
        State: [cart_position, cart_velocity, pole_angle, pole_angular_velocity]
        Actions: 0 (push left), 1 (push right)
        Reward: +1 per step, max 500 steps
        Solved: average reward >= 475 over 100 consecutive episodes
    """
    # Set seeds for reproducibility
    torch.manual_seed(seed)
    np.random.seed(seed)

    env = gym.make("CartPole-v1")
    env.reset(seed=seed)

    obs_dim = env.observation_space.shape[0]  # 4
    act_dim = env.action_space.n  # 2

    agent = REINFORCEAgent(obs_dim, act_dim, lr=lr, gamma=gamma)

    # Tracking
    episode_rewards = []
    running_avg = []

    print("--- REINFORCE Training on CartPole-v1 ---")
    print(f"  Episodes:     {n_episodes}")
    print(f"  Gamma:        {gamma}")
    print(f"  Learning rate:{lr}")
    print(f"  Observation:  {obs_dim} dims")
    print(f"  Actions:      {act_dim} (left/right)")
    print()

    for episode in range(1, n_episodes + 1):
        obs, _ = env.reset()
        done = False
        truncated = False

        while not (done or truncated):
            action = agent.select_action(obs)
            obs, reward, done, truncated, _ = env.step(action)
            agent.store_reward(reward)

        # Update after full episode
        result = agent.update()
        ep_reward = result["episode_reward"]
        episode_rewards.append(ep_reward)

        # Running average (last 100 episodes)
        window = min(100, len(episode_rewards))
        avg = np.mean(episode_rewards[-window:])
        running_avg.append(avg)

        if episode % print_every == 0:
            print(f"  Episode {episode:>4d}/{n_episodes}: "
                  f"reward={ep_reward:>6.1f}  "
                  f"avg(100)={avg:>6.1f}  "
                  f"loss={result['loss']:>8.2f}")

    env.close()

    return episode_rewards, running_avg


# ============================================================================
# 4. Evaluation
# ============================================================================

def evaluate_agent(n_episodes: int = 10, seed: int = 123):
    """Evaluate a freshly trained agent (deterministic, no exploration)."""
    torch.manual_seed(seed)
    np.random.seed(seed)

    env = gym.make("CartPole-v1")
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.n

    # Train a quick agent
    agent = REINFORCEAgent(obs_dim, act_dim, lr=1e-3, gamma=0.99)

    # Quick training
    for ep in range(300):
        obs, _ = env.reset(seed=seed + ep)
        done = False
        truncated = False
        while not (done or truncated):
            action = agent.select_action(obs)
            obs, reward, done, truncated, _ = env.step(action)
            agent.store_reward(reward)
        agent.update()

    # Evaluate (take argmax, no sampling)
    rewards = []
    for ep in range(n_episodes):
        obs, _ = env.reset(seed=999 + ep)
        total_reward = 0
        done = False
        truncated = False
        while not (done or truncated):
            obs_t = torch.FloatTensor(obs).unsqueeze(0)
            with torch.no_grad():
                dist = agent.policy(obs_t)
                action = dist.probs.argmax().item()  # Greedy
            obs, reward, done, truncated, _ = env.step(action)
            total_reward += reward
        rewards.append(total_reward)

    env.close()
    return rewards


# ============================================================================
# 5. Main
# ============================================================================

def main():
    print("=" * 70)
    print("Phase 3: REINFORCE Policy Gradient on CartPole-v1")
    print("=" * 70)

    print("\n--- REINFORCE Algorithm Overview ---")
    print("""
  REINFORCE (Monte Carlo Policy Gradient):

    1. Initialize policy pi(a|s; theta) with random weights
    2. For each episode:
       a. Collect trajectory: (s_0, a_0, r_0), ..., (s_T, a_T, r_T)
       b. Compute returns: G_t = sum_{k=t}^{T} gamma^k * r_k
       c. Compute advantage: A_t = G_t - mean(G)   [baseline reduces variance]
       d. Update: theta <- theta + alpha * sum_t A_t * grad log pi(a_t|s_t; theta)

  Loss function (negated for gradient descent):
    L(theta) = -sum_t (G_t - baseline) * log pi(a_t | s_t; theta)
    """)

    # Train
    print("=" * 70)
    episode_rewards, running_avg = train_reinforce(
        n_episodes=500,
        print_every=50,
        gamma=0.99,
        lr=1e-3,
        seed=42,
    )

    # Results summary
    print("\n--- Training Results ---")
    print(f"  Final episode reward:     {episode_rewards[-1]:.1f}")
    print(f"  Final running avg (100):  {running_avg[-1]:.1f}")
    print(f"  Best episode reward:      {max(episode_rewards):.1f}")
    print(f"  Overall mean reward:      {np.mean(episode_rewards):.1f}")
    print(f"  Last 100 mean reward:     {np.mean(episode_rewards[-100:]):.1f}")

    # Learning curve summary (text-based)
    print("\n--- Learning Curve (text) ---")
    for ep_idx in [0, 49, 99, 199, 299, 399, 499]:
        if ep_idx < len(episode_rewards):
            bar_len = min(int(running_avg[ep_idx] / 10), 50)
            bar = "#" * bar_len
            print(f"  Ep {ep_idx + 1:>3d}: avg={running_avg[ep_idx]:>6.1f} |{bar}")

    # Verification
    print("\n--- Verification ---")

    # 1. Running average improved
    early_avg = np.mean(running_avg[:50])
    late_avg = np.mean(running_avg[-50:])
    improved = late_avg > early_avg
    print(f"  Running avg improved: {early_avg:.1f} -> {late_avg:.1f} "
          f"({'PASS' if improved else 'FAIL'})")

    # 2. Agent learned something (avg > random baseline ~20 for CartPole)
    random_baseline = 20.0  # Random policy typically gets ~10-25
    learned = running_avg[-1] > random_baseline
    print(f"  Better than random: {running_avg[-1]:.1f} > {random_baseline:.1f} "
          f"({'PASS' if learned else 'FAIL'})")

    # 3. Best episode was good
    best = max(episode_rewards)
    print(f"  Best episode: {best:.1f}/500.0 "
          f"({'PASS' if best > 100 else 'FAIL'})")

    # Comparison with DQN
    print("\n--- REINFORCE vs DQN Comparison ---")
    print("""
  +---------------------+-------------------------+-------------------------+
  | Aspect              | REINFORCE               | DQN                     |
  +---------------------+-------------------------+-------------------------+
  | Method              | Policy gradient          | Value-based             |
  | Policy output       | pi(a|s) probabilities    | Q(s,a) values           |
  | Exploration         | Inherent (stochastic)    | Epsilon-greedy          |
  | Data usage          | On-policy (fresh only)   | Off-policy (replay buf) |
  | Variance            | High (Monte Carlo)       | Lower (bootstrapping)   |
  | Sample efficiency   | Lower                    | Higher                  |
  | Continuous action   | Natural extension        | Not applicable          |
  | Convergence         | To local optimum         | Can be unstable         |
  | Implementation      | Simple                   | Complex (target net)    |
  +---------------------+-------------------------+-------------------------+

  REINFORCE is the FOUNDATION of policy gradient methods.
  Modern algorithms (PPO, SAC, TD3) build on these principles:
    PPO = clipped REINFORCE + advantage estimation (GAE)
    A2C/A3C = REINFORCE + learned baseline (value function)
    SAC = REINFORCE + entropy regularization + off-policy
    """)

    print("=" * 70)
    print("Key Takeaways:")
    print("  1. REINFORCE: collect full episodes, then update policy")
    print("  2. Advantage = return - baseline reduces variance")
    print("  3. Loss = -sum(log_prob * advantage) -> gradient ascent on return")
    print("  4. On-policy: must collect fresh data each update")
    print("  5. Foundation for modern RL: PPO, SAC, A2C all extend REINFORCE")
    print("  6. For Mamba+RL: same principles, Mamba replaces the policy network")
    print("=" * 70)


if __name__ == "__main__":
    main()
