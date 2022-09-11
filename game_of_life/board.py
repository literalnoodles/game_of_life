import pygame
import numpy as np
from .constants import BORDER_WIDTH, COLS, DELTA, SQUARE_SIZE, WHITE, BLACK, ROWS

CELL_ALIVE = 1
CELL_DEAD = 0

class Board:
    def __init__(self, win):
        self.cells = np.zeros((ROWS, COLS))
        self.win = win

    def print_result(self, best_of_gen):
        """
            print best of genereration result to the screen
        """
        cells = zip(*np.where(best_of_gen == CELL_ALIVE))
        for x, y in cells:
            self.fill_x_y(x + 1, y + 5)

    def set_seed(self, input):
        self.cells = np.zeros((ROWS, COLS))
        y_size, x_size = input.shape
        x_0 = (ROWS - x_size) // 2
        x_1 = x_0 + x_size
        y_0 = (COLS - y_size) // 2
        y_1 = y_0 + y_size
        self.cells[x_0: x_1, y_0: y_1] = input

    def draw_board(self):
        self.win.fill(WHITE)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.win, BLACK, (
                    row * SQUARE_SIZE, col *SQUARE_SIZE,
                    SQUARE_SIZE, SQUARE_SIZE
                ), width=BORDER_WIDTH)
        alive_cells = zip(*np.where(self.cells == CELL_ALIVE))     
        for x, y in alive_cells:
            self.fill_x_y(x, y)

    def fill_x_y(self, x, y):
        pygame.draw.rect(self.win, BLACK, (
            y * SQUARE_SIZE + BORDER_WIDTH,
            x * SQUARE_SIZE + BORDER_WIDTH,
            SQUARE_SIZE - 2 * BORDER_WIDTH,
            SQUARE_SIZE - 2 * BORDER_WIDTH
        ))
    
    def get_num(self, x, y):
        """
        It takes the x and y coordinates of a cell and returns the number of the cell
        :param x: the row number of the cell
        :param y: the row number
        :return: The number of the cell.
        """
        return x + y * COLS

    def is_inside(self, x, y):
        return 0 <= x  < ROWS and 0 <= y < COLS

    def get_neighbors(self, x, y):
        return np.array(
            [[-1, -1],
             [ 0, -1],
             [+1, -1],
             [-1,  0],
             [+1,  0],
             [-1, +1],
             [ 0, +1],
             [+1, +1]]
        ) + (x, y)
    
    def get_neighbors_alive(self, x, y):
        neighbors = self.get_neighbors(x, y)
        alives = []
        for m, n in neighbors:
            if self.is_inside(m,n) and self.cells[m, n] == CELL_ALIVE:
                alives.append((m,n))
        return alives

    def get_cell_new_status(self, x, y):
        cell_status = self.cells[x, y]
        # check number of neighbor is alive
        neighbors_alive = self.get_neighbors_alive(x, y)
        if cell_status == CELL_ALIVE:
            if (len(neighbors_alive) < 2):
                return CELL_DEAD
            if (len(neighbors_alive) > 3):
                return CELL_DEAD
            return CELL_ALIVE
        if cell_status == CELL_DEAD:
            if (len(neighbors_alive) == 3):
                return CELL_ALIVE
            return CELL_DEAD

    def update_board(self):
        # for storing new living cells
        updates = []
        # for storing checked cell number
        checked = []
        # only check living cells and its neighbors
        for cell in zip(*np.where(self.cells == CELL_ALIVE)):
            cell_x, cell_y = cell
            neighbors = self.get_neighbors(cell_x, cell_y)
            for x, y in np.concatenate((np.array(cell).reshape(1, -1), neighbors)):
                num = self.get_num(x, y)
                if num in checked or not self.is_inside(x, y):
                    continue
                current_status = self.cells[x, y]
                new_status = self.get_cell_new_status(x, y)
                if current_status != new_status:
                    updates.append((x, y))
                checked.append(num)
        for x, y in updates:
            # toggle
            self.cells[x, y] = 1 - self.cells[x, y]
        return len(self.cells[self.cells == CELL_ALIVE])

