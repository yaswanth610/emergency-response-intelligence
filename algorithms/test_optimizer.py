from simulation.generator import (
    generate_ambulances,
    generate_emergency,
)

from algorithms.routing import get_route
from algorithms.optimizer import optimize_assignments


# ============================================
# GENERATE SIMULATION
# ============================================

ambulances = generate_ambulances(5)

emergencies = [
    generate_emergency()
    for _ in range(3)
]


# ============================================
# BUILD ETA MATRIX
# ============================================

eta_matrix = {}

for emergency in emergencies:

    eta_matrix[emergency.id] = {}

    for ambulance in ambulances:

        route = get_route(
            ambulance.latitude,
            ambulance.longitude,
            emergency.latitude,
            emergency.longitude,
        )

        if route is not None:

            eta_matrix[
                emergency.id
            ][
                ambulance.id
            ] = route["duration_minutes"]


# ============================================
# OPTIMIZE
# ============================================

result = optimize_assignments(
    ambulances,
    emergencies,
    eta_matrix,
)


# ============================================
# DISPLAY
# ============================================

print()
print("🧠 MULTI-EMERGENCY OPTIMIZER")
print("========================================")

print(
    f"Emergencies: "
    f"{len(emergencies)}"
)

print(
    f"Ambulances: "
    f"{len(ambulances)}"
)


print()
print("🚨 OPTIMAL ASSIGNMENTS")
print("----------------------------------------")

for assignment in result["assignments"]:

    emergency = assignment["emergency"]
    ambulance = assignment["ambulance"]

    print(
        f"{emergency.id} "
        f"({emergency.severity.value})"
        f" → "
        f"{ambulance.id}"
        f" | ETA: "
        f"{assignment['eta']:.2f} min"
        f" | Weighted Cost: "
        f"{assignment['weighted_cost']:.2f}"
    )


print()
print(
    f"Total Weighted Cost: "
    f"{result['total_cost']:.2f}"
)