import random
from dummy_env import DummyEnv
from agent import QLearningAgent

def train(num_episodes=5000):
    env = DummyEnv()
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=1.0)
    
    episode_rewards = []
    
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            possible_actions = env.get_possible_actions()
            action = agent.get_action(state, possible_actions)
            
            next_state, reward, done, text_log = env.step(action)
            
            next_possible_actions = env.get_possible_actions() if not done else []
            agent.learn(state, action, reward, next_state, next_possible_actions)
            
            state = next_state
            total_reward += reward
        
        # Epsilon decay after each episode
        agent.epsilon = max(0.01, agent.epsilon * 0.995)
        episode_rewards.append(total_reward)
        
        if (episode + 1) % 500 == 0:
            avg_reward = sum(episode_rewards[-500:]) / 500
            print(f"Episode {episode + 1}/{num_episodes} | Avg Reward (last 500): {avg_reward:.2f} | Epsilon: {agent.epsilon:.3f}")
    
    return agent, episode_rewards

if __name__ == "__main__":
    agent, rewards = train()