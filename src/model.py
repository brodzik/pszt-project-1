import copy
import json
import math
import multiprocessing
import os
import time

import numpy as np
import pandas as pd
from tqdm import tqdm


class Individual:
    def __init__(self, individual_size, fitness_function):
        self.individual_size = individual_size
        self.fitness_function = fitness_function

        assert individual_size > 0

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

    def data_to_string(self):
        result = ""
        for bit in self.data:
            result += str(bit)
        return result


class Population:
    def __init__(self, population_size, individual_size, mutation_rate, fitness_function):
        self.population_size = population_size
        self.individual_size = individual_size
        self.mutation_rate = mutation_rate
        self.fitness_function = fitness_function

        assert population_size > 0
        assert individual_size > 0

        self.individuals = [Individual(individual_size, fitness_function) for i in range(population_size)]

    def get_best(self):
        self.sort()
        return self.individuals[0]

    def select(self, k):
        weights = np.array([x.score for x in self.individuals])
        weights = weights - min(weights) + 1
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

    def sort(self):
        self.individuals = sorted(self.individuals, key=lambda x: x.score, reverse=True)
        self.individuals = self.individuals[:self.population_size]

    def run(self):
        self.sort()

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

        assert world_size > 0
        assert population_size > 0
        assert individual_size > 0

        self.islands = [Population(population_size, individual_size, mutation_rate, fitness_function) for i in range(world_size)]

    def migrate(self):
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

    def run_parallel_island(self, island):
        for i in range(self.migration_interval):
            island.run()
        return island

    def run_parallel(self, generations, max_time, target_score, name):
        assert self.world_size > 1
        assert self.migration_interval > 0
        assert self.migration_size > 0

        log = pd.DataFrame(columns=["generation", "score"])

        splits = generations // self.migration_interval
        status = tqdm(range(splits))
        best_individual = self.islands[0].individuals[0]
        start_time = time.time()

        for split in status:
            with multiprocessing.Pool() as pool:
                self.islands = pool.map(self.run_parallel_island, self.islands)

            for island in self.islands:
                if island.get_best().score > best_individual.score:
                    best_individual = island.get_best()

            status.set_description("score: {}".format(best_individual.score))

            log = log.append({"generation": split * self.migration_interval, "score": best_individual.score}, ignore_index=True)
            log.to_csv(os.path.join("output", name + ".log"), index=False)

            if math.fabs(target_score - best_individual.score) < 1e-32:
                print("Score target reached.")
                return best_individual

            if time.time() - start_time >= max_time:
                print("Time limit reached.")
                return best_individual

            self.migrate()

        print("Generations limit reached.")
        return best_individual

    def run_single_island(self, generations, max_time, target_score, name):
        assert self.world_size == 1
        assert self.migration_interval == 0
        assert self.migration_size == 0

        log = pd.DataFrame(columns=["generation", "score"])

        status = tqdm(range(generations))
        best_individual = self.islands[0].individuals[0]
        start_time = time.time()

        for generation_idx in status:
            for island in self.islands:
                island.run()

                if island.get_best().score > best_individual.score:
                    best_individual = island.get_best()

            status.set_description("score: {}".format(best_individual.score))

            log = log.append({"generation": generation_idx, "score": best_individual.score}, ignore_index=True)
            log.to_csv(os.path.join("output", name + ".log"), index=False)

            if math.fabs(target_score - best_individual.score) < 1e-32:
                print("Score target reached.")
                return best_individual

            if time.time() - start_time >= max_time:
                print("Time limit reached.")
                return best_individual

        print("Generations limit reached.")
        return best_individual
