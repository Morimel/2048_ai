import pygame
import time
import pickle
from game import Game2048
from visualizer import draw_board
from model import QLearningAgent
import imageio
from PIL import Image

# === Настройка окна ===
pygame.init()
screen = pygame.display.set_mode((420, 460))
pygame.display.set_caption("2048 Q-Learning Viewer")
clock = pygame.time.Clock()

# === Игра и агент ===
env = Game2048()
agent = QLearningAgent(action_dim=4)

# === Загрузка обученной Q-таблицы ===
with open("q_table.pkl", "rb") as f:
    agent.q_table = pickle.load(f)

agent.epsilon = 0.0  # ✅ Агент будет использовать только лучшие ходы

# === Начало игры ===
state = env.reset()
state = env.get_state()
done = False

max_steps = 1000
steps = 0

frames = []

while not done and steps < max_steps:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    draw_board(screen, env.board, env.score)
    
    pygame.image.save(screen, "frame.png")
    frame = Image.open("frame.png")
    frames.append(frame.copy())
    frame.close()
    
    print(f"State: {state}")
    print(f"Known Qs: {[agent.get_q(state, a) for a in range(4)]}")
    
    action = agent.act(state)
    next_state, reward, done = env.move(action)
    state = next_state
    time.sleep(0.25)
    clock.tick(60)
    steps += 1

# Показ финального состояния
draw_board(screen, env.board, env.score)
time.sleep(2)

frames[0].save("game_play.gif", format="GIF", save_all=True, append_images=frames[1:], duration=250, loop=0)
print("🎞 Saved gameplay as game_play.gif")