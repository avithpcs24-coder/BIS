import random
import networkx as nx

# 1. Create computer network
G = nx.Graph()

edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2),
    ('D', 'F', 6),
    ('E', 'F', 3)
]

G.add_weighted_edges_from(edges)

source = 'A'
destination = 'F'


# 2. Generate a valid path
def generate_path():
    return nx.shortest_path(
        G, source, destination, weight='weight'
    )


# 3. Calculate path cost
def fitness(path):
    cost = 0

    for i in range(len(path) - 1):
        cost += G[path[i]][path[i+1]]['weight']

    return cost


# 4. Generate a new candidate path
def generate_new_path(path):
    new_path = path.copy()

    if len(new_path) > 2:
        index = random.randint(1, len(new_path) - 2)

        current = new_path[index - 1]
        next_node = new_path[index + 1]

        candidates = [
            n for n in G.neighbors(current)
            if n != next_node and n not in new_path[:index]
        ]

        if candidates:
            new_path[index] = random.choice(candidates)

            try:
                tail = nx.shortest_path(
                    G, new_path[index], destination,
                    weight='weight'
                )
                new_path = new_path[:index] + tail

            except nx.NetworkXNoPath:
                return generate_path()

    return new_path


# 5. Cuckoo Search Algorithm
def cuckoo_search(nests=20, iterations=100,
                  discovery_rate=0.25):

    population = [generate_path() for _ in range(nests)]

    population.sort(key=fitness)

    best_path = population[0]
    best_cost = fitness(best_path)

    for iteration in range(iterations):

        for i in range(nests):

            new_path = generate_new_path(population[i])
            new_cost = fitness(new_path)

            j = random.randint(0, nests - 1)

            if new_cost < fitness(population[j]):
                population[j] = new_path

            if new_cost < best_cost:
                best_path = new_path
                best_cost = new_cost

        # Abandon poor nests
        population.sort(key=fitness)

        abandon_count = int(discovery_rate * nests)

        for i in range(nests - abandon_count, nests):
            population[i] = generate_path()

        population.sort(key=fitness)

        if fitness(population[0]) < best_cost:
            best_path = population[0]
            best_cost = fitness(best_path)

    return best_path, best_cost


# 6. Display final result
best_path, best_cost = cuckoo_search()

print("\n----- OPTIMAL NETWORK ROUTE -----")
print("Source:", source)
print("Destination:", destination)
print("Optimal Path:", " -> ".join(best_path))
print("Minimum Communication Cost:", best_cost)
print("Routing Status: Successful")

