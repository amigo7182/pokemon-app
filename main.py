import random
from time import sleep
from environment import PokemonEnv
from agent import QLearningAgent
import sys

#The main training loop for agent
def train(num_episodes=10000):
    env = PokemonEnv()
    agent = QLearningAgent(alpha=0.1, gamma=0.9, epsilon=1.0)
    decay_rate = 0.9999
    
    episode_rewards = []
    
    #train for a specified number of episodes
    for episode in range(num_episodes):
        state = env.reset() #reset the board at the start of each episode
        done = False
        total_reward = 0
        
        #run until the game end
        while not done:
            possible_actions = env.get_possible_actions()
            action = agent.get_action(state, possible_actions) #let the agent decide the action
            
            next_state, reward, done, text_log = env.step(action) #carry out that action
            
            next_possible_actions = env.get_possible_actions() if not done else []
            agent.learn(state, action, reward, next_state, next_possible_actions) #let the agent learn from their action
            
            state = next_state
            total_reward += reward
        
        # Epsilon decay after each episode
        agent.epsilon = max(0.01, agent.epsilon * decay_rate)
        episode_rewards.append(total_reward)
        
        #visualize the average reward per 500 episodes of training 
        if (episode + 1) % 500 == 0:
            avg_reward = sum(episode_rewards[-500:]) / 500
            print(f"Episode {episode + 1}/{num_episodes} | Avg Reward (last 500): {avg_reward:.2f} | Epsilon: {agent.epsilon:.3f}")
    
    agent.save_q_table()

#The simulation of the agent playing the game
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

    #run until the game is complete
    while not done:
        #let the agent make the move
        possible_actions = env.get_possible_actions()
        action = agent.get_action(state, possible_actions)
        next_state, reward, done, log = env.step(action)
        
        #print out the game log
        for i in log:
            print(i)
            sleep(0.5) 

        state = next_state

def main():
    #start the model in train mode or simulation mode depending on the parameter
    if "train" in sys.argv:
        train()
    else:
        simulation()

if __name__ == "__main__":
    main()
