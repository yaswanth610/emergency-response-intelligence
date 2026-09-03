import statistics
import requests

from simulation.generator import (
    generate_ambulances,
    generate_emergency,
)

from simulation.models import AmbulanceStatus

from algorithms.dispatch import SEVERITY_WEIGHTS
from algorithms.optimizer import optimize_assignments


# ============================================
# CONFIGURATION
# ============================================

NUM_SIMULATIONS = 50

AMBULANCE_COUNT = 5
EMERGENCY_COUNT = 3


# ============================================
# OSRM MATRIX
# ============================================

def get_eta_matrix(
    ambulances,
    emergencies,
):
    """
    Get road ETA from every ambulance
    to every emergency.

    One OSRM table request.
    """

    coordinates = []

    for ambulance in ambulances:

        coordinates.append(
            f"{ambulance.longitude},"
            f"{ambulance.latitude}"
        )

    for emergency in emergencies:

        coordinates.append(
            f"{emergency.longitude},"
            f"{emergency.latitude}"
        )

    coordinate_string = ";".join(
        coordinates
    )

    ambulance_indices = ";".join(
        str(i)
        for i in range(
            len(ambulances)
        )
    )

    emergency_indices = ";".join(
        str(
            len(ambulances) + i
        )
        for i in range(
            len(emergencies)
        )
    )

    url = (
        "https://router.project-osrm.org/"
        "table/v1/driving/"
        + coordinate_string
    )

    params = {
        "sources": ambulance_indices,
        "destinations": emergency_indices,
        "annotations": "duration",
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            return None

        durations = data.get(
            "durations"
        )

        if durations is None:
            return None

        eta_matrix = {}

        for emergency_index, emergency in enumerate(
            emergencies
        ):

            eta_matrix[
                emergency.id
            ] = {}

            for ambulance_index, ambulance in enumerate(
                ambulances
            ):

                duration = durations[
                    ambulance_index
                ][
                    emergency_index
                ]

                if duration is None:
                    continue

                eta_matrix[
                    emergency.id
                ][
                    ambulance.id
                ] = duration / 60

        return eta_matrix

    except requests.RequestException:

        return None


# ============================================
# GREEDY STRATEGY
# ============================================

def greedy_assignment(
    ambulances,
    emergencies,
    eta_matrix,
):
    """
    Greedy strategy.

    Process emergencies in their
    original order and assign each
    the ambulance with the lowest
    severity-weighted ETA.
    """

    available = list(ambulances)

    assignments = []

    total_cost = 0.0

    for emergency in emergencies:

        best = None

        severity_weight = SEVERITY_WEIGHTS[
            emergency.severity
        ]

        for ambulance in available:

            eta = eta_matrix[
                emergency.id
            ].get(
                ambulance.id
            )

            if eta is None:
                continue

            cost = eta * severity_weight

            if best is None or cost < best["cost"]:

                best = {
                    "ambulance": ambulance,
                    "eta": eta,
                    "cost": cost,
                }

        if best is None:
            continue

        available.remove(
            best["ambulance"]
        )

        assignments.append({
            "emergency": emergency,
            "ambulance": best["ambulance"],
            "eta": best["eta"],
            "weighted_cost": best["cost"],
        })

        total_cost += best["cost"]

    return {
        "assignments": assignments,
        "total_cost": total_cost,
    }


# ============================================
# BENCHMARK
# ============================================

def run_benchmark():

    greedy_costs = []
    optimized_costs = []

    improvements = []

    failures = 0

    for simulation in range(
        1,
        NUM_SIMULATIONS + 1,
    ):

        ambulances = generate_ambulances(
            AMBULANCE_COUNT
        )

        emergencies = [
            generate_emergency()
            for _ in range(
                EMERGENCY_COUNT
            )
        ]

        eta_matrix = get_eta_matrix(
            ambulances,
            emergencies,
        )

        if eta_matrix is None:

            failures += 1

            print(
                f"⚠️ OSRM failure "
                f"on simulation {simulation}"
            )

            continue

        # ------------------------------------
        # Greedy
        # ------------------------------------

        greedy_result = greedy_assignment(
            ambulances,
            emergencies,
            eta_matrix,
        )

        # ------------------------------------
        # Optimized
        # ------------------------------------

        optimized_result = optimize_assignments(
            ambulances,
            emergencies,
            eta_matrix,
        )

        greedy_cost = (
            greedy_result["total_cost"]
        )

        optimized_cost = (
            optimized_result["total_cost"]
        )

        greedy_costs.append(
            greedy_cost
        )

        optimized_costs.append(
            optimized_cost
        )

        # ------------------------------------
        # Improvement
        # ------------------------------------

        if greedy_cost > 0:

            improvement = (
                (
                    greedy_cost
                    - optimized_cost
                )
                / greedy_cost
            ) * 100

            improvements.append(
                improvement
            )

    # ========================================
    # RESULTS
    # ========================================

    print()
    print("🧠 OPTIMIZATION BENCHMARK")
    print("========================================")

    print(
        f"Requested Simulations: "
        f"{NUM_SIMULATIONS}"
    )

    print(
        f"Successful Simulations: "
        f"{len(greedy_costs)}"
    )

    print(
        f"OSRM Failures: "
        f"{failures}"
    )

    print()
    print("📊 WEIGHTED RESPONSE COST")
    print("----------------------------------------")

    if greedy_costs:

        print(
            f"Greedy Average Cost: "
            f"{statistics.mean(greedy_costs):.2f}"
        )

    if optimized_costs:

        print(
            f"Optimized Average Cost: "
            f"{statistics.mean(optimized_costs):.2f}"
        )

    print()
    print("🚀 OPTIMIZATION IMPACT")
    print("----------------------------------------")

    if improvements:

        print(
            f"Average Improvement: "
            f"{statistics.mean(improvements):.2f}%"
        )

        print(
            f"Best Improvement: "
            f"{max(improvements):.2f}%"
        )

        print(
            f"Worst Improvement: "
            f"{min(improvements):.2f}%"
        )


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    run_benchmark()