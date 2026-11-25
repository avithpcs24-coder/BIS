
import random

# Step 1: Initialize parameters
cost = [20000, 30000, 15000, 25000, 10000]
benefit = [40, 60, 35, 50, 25]
print("Avith P Shetty", "1WN24CS056")

budget = 100000
population_size = 6
mutation_rate = 0.1
crossover_rate = 0.8
max_generations = 5

# Step 2: Initialize population
population = [
    [random.randint(0, 1) for _ in cost]
    for _ in range(population_size)
]

# Step 3: Fitness function
def fitness(chromosome):
    total_cost = sum(
        chromosome[i] * cost[i]
        for i in range(len(cost))
    )

    total_benefit = sum(
        chromosome[i] * benefit[i]
        for i in range(len(benefit))
    )

    if total_cost > budget:
        return 0

    return total_benefit

# Step 4: Genetic Algorithm
best_solution = None
best_fitness = 0

for gen in range(max_generations):

    scores = [fitness(c) for c in population]

    # Store best solution
    index = scores.index(max(scores))

    if scores[index] > best_fitness:
        best_fitness = scores[index]
        best_solution = population[index].copy()

    # Selection
    selected = []

    for i in range(population_size):
        a, b = random.sample(range(population_size), 2)
        winner = a if scores[a] >= scores[b] else b
        selected.append(population[winner].copy())

    # Crossover
    offspring = []

    for i in range(0, population_size, 2):
        p1 = selected[i]
        p2 = selected[i + 1]

        if random.random() < crossover_rate:
            point = random.randint(1, len(cost) - 1)
            c1 = p1[:point] + p2[point:]
            c2 = p2[:point] + p1[point:]
        else:
            c1, c2 = p1.copy(), p2.copy()

        offspring.extend([c1, c2])

    # Mutation
    for child in offspring:
        for j in range(len(child)):
            if random.random() < mutation_rate:
                child[j] = 1 - child[j]

    # Update population
    population = offspring

# Step 5: Calculate final results
total_cost = sum(
    best_solution[i] * cost[i]
    for i in range(len(cost))
)

total_benefit = sum(
    best_solution[i] * benefit[i]
    for i in range(len(benefit))
)

remaining_budget = budget - total_cost

# Step 6: Display output
print("\n--- Resource Budget Optimization ---")
print("Total Cost       :", total_cost)
print("Available Budget :", budget)
print("Remaining Budget :", remaining_budget)
print("Total Benefit    :", total_benefit)

print("\nSelected Projects:")
for i in range(len(cost)):
    if best_solution[i] == 1:
        print("Project", i + 1)

