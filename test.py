import gymnasium as gym
from agent import QLearningAgent
import numpy as np

env = gym.make("FrozenLake-v1", is_slippery=True)

n_episodes = 2000

agent = QLearningAgent(n_states=16, n_actions=4)
rewards_per_episode = []

for episode in range(n_episodes):
    state, _ = env.reset()
    total_reward = 0
    done = False
    while not done:
        action = agent.choose_action(state)
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
    agent.decay_epsilon()
    rewards_per_episode.append(total_reward)

    if (episode + 1) % 100 == 0:
        recent_avg = np.mean(rewards_per_episode[-100:])
        print(f"Episode {episode + 1}: avg reward (last 100) = {recent_avg:.3f}, epsilon = {agent.epsilon:.3f}")