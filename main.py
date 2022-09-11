import pygame
import numpy as np
import matplotlib.pyplot as plt
from game_of_life.constants import COLS, DELTA, ROWS, WIDTH, HEIGHT
from game_of_life.board import Board
from game_of_life.genetic_algorithm import Population
from game_of_life.helper import print_msg
FPS = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Game of life')
def main():
    run = True
    clock = pygame.time.Clock()
    # initiate = np.array([
    #     [1, 1, 1],
    #     [0, 1, 0],
    #     [1, 0, 1]
    # ])
    board = Board(WIN)
    population = Population(board)
    population.generate_population(100)

    i = 0
    while (run):
        i += 1
        try:
            population.evolve(DELTA)
        except KeyboardInterrupt:
            run = False
        best_of_gen = population.population_data[0]
        board.set_seed(best_of_gen)
        for _ in range(DELTA + 1):
            clock.tick(3)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    run = False
            # the main logic
            board.draw_board()
            board.update_board()
            print_msg(f'Gen {i}', WIN, 20, 20)
            board.print_result(best_of_gen)
            # update the screen
            pygame.display.update()

    pygame.quit()

main()