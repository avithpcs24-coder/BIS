import random

# ============================================
# RESOURCE BUDGET OPTIMIZATION USING GA
# ============================================

# Input
budget = float(input("Enter total budget: "))
n = 3

projects = []

for i in range(n):
    print(f"\nProject {i + 1}")

    name = input("Enter project name: ")
    cost = float(input("Enter cost per unit: "))
    benefit = float(input("Enter benefit per unit: "))
    max_units = int(input("Enter maximum units: "))

    projects.append({
        "name": name,
        "cost": cost,
        "benefit": benefit,
        "max_units": max_units
    })


# ============================================
# Genetic Algorithm
# ============================================

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1


def create_solution():
    return [
        random.randint(0, p["max_units"])
        for p in projects
    ]


def calculate_cost(solution):
    return sum(
        solution[i] * projects[i]["cost"]
        for i in range(n)
    )


def calculate_benefit(solution):
    return sum(
        solution[i] * projects[i]["benefit"]
        for i in range(n)
    )


def fitness(solution):
    cost = calculate_cost(solution)

    if cost > budget:
        return 0

    return calculate_benefit(solution)


def selection(population):
    candidates = random.sample(population, 3)
    return max(candidates, key=fitness)


def crossover(parent1, parent2):
    point = random.randint(1, n - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def mutation(solution):
    for i in range(n):
        if random.random() < MUTATION_RATE:
            solution[i] = random.randint(
                0,
                projects[i]["max_units"]
            )

    return solution


def genetic_algorithm():

    population = [
        create_solution()
        for _ in range(POPULATION_SIZE)
    ]

    best_solution = None
    best_benefit = -1

    for generation in range(GENERATIONS):

        for solution in population:

            cost = calculate_cost(solution)
            benefit = calculate_benefit(solution)

            if cost <= budget and benefit > best_benefit:
                best_solution = solution[:]
                best_benefit = benefit

        new_population = []

        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            child1, child2 = crossover(
                parent1,
                parent2
            )

            mutation(child1)
            mutation(child2)

            new_population.append(child1)

            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    return best_solution


# ============================================
# Run Program
# ============================================

random.seed(42)

best = genetic_algorithm()

total_cost = calculate_cost(best)
total_benefit = calculate_benefit(best)

print("\n======================================")
print("       OPTIMIZATION RESULT")
print("======================================")

print("Project     Units     Cost     Benefit")
print("--------------------------------------")

for i, project in enumerate(projects):

    units = best[i]
    cost = units * project["cost"]
    benefit = units * project["benefit"]

    print(
        f"{project['name']:<12}"
        f"{units:<10}"
        f"{cost:<9.2f}"
        f"{benefit:.2f}"
    )

print("--------------------------------------")
print(f"Total Cost       : {total_cost:.2f}")
print(f"Budget           : {budget:.2f}")
print(f"Remaining Budget : {budget - total_cost:.2f}")
print(f"Total Benefit    : {total_benefit:.2f}")

print("======================================")
print("       Optimization Complete")
print("======================================")

