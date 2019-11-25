#!/bin/bash
python main.py \
    --world_size 4 \
    --population_size 500 \
    --individual_size 560 \
    --mutation_rate 0.001 \
    --migration_interval 100 \
    --migration_size 2 \
    --seed 42 \
    --fitness_function "rastrigin" \
    --function_complexity 40 \
    --max_generations 1000000 \
    --max_time 10 \
    --target_score 0 \
    --name "test_1"
