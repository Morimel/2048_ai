import pygame
import sys
import numpy as np

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

FONT_COLOR = (119, 110, 101)
BG_COLOR = (187, 173, 160)
GRID_COLOR = (205, 193, 180)

def draw_board(screen, board, score):
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont("arial", 40, bold=True)
    score_font = pygame.font.SysFont("arial", 30)

    tile_size = 100
    tile_margin = 10
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            rect = pygame.Rect(j * (tile_size + tile_margin) + tile_margin,
                               i * (tile_size + tile_margin) + tile_margin,
                               tile_size, tile_size)
            pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), rect)
            if value != 0:
                text = font.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 420))
    pygame.display.flip()
