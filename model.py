import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

class QLearningAgent:
    def __init__(self, action_dim, alpha=0.1, gamma=0.99, epsilon=1.0):
        self.q_table = {}  # (state, action) -> value
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.action_dim = action_dim

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        qs = [self.get_q(state, a) for a in range(self.action_dim)]
        if all(q == 0 for q in qs):  # 🔥 новое поведение
            return random.randint(0, self.action_dim - 1)
        return int(np.argmax(qs))


    def train(self, state, action, reward, next_state, done):
        best_next = max([self.get_q(next_state, a) for a in range(self.action_dim)])
        target = reward + self.gamma * best_next * (1 - int(done))
        old_value = self.get_q(state, action)
        self.q_table[(state, action)] = old_value + self.alpha * (target - old_value)

