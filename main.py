import argparse

from src.model import *
from src.utility import *


def fitness_function(data):
    score = 0
    for bit in data:
        if bit == 1:
            score += 1
    return score


def main():
    seed_everything(1234)

    parser = argparse.ArgumentParser()
    parser.add_argument("world_size", type=int)
    parser.add_argument("population_size", type=int)
    parser.add_argument("individual_size", type=int)
    parser.add_argument("mutation_rate", type=float)
    parser.add_argument("migration_interval", type=int)
    parser.add_argument("migration_size", type=int)

    args = parser.parse_args()

    world = World(**vars(args), fitness_function=fitness_function)
    world.run(100)


if __name__ == "__main__":
    main()
