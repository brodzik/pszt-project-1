import argparse
import time

from src.model import *
from src.utility import *


def fitness_function(data):
    score = 0
    for bit in data:
        if bit == 1:
            score += 1
    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world_size", type=int, default=1)
    parser.add_argument("--population_size", type=int, default=500)
    parser.add_argument("--individual_size", type=int, default=100)
    parser.add_argument("--mutation_rate", type=float, default=1e-3)
    parser.add_argument("--migration_interval", type=int, default=0)
    parser.add_argument("--migration_size", type=int, default=0)
    parser.add_argument("--seed", type=int, default=0)

    args = parser.parse_args()

    seed_everything(int(time.time()) if args.seed == 0 else args.seed)

    world = World(args.world_size,
                  args.population_size,
                  args.individual_size,
                  args.mutation_rate,
                  args.migration_interval,
                  args.migration_size,
                  fitness_function)
    world.run(10000)
    print(world.islands[0].individuals[0])


if __name__ == "__main__":
    main()
