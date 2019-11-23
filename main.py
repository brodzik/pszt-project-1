import argparse
import math
import time

from src.model import *
from src.utility import *
from src.benchmark import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world_size", type=int, default=4)
    parser.add_argument("--population_size", type=int, default=500)
    parser.add_argument("--individual_size", type=int, default=8*40)
    parser.add_argument("--mutation_rate", type=float, default=1e-3)
    parser.add_argument("--migration_interval", type=int, default=200)
    parser.add_argument("--migration_size", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    seed_everything(int(time.time()) if args.seed == 0 else args.seed)

    world = World(args.world_size,
                  args.population_size,
                  args.individual_size,
                  args.mutation_rate,
                  args.migration_interval,
                  args.migration_size,
                  rastrigin)
    best_individual = world.run_parallel(10000000, 0)
    print(best_individual)


if __name__ == "__main__":
    main()
