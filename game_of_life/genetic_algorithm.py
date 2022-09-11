import numpy as np
from .constants import INIT_SIZE
from collections import Counter

class Population:
    def __init__(self, board, retain_ratio=0.8, retain_random=0.05, swap_rate=0.1, mutate_chance=0.05) -> None:
        self.board = board
        self.retain_ratio = retain_ratio
        self.retain_random = retain_random
        self.swap_rate = swap_rate
        self.mutate_chance = mutate_chance
        self.og_mutate_chance = mutate_chance
        self.population_data = []
        self.scores = []
    
    def generate_population(self, size):
        self.population_data = np.split(np.random.binomial(1, 0.5, (INIT_SIZE * size, INIT_SIZE)), size)
    
    def fitness(self, initiate, delta):
        self.board.set_seed(initiate)
        for _ in range(delta):
            total_alive = self.board.update_board()
        return total_alive

    def get_score_population(self, delta):
        scores = []
        for i, gene in enumerate(self.population_data):
            scores.append(self.fitness(gene, delta))
        self.scores = scores

    def selection(self):
        retain_len = int(len(self.scores) *  self.retain_ratio)
        sorted_scores_indices = np.argsort(self.scores)[::-1]
        self.scores = [self.scores[idx] for idx in sorted_scores_indices]
        self.population_data = [self.population_data[idx] for idx in sorted_scores_indices]
        selected = self.population_data[:retain_len]
        left_over = self.population_data[retain_len:]
        for gene in left_over:
            if np.random.rand() < self.retain_random:
                selected.append(gene)
        
        return selected
    
    def mutate(self):
        # increase mutate chance if the algorithm is stuck at a local minima
        dup_rate = max([v for k,v in Counter(self.scores).items()]) / len(self.scores)
        print(f'-> dup rate: {dup_rate}')
        if (dup_rate > 0.6):
            self.mutate_chance = dup_rate / 2
        else:
            self.mutate_chance = self.og_mutate_chance
        for gene in self.population_data[1:]:
            if np.random.rand() < self.mutate_chance:
                    a = np.random.binomial(1, self.swap_rate, size=(INIT_SIZE, INIT_SIZE)).astype('bool')
                    gene[a] += 1
                    gene[a] %= 2

    def crossover(self, mom, dad):
        select_mask = np.random.binomial(1, 0.5, size=(INIT_SIZE, INIT_SIZE)).astype('bool')
        child1, child2 = np.copy(mom), np.copy(dad)
        child1[select_mask] = dad[select_mask]
        child2[select_mask] = mom[select_mask]
        return child1, child2
    
    def evolve(self, delta):
        self.get_score_population(delta)
        selected_population = self.selection()
        print(f'best scores: {self.scores[0]}')
        # retain some of the selected_population and keep it to the next population
        next_population = selected_population[:int(len(selected_population) * 0.05)]
        left_over = len(self.population_data) - len(next_population)
        children = []
        parent_max_idx = len(selected_population) - 1
        while (len(children) < left_over):
            mom_idx, dad_idx = np.random.randint(0, parent_max_idx, 2)
            if mom_idx != dad_idx:
                child1, child2 = self.crossover(selected_population[mom_idx], selected_population[dad_idx])
                children.append(child1)
                if len(children) < left_over:
                    children.append(child2)
        
        next_population.extend(children)
        self.population_data = next_population
        self.mutate()