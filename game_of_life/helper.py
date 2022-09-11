import math
from .constants import COLS, ROWS, BLACK
import pygame

pygame.font.init()
font = pygame.font.SysFont(None, 30)

def convert_onehot_encode(coordinates):
    size = int(math.sqrt(len(coordinates)))
    if size ** 2 != len(coordinates):
        raise Exception('Number of coordinates should be perfect square')
    living_cells = []
    x_0 = (COLS - size) // 2
    y_0 = (ROWS - size) // 2
    for i in range(len(coordinates)):
        if coordinates[i] == 1:
            x, y = i % size, i // size
            living_cells.append(x_0 + x + (y_0 + y) * COLS)
    return living_cells

def print_msg(msg, win, x, y):
    # helper function to print message on the screen
    text = font.render(msg, True, BLACK)
    win.blit(text, (x, y))