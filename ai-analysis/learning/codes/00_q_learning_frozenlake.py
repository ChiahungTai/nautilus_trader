"""
Phase 0: RL Basics — Q-Learning on FrozenLake-v1

Teaches:
  - Tabular Q-learning with epsilon-greedy exploration
  - Q-table update rule: Q(s,a) <- Q(s,a) + alpha * [r + gamma * max_a' Q(s',a') - Q(s,a)]
  - Epsilon decay for exploration-exploitation trade-off
  - Episode-based training loop with gymnasium

Dependencies: numpy, gymnasium (pip install gymnasium)
"""

import gymnasium as gym
import numpy as np


def train_q_learning(
    n_episodes: int = 200,
    alpha: float = 0.1,
    gamma: float = 0.99,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.01,
    epsilon_decay: float = 0.995,
):
    env = gym.make("FrozenLake-v1", is_slippery=False)
    n_states = env.observation_space.n
    n_actions = env.action_space.n
    q_table = np.zeros((n_states, n_actions))

    action_map = {0: "LEFT", 1: "DOWN", 2: "RIGHT", 3: "UP"}

    epsilon = epsilon_start
    rewards_history = []

    print("=" * 60)
    print("Phase 0: Q-Learning on FrozenLake-v1")
    print(f"  States: {n_states}, Actions: {n_actions}")
    print(f"  alpha={alpha}, gamma={gamma}")
    print(f"  epsilon: {epsilon_start} -> {epsilon_end} (decay={epsilon_decay})")
    print(f"  Episodes: {n_episodes}")
    print("=" * 60)

    for ep in range(n_episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False

        while not done:
            if np.random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = int(np.argmax(q_table[state]))

            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # Q-learning update: off-policy TD(0)
            best_next = np.max(q_table[next_state])
            td_target = reward + gamma * best_next * (1 - terminated)
            td_error = td_target - q_table[state, action]
            q_table[state, action] += alpha * td_error

            state = next_state
            total_reward += reward

        epsilon = max(epsilon_end, epsilon * epsilon_decay)
        rewards_history.append(total_reward)

        if (ep + 1) % 50 == 0:
            window = rewards_history[-50:]
            success_rate = np.mean(window) * 100
            print(
                f"  Episode {ep+1:4d} | "
                f"Success rate (last 50): {success_rate:5.1f}% | "
                f"epsilon: {epsilon:.3f}"
            )

    # Final evaluation
    print("\n--- Final Evaluation (100 episodes, greedy policy) ---")
    eval_rewards = []
    for _ in range(100):
        state, _ = env.reset()
        done = False
        ep_reward = 0
        while not done:
            action = int(np.argmax(q_table[state]))
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            ep_reward += reward
        eval_rewards.append(ep_reward)

    final_success_rate = np.mean(eval_rewards) * 100
    print(f"  Final success rate: {final_success_rate:.1f}%")

    # Print learned Q-table (compact view)
    print("\n--- Learned Q-Table (state -> [LEFT, DOWN, RIGHT, UP]) ---")
    for s in range(n_states):
        best_a = int(np.argmax(q_table[s]))
        bar = " ".join(f"{q_table[s, a]:6.3f}" for a in range(n_actions))
        print(f"  State {s:2d}: [{bar}]  best={action_map[best_a]}")

    # Print learned policy as grid
    print("\n--- Learned Policy Grid ---")
    grid_size = int(np.sqrt(n_states))
    symbols = {0: "<", 1: "v", 2: ">", 3: "^"}
    for row in range(grid_size):
        cells = []
        for col in range(grid_size):
            s = row * grid_size + col
            best_a = int(np.argmax(q_table[s]))
            val = np.max(q_table[s])
            if val == 0:
                cells.append(" . ")
            else:
                cells.append(f" {symbols[best_a]} ")
        print("  " + " ".join(cells))

    env.close()
    return q_table, final_success_rate


if __name__ == "__main__":
    q_table, success_rate = train_q_learning()
    print(f"\n{'=' * 60}")
    print(f"Training complete. Final success rate: {success_rate:.1f}%")
    print(f"{'=' * 60}")
