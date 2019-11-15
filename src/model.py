import numpy as np


class Individual:
    def __init__(self, individual_size, fitness_function):
        self.individual_size = individual_size
        self.fitness_function = fitness_function
        self.data = np.random.randint(0, 2, individual_size, int)
        self.score = self.evaluate()

    def __str__(self):
        return "score: {}".format(self.score)

    def __repr__(self):
        return str(self)

    def evaluate(self):
        return self.fitness_function(self.data)

    def reevaluate(self):
        self.score = self.evaluate()


class Population:
    def __init__(self, population_size, individual_size, fitness_function):
        self.individuals = [Individual(individual_size, fitness_function) for i in range(population_size)]

    def select(self):
        weights = np.array([x.score for x in self.individuals])
        weights = weights / weights.sum()
        return np.random.choice(self.individuals, size=2, p=weights)

    def run(self):
        self.individuals = sorted(self.individuals, key=lambda x: x.score, reverse=True)
        parents = self.select()


class World:
    def __init__(self,
                 world_size,
                 population_size,
                 individual_size,
                 mutation_rate,
                 migration_interval,
                 migration_size,
                 fitness_function):
        self.islands = [Population(population_size, individual_size, fitness_function) for i in range(world_size)]
        self.generation = 0

    def run(self, generations):
        for generation_idx in range(generations):
            for island_population in self.islands:
                island_population.run()
            self.generation += 1
