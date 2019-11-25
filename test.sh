#!/bin/bash

i=0

for world_size in 2 3 4 5 10; do
for population_size in 100 500 1000; do
for mutation_rate in 0.1 0.01 0.001; do
for migration_interval in 100 500 1000; do
for migration_size in 1 2 3 4 5 10; do

echo "Running test $i..."
python main.py \
    --world_size $world_size \
    --population_size $population_size \
    --individual_size 280 \
    --mutation_rate $mutation_rate \
    --migration_interval $migration_interval \
    --migration_size $migration_size \
    --seed 42 \
    --fitness_function "rastrigin" \
    --function_complexity 20 \
    --max_generations 1000000 \
    --max_time 300 \
    --target_score 0 \
    --name "test_$i"
echo "Test $i finished."

((i=i+1))

done
done
done
done
done
