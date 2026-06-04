import random
from time import sleep
from environment import PokemonEnv
from agent import QLearningAgent
import sys

def train(num_episodes=10000):
    env = PokemonEnv()
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=1.0)
    decay_rate = 0.995
    
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
        agent.epsilon = max(0.01, agent.epsilon * decay_rate)
        episode_rewards.append(total_reward)
        
        if (episode + 1) % 500 == 0:
            avg_reward = sum(episode_rewards[-500:]) / 500
            print(f"Episode {episode + 1}/{num_episodes} | Avg Reward (last 500): {avg_reward:.2f} | Epsilon: {agent.epsilon:.3f}")
    
    agent.save_q_table()

def simulation():
    env = PokemonEnv()
    state = env.reset()
    agent = QLearningAgent(alpha = 0.1, gamma = 0.9, epsilon = 0)
    agent.load_q_table()
    done = False; 

    print("Hi, I'm Brock! I'm Pewter's Gym Leader!\n"
    "I believe in rock hard defense and determination!\n"
    "That's why my Pokemon are all the rock-type!\n"
    "Do you still want to challenger me?\n"
    "Fine then! Show me your best!")

    while not done:
        possible_actions = env.get_possible_actions()
        action = agent.get_action(state, possible_actions)

        next_state, done, log = env.step(action)
        
        for i in log:
            print(i)
            sleep(0.5) 

        state = next_state

if __name__ == "__main__":
    if "train" in sys.argv:
        train()
    else:
        simulation()
