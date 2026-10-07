# Install required libraries
# pip install pyswarms scikit-learn pandas numpy -q

import numpy as np
import pandas as pd

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

import pyswarms as ps


# -------------------------------------------------------
# 1. CREATE SAMPLE INTRUSION DETECTION DATA
# -------------------------------------------------------

X, y = make_classification(
    n_samples=5000,
    n_features=20,
    n_informative=12,
    n_redundant=4,
    n_classes=2,
    weights=[0.7, 0.3],
    random_state=42
)

# 0 = Normal traffic
# 1 = Attack


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)


# -------------------------------------------------------
# 2. FITNESS FUNCTION
# -------------------------------------------------------

def fitness_function(params):

    results = []

    for particle in params:

        # PSO gives continuous values,
        # so convert them into valid Random Forest parameters

        n_estimators = int(particle[0])
        max_depth = int(particle[1])

        n_estimators = max(10, n_estimators)
        max_depth = max(2, max_depth)

        # Create IDS classifier
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )

        # Train
        model.fit(X_train, y_train)

        # Prediction
        y_pred = model.predict(X_test)

        # Accuracy
        accuracy = accuracy_score(y_test, y_pred)

        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(
            y_test,
            y_pred
        ).ravel()

        # False Alarm Rate
        false_alarm_rate = fp / (fp + tn)

        # ------------------------------------------------
        # Objective:
        # MAXIMIZE accuracy
        # MINIMIZE false alarm rate
        #
        # Since PSO minimizes the fitness,
        # convert accuracy into (1 - accuracy)
        # ------------------------------------------------

        fitness = (
            0.7 * (1 - accuracy)
            +
            0.3 * false_alarm_rate
        )

        results.append(fitness)

    return np.array(results)


# -------------------------------------------------------
# 3. DEFINE PSO SEARCH SPACE
# -------------------------------------------------------

# n_estimators: 10 - 200
# max_depth:     2 - 30

lower_bound = np.array([10, 2])
upper_bound = np.array([200, 30])

bounds = (lower_bound, upper_bound)


# -------------------------------------------------------
# 4. PSO OPTIONS
# -------------------------------------------------------

options = {
    'c1': 1.5,   # Cognitive coefficient
    'c2': 1.5,   # Social coefficient
    'w': 0.7     # Inertia weight
}


# -------------------------------------------------------
# 5. CREATE PSO OPTIMIZER
# -------------------------------------------------------

optimizer = ps.single.GlobalBestPSO(
    n_particles=10,
    dimensions=2,
    options=options,
    bounds=bounds
)


# -------------------------------------------------------
# 6. RUN PSO
# -------------------------------------------------------

best_cost, best_position = optimizer.optimize(
    fitness_function,
    iters=20
)


# -------------------------------------------------------
# 7. GET OPTIMAL PARAMETERS
# -------------------------------------------------------

best_n_estimators = int(best_position[0])
best_max_depth = int(best_position[1])


print("\n========== PSO RESULT ==========")

print("Optimal n_estimators :", best_n_estimators)
print("Optimal max_depth    :", best_max_depth)

print("Best fitness         :", best_cost)


# -------------------------------------------------------
# 8. TRAIN FINAL IDS USING OPTIMAL PARAMETERS
# -------------------------------------------------------

final_model = RandomForestClassifier(
    n_estimators=best_n_estimators,
    max_depth=best_max_depth,
    random_state=42,
    n_jobs=-1
)

final_model.fit(X_train, y_train)

y_pred = final_model.predict(X_test)


# -------------------------------------------------------
# 9. CALCULATE FINAL PERFORMANCE
# -------------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred
).ravel()

false_alarm_rate = fp / (fp + tn)

detection_rate = tp / (tp + fn)


# -------------------------------------------------------
# 10. FINAL OUTPUT
# -------------------------------------------------------

print("\n========== FINAL IDS PERFORMANCE ==========")

print("Detection Accuracy :", round(accuracy * 100, 2), "%")
print("Detection Rate     :", round(detection_rate * 100, 2), "%")
print("False Alarm Rate   :", round(false_alarm_rate * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))