import copy

import numpy as np
from tqdm import tqdm


class Individual:
    def __init__(self, individual_size, fitness_function):
        self.individual_size = individual_size
        self.fitness_function = fitness_function

        self.data = np.random.random_integers(0, 1, individual_size)
        self.score = self.evaluate()

    def __str__(self):
        return "score: {},\tdata: {}".format(self.score, self.data)

    def __repr__(self):
        return str(self)

    def evaluate(self):
        return self.fitness_function(self.data)

    def reevaluate(self):
        self.score = self.evaluate()


class Population:
    def __init__(self, population_size, individual_size, mutation_rate, fitness_function):
        self.population_size = population_size
        self.individual_size = individual_size
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function

        self.individuals = [Individual(individual_size, fitness_function) for i in range(population_size)]

    def select(self, k):
        weights = np.array([x.score for x in self.individuals])
        weights = weights / weights.sum()

        parents = np.random.choice(self.individuals, size=k, p=weights)

        return parents

    def crossover(self, parent_1, parent_2):
        child_1 = copy.deepcopy(parent_1)
        child_2 = copy.deepcopy(parent_2)

        pivot = np.random.random_integers(0, self.individual_size)

        child_1.data[:pivot] = parent_2.data[:pivot]
        child_2.data[:pivot] = parent_1.data[:pivot]

        return child_1, child_2

    def mutate(self, child):
        for i in range(child.individual_size):
            if np.random.uniform(0, 1) < self.mutation_rate:
                child.data[i] = (child.data[i] + 1) % 2

    def run(self):
        self.individuals = sorted(self.individuals, key=lambda x: x.score, reverse=True)
        self.individuals = self.individuals[:self.population_size]

        parent_1, parent_2 = self.select(2)

        child_1, child_2 = self.crossover(parent_1, parent_2)

        self.mutate(child_1)
        self.mutate(child_2)

        child_1.reevaluate()
        child_2.reevaluate()

        self.individuals.append(child_1)
        self.individuals.append(child_2)


class World:
    def __init__(self,
                 world_size,
                 population_size,
                 individual_size,
                 mutation_rate,
                 migration_interval,
                 migration_size,
                 fitness_function):
        self.world_size = world_size
        self.population_size = population_size
        self.individual_size = individual_size
        self.mutation_rate = mutation_rate
        self.migration_interval = migration_interval
        self.migration_size = migration_size
        self.fitness_function = fitness_function

        self.islands = [Population(population_size, individual_size, mutation_rate, fitness_function) for i in range(world_size)]

    def run(self, generations):
        for generation_idx in tqdm(range(generations)):
            for island in self.islands:
                island.run()

            if self.migration_interval > 0 and self.world_size > 1:
                if generation_idx % self.migration_interval == self.migration_interval - 1:
                    migrant_groups = []

                    for island in self.islands:
                        migrant_groups.append({
                            "individuals": island.select(self.migration_size),
                            "destination": np.random.randint(self.world_size)
                        })

                    for migrant_group in migrant_groups:
                        for individual in migrant_group["individuals"]:
                            migrant = copy.deepcopy(individual)
                            self.islands[migrant_group["destination"]].individuals.append(migrant)
