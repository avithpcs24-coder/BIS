import numpy as np

# --------------------------------
# 1. GENERATOR DATA
# --------------------------------

a = np.array([500, 400, 200])
b = np.array([5.3, 5.5, 5.8])
c = np.array([0.004, 0.006, 0.009])

Pmin = np.array([50, 50, 50])
Pmax = np.array([200, 150, 100])

PD = 300

n_gen = 3
n_wolves = 30
max_iter = 100

np.random.seed(42)


# --------------------------------
# 2. POWER BALANCE REPAIR
# --------------------------------

def repair(position):

    low = -1000.0
    high = 1000.0

    for _ in range(100):

        mid = (low + high) / 2

        P = np.clip(
            position - mid,
            Pmin,
            Pmax
        )

        if np.sum(P) > PD:
            low = mid
        else:
            high = mid

    return np.clip(
        position - (low + high) / 2,
        Pmin,
        Pmax
    )


# --------------------------------
# 3. FUEL COST FUNCTION
# --------------------------------

def fuel_cost(P):

    cost = a + b * P + c * P**2

    return np.sum(cost)


# --------------------------------
# 4. FITNESS FUNCTION
# --------------------------------

def fitness(position):

    P = repair(position)

    return fuel_cost(P)


# --------------------------------
# 5. INITIALIZE WOLF POPULATION
# --------------------------------

wolves = np.random.uniform(
    Pmin,
    Pmax,
    (n_wolves, n_gen)
)

for i in range(n_wolves):
    wolves[i] = repair(wolves[i])


# Initialize alpha, beta and delta

alpha_pos = np.zeros(n_gen)
beta_pos = np.zeros(n_gen)
delta_pos = np.zeros(n_gen)

alpha_score = float("inf")
beta_score = float("inf")
delta_score = float("inf")


# --------------------------------
# 6. GREY WOLF OPTIMIZATION
# --------------------------------

for iteration in range(max_iter):

    # Evaluate fitness of wolves

    for i in range(n_wolves):

        wolves[i] = repair(wolves[i])

        score = fitness(wolves[i])

        # Alpha wolf
        if score < alpha_score:

            delta_score = beta_score
            delta_pos = beta_pos.copy()

            beta_score = alpha_score
            beta_pos = alpha_pos.copy()

            alpha_score = score
            alpha_pos = wolves[i].copy()

        # Beta wolf
        elif score < beta_score:

            delta_score = beta_score
            delta_pos = beta_pos.copy()

            beta_score = score
            beta_pos = wolves[i].copy()

        # Delta wolf
        elif score < delta_score:

            delta_score = score
            delta_pos = wolves[i].copy()

    # Decrease control parameter

    A_parameter = 2 - 2 * iteration / max_iter

    # Update wolf positions

    for i in range(n_wolves):

        # Alpha position

        r1 = np.random.rand(n_gen)
        r2 = np.random.rand(n_gen)

        A1 = 2 * A_parameter * r1 - A_parameter
        C1 = 2 * r2

        D_alpha = np.abs(
            C1 * alpha_pos - wolves[i]
        )

        X1 = alpha_pos - A1 * D_alpha

        # Beta position

        r1 = np.random.rand(n_gen)
        r2 = np.random.rand(n_gen)

        A2 = 2 * A_parameter * r1 - A_parameter
        C2 = 2 * r2

        D_beta = np.abs(
            C2 * beta_pos - wolves[i]
        )

        X2 = beta_pos - A2 * D_beta

        # Delta position

        r1 = np.random.rand(n_gen)
        r2 = np.random.rand(n_gen)

        A3 = 2 * A_parameter * r1 - A_parameter
        C3 = 2 * r2

        D_delta = np.abs(
            C3 * delta_pos - wolves[i]
        )

        X3 = delta_pos - A3 * D_delta

        # Calculate new position

        new_position = (X1 + X2 + X3) / 3

        # Repair power balance

        wolves[i] = repair(new_position)


# --------------------------------
# 7. FINAL OPTIMAL RESULTS
# --------------------------------

optimal_P = repair(alpha_pos)

minimum_cost = fuel_cost(optimal_P)

total_power = np.sum(optimal_P)

print("\n===== GWO BASED ECONOMIC LOAD DISPATCH =====")
print(f"Generator Power: G1={optimal_P[0]:.2f} MW, G2={optimal_P[1]:.2f} MW, G3={optimal_P[2]:.2f} MW")
print(f"Total Power Generated: {total_power:.2f} MW")
print(f"Total Load Demand: {PD:.2f} MW")
print(f"Minimum Fuel Cost: ${minimum_cost:.2f}/hour")
