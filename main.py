import torch  # Не забудь импортировать torch
from game import Game2048
from model import QLearningAgent
import matplotlib.pyplot as plt
import pickle

env = Game2048()
agent = QLearningAgent(action_dim=4)
episodes = 30000
scores = []

for episode in range(episodes):
    state = env.reset()
    state = env.get_state()
    total_reward = 0
    done = False

    while not done:
        action = agent.act(state)
        next_state_raw, reward, done = env.move(action)
        next_state = env.get_state()
        agent.train(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

    agent.epsilon = max(0.01, agent.epsilon * 0.995)
    scores.append(total_reward)
    if episode % 100 == 0:
        print(f"Episode {episode}, score: {total_reward}")


with open("q_table.pkl", "wb") as f:
    print("✅ Q-table size:", len(agent.q_table))
    pickle.dump(agent.q_table, f)
    
    
import matplotlib.pyplot as plt

plt.plot(scores)
plt.xlabel("Episode")
plt.ylabel("Score")
plt.title("Training Progress")
plt.grid(True)
plt.tight_layout()
plt.savefig("training_progress.png")  
print("📊 Saved training graph as training_progress.png")


