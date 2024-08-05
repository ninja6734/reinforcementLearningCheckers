import numpy as np
import random
from NeuralNetwork import NeuralNetwork

class Agent:
    def __init__(self, state_dim, hidden_dim, max_actions, pID, alpha=0.01, gamma=0.9, epsilon=0.1):
        self.state_dim = state_dim
        self.pID = pID
        self.gamma = gamma
        self.epsilon = epsilon
        self.model = NeuralNetwork(state_dim, hidden_dim, max_actions)
        self.alpha = alpha
    
    def load(self,model):
        self.model = model

    def getQValues(self, state):
        return self.model.forward(state)

    def choose_action(self, state, available_actions):
        if np.random.rand() < self.epsilon:
            return random.choice(available_actions)
        q_values = self.getQValues(state)
        q_values = q_values[0, range(len(available_actions))]
        index = np.argmax(q_values)
        return available_actions[index]

    def update(self, state, action, reward, next_state, available_actions, next_available_actions):
        q_values = self.getQValues(state)
        action_idx = available_actions.index(action)
        q_value = q_values[0, action_idx]
        
        if(next_state):
            next_q_values = self.getQValues(next_state)
            next_q_value = np.max(next_q_values[0, range(len(next_available_actions))])
            
            target = reward + self.gamma * next_q_value
        else:
            target = reward
        
        grad_output = np.zeros_like(q_values)
        grad_output[0, action_idx] = q_value - target
        
        self.model.backward(state, grad_output, self.alpha)
