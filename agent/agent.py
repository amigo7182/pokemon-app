import numpy as np
import random
import pickle

class QLearningAgent:

    def __init__(self, alpha, gamma, epsilon):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_action(self, state, possible_actions):
        
        if random.random() < self.epsilon:
            return random.choice(possible_actions)
        
        q_values = {action: self.q_table.get((state, action), 0.0) for action in possible_actions}
        return max(q_values, key=lambda a: q_values[a])

    def learn(self, state, action, reward, next_state, next_possible_actions):

        if next_possible_actions:
            max_next_q = max(self.q_table.get((next_state, a), 0.0) for a in next_possible_actions)
        else:
            max_next_q = 0.0
        

        current_q = self.q_table.get((state, action), 0.0)
        
        
        self.q_table[(state, action)] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)

    def save_q_table(self):
        # Save the Q-table dict to a file
        with open('Q_table.pickle', 'wb') as handle:
            pickle.dump(self.q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load_q_table(self):
        with open('Q_table.pickle', 'rb') as f:
            self.q_table = pickle.load(f)
