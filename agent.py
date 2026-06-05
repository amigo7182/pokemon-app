import numpy as np
import random
import pickle

#The main agent used to play the pokemon game
class QLearningAgent:

    def __init__(self, alpha, gamma, epsilon):
        self.q_table = {} #The Q-table agent is using to try and find the best possible move
        self.alpha = alpha #The learning rate: how fast the Q-table changes
        self.gamma = gamma #How much the agent value future reward compare to present reward
        self.epsilon = epsilon #How likely the agent will make a random move (how much it will explore)

    #Use to decide what action the agent is taking
    def get_action(self, state, possible_actions):
        #The agent may choose to do random action based on epsilon
        if random.random() < self.epsilon:
            return random.choice(possible_actions)
        
        #return the action with the highest Q-value
        q_values = {action: self.q_table.get((state, action), 0.0) for action in possible_actions}
        return max(q_values, key=lambda a: q_values[a])

    #Train the model using Bellman equation
    def learn(self, state, action, reward, next_state, next_possible_actions):
        #finding the reward for being in future state
        if next_possible_actions:
            max_next_q = max(self.q_table.get((next_state, a), 0.0) for a in next_possible_actions)
        else:
            max_next_q = 0.0
        
        #finding reward for being in current state and taking a specific action
        current_q = self.q_table.get((state, action), 0.0)
        
        #update the Q-table
        self.q_table[(state, action)] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

    #Save the trained Q-table dict to a file
    def save_q_table(self):
        with open('Q_table.pickle', 'wb') as handle:
            pickle.dump(self.q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    #Retrieved the Q-table from a file and load it into the model
    def load_q_table(self):
        with open('Q_table.pickle', 'rb') as f:
            self.q_table = pickle.load(f)
