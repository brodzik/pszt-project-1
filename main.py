import argparse
import math
import time

from src.benchmark import *
from src.model import *
from src.utility import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--world_size", type=int)
    parser.add_argument("--population_size", type=int)
    parser.add_argument("--individual_size", type=int)
    parser.add_argument("--mutation_rate", type=float)
    parser.add_argument("--migration_interval", type=int)
    parser.add_argument("--migration_size", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--fitness_function", type=str)
    parser.add_argument("--function_complexity", type=int)
    parser.add_argument("--max_generations", type=int)
    parser.add_argument("--max_time", type=int)
    parser.add_argument("--target_score", type=int)
    parser.add_argument("--name", type=str)

    args = parser.parse_args()

    seed_everything(int(time.time()) if args.seed == 0 else args.seed)

    if args.fitness_function == "griewangk":
        fitness_function = Griewangk(args.function_complexity)
    elif args.fitness_function == "rastrigin":
        fitness_function = Rastrigin(args.function_complexity)
    else:
        raise "Invalid fitness function"

    if not os.path.exists("output"):
        os.makedirs("output")

    with open(os.path.join("output", args.name + ".params"), "w") as json_file:
        json.dump(vars(args), json_file, indent=4)

    world = World(
        args.world_size,
        args.population_size,
        args.individual_size,
        args.mutation_rate,
        args.migration_interval,
        args.migration_size,
        fitness_function
    )
    world.run_parallel(args.max_generations, args.max_time, args.target_score, args.name)
    #world.run_single_island(args.max_generations, args.max_time, args.target_score, args.name)


if __name__ == "__main__":
    main()
