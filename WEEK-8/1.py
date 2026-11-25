import random

# Step 1: Initialize parameters
weights = [2, 3, 4, 5, 1]
profits = [10, 15, 20, 25, 8]
print("Avith P Shetty", "1WN24CS056")

capacity = 10
population_size = 6
mutation_rate = 0.1
crossover_rate = 0.8
max_generations = 5

# Step 2: Initialize population
population = [
    [random.randint(0, 1) for _ in weights]
    for _ in range(population_size)
]

# Step 3: Fitness function
def fitness(chromosome):
    total_weight = sum(
        chromosome[i] * weights[i]
        for i in range(len(weights))
    )
    total_profit = sum(
        chromosome[i] * profits[i]
        for i in range(len(weights))
    )

    if total_weight > capacity:
        return 0
    return total_profit

# Step 4: Evolution process
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
            point = random.randint(1, len(weights) - 1)
            c1 = p1[:point] + p2[point:]
            c2 = p2[:point] + p1[point:]
        else:
            c1, c2 = p1.copy(), p2.copy()

        offspring.extend([c1, c2])

    # Mutation and gene expression
    for child in offspring:
        for j in range(len(child)):
            if random.random() < mutation_rate:
                child[j] = 1 - child[j]

        # Gene expression: decode chromosome
        solution = child
        fitness(solution)

    population = offspring

# Step 5: Output best solution
print("Best Solution:", best_solution)
print("Maximum Profit:", best_fitness)
print("Total Weight:",
      sum(best_solution[i] * weights[i]
          for i in range(len(weights))))
