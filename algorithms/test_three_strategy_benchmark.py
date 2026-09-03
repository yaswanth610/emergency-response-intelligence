import requests

from algorithms.export_results import export_benchmark_results

from simulation.generator import (
    generate_ambulances,
    generate_emergency,
)

from algorithms.optimizer import optimize_assignments
from algorithms.dispatch import SEVERITY_WEIGHTS

from algorithms.evaluation import (
    evaluate_strategy,
    evaluate_critical_cases,
    print_evaluation,
    improvement_percentage,
)


NUM_SIMULATIONS = 500
NUM_AMBULANCES = 5
NUM_EMERGENCIES = 3


# ============================================
# BUILD ETA MATRIX
# ============================================

def build_eta_matrix(ambulances, emergencies):
    """
    Build road ETA matrix using one OSRM table request.
    """

    coordinates = []

    for ambulance in ambulances:
        coordinates.append(
            f"{ambulance.longitude},{ambulance.latitude}"
        )

    for emergency in emergencies:
        coordinates.append(
            f"{emergency.longitude},{emergency.latitude}"
        )

    coordinates_string = ";".join(coordinates)

    ambulance_count = len(ambulances)

    sources = ";".join(
        str(i)
        for i in range(ambulance_count)
    )

    destinations = ";".join(
        str(i)
        for i in range(
            ambulance_count,
            ambulance_count + len(emergencies),
        )
    )

    url = (
        "https://router.project-osrm.org/"
        f"table/v1/driving/"
        f"{coordinates_string}"
    )

    params = {
        "sources": sources,
        "destinations": destinations,
        "annotations": "duration",
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if data["code"] != "Ok":
        return None

    eta_matrix = {}

    for emergency_index, emergency in enumerate(
        emergencies
    ):

        eta_matrix[emergency.id] = {}

        for ambulance_index, ambulance in enumerate(
            ambulances
        ):

            eta_seconds = data["durations"][
                ambulance_index
            ][
                emergency_index
            ]

            if eta_seconds is not None:

                eta_matrix[
                    emergency.id
                ][
                    ambulance.id
                ] = eta_seconds / 60

    return eta_matrix


# ============================================
# COST CALCULATION
# ============================================

def calculate_cost(assignments):
    """
    Calculate total severity-weighted response cost.
    """

    total = 0.0

    for assignment in assignments:

        emergency = assignment["emergency"]

        eta = assignment["eta"]

        weight = SEVERITY_WEIGHTS[
            emergency.severity
        ]

        total += eta * weight

    return total


# ============================================
# STRATEGY 1
# ============================================

def nearest_eta_assignment(
    ambulances,
    emergencies,
    eta_matrix,
):
    """
    Strategy 1:
    Assign the lowest ETA ambulance
    to each emergency in generation order.
    """

    available = {
        ambulance.id: ambulance
        for ambulance in ambulances
    }

    assignments = []

    for emergency in emergencies:

        best_ambulance = None
        best_eta = float("inf")

        for ambulance_id in available:

            eta = eta_matrix.get(
                emergency.id,
                {},
            ).get(
                ambulance_id
            )

            if eta is None:
                continue

            if eta < best_eta:

                best_eta = eta

                best_ambulance = available[
                    ambulance_id
                ]

        if best_ambulance is None:
            continue

        assignments.append({
            "emergency": emergency,
            "ambulance": best_ambulance,
            "eta": best_eta,
        })

        del available[
            best_ambulance.id
        ]

    return assignments


# ============================================
# STRATEGY 2
# ============================================

def severity_greedy_assignment(
    ambulances,
    emergencies,
    eta_matrix,
):
    """
    Strategy 2:
    Prioritize emergencies by severity,
    then assign the best available ambulance.
    """

    available = {
        ambulance.id: ambulance
        for ambulance in ambulances
    }

    severity_order = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    ordered_emergencies = sorted(
        emergencies,
        key=lambda emergency:
        severity_order[
            emergency.severity.value
        ],
    )

    assignments = []

    for emergency in ordered_emergencies:

        best_ambulance = None
        best_eta = float("inf")

        for ambulance_id in available:

            eta = eta_matrix.get(
                emergency.id,
                {},
            ).get(
                ambulance_id
            )

            if eta is None:
                continue

            if eta < best_eta:

                best_eta = eta

                best_ambulance = available[
                    ambulance_id
                ]

        if best_ambulance is None:
            continue

        assignments.append({
            "emergency": emergency,
            "ambulance": best_ambulance,
            "eta": best_eta,
        })

        del available[
            best_ambulance.id
        ]

    return assignments


# ============================================
# STRATEGY 3
# ============================================

def optimizer_assignment(
    ambulances,
    emergencies,
    eta_matrix,
):
    """
    Strategy 3:
    Global optimization.
    """

    result = optimize_assignments(
        ambulances,
        emergencies,
        eta_matrix,
    )

    assignments = []

    for assignment in result["assignments"]:

        assignments.append({
            "emergency": assignment["emergency"],
            "ambulance": assignment["ambulance"],
            "eta": assignment["eta"],
        })

    return assignments


# ============================================
# BENCHMARK DATA
# ============================================

nearest_costs = []
severity_costs = []
optimized_costs = []

nearest_etas = []
severity_etas = []
optimized_etas = []

nearest_critical_etas = []
severity_critical_etas = []
optimized_critical_etas = []

# Raw results for CSV export
benchmark_records = []

successful = 0
failures = 0


# ============================================
# RUN SIMULATIONS
# ============================================

for _ in range(NUM_SIMULATIONS):

    ambulances = generate_ambulances(
        NUM_AMBULANCES
    )

    emergencies = [
        generate_emergency()
        for _ in range(NUM_EMERGENCIES)
    ]

    try:

        eta_matrix = build_eta_matrix(
            ambulances,
            emergencies,
        )

        if eta_matrix is None:
            failures += 1
            continue

    except requests.RequestException:

        failures += 1
        continue

    # ----------------------------------------
    # RUN ALL THREE STRATEGIES
    # ----------------------------------------

    nearest = nearest_eta_assignment(
        ambulances,
        emergencies,
        eta_matrix,
    )

    severity_greedy = severity_greedy_assignment(
        ambulances,
        emergencies,
        eta_matrix,
    )

    optimized = optimizer_assignment(
        ambulances,
        emergencies,
        eta_matrix,
    )

    # ----------------------------------------
    # VALIDATE RESULTS
    # ----------------------------------------

    if (
        len(nearest) != NUM_EMERGENCIES
        or len(severity_greedy) != NUM_EMERGENCIES
        or len(optimized) != NUM_EMERGENCIES
    ):
        continue

    # ----------------------------------------
    # CALCULATE COSTS
    # ----------------------------------------

    nearest_cost = calculate_cost(
        nearest
    )

    severity_cost = calculate_cost(
        severity_greedy
    )

    optimized_cost = calculate_cost(
        optimized
    )

    nearest_costs.append(
        nearest_cost
    )

    severity_costs.append(
        severity_cost
    )

    optimized_costs.append(
        optimized_cost
    )

    # ----------------------------------------
    # RECORD NEAREST ETA
    # ----------------------------------------

    for assignment in nearest:

        eta = assignment["eta"]

        nearest_etas.append(eta)

        if (
            assignment["emergency"].severity.value
            == "CRITICAL"
        ):
            nearest_critical_etas.append(eta)

    # ----------------------------------------
    # RECORD SEVERITY GREEDY ETA
    # ----------------------------------------

    for assignment in severity_greedy:

        eta = assignment["eta"]

        severity_etas.append(eta)

        if (
            assignment["emergency"].severity.value
            == "CRITICAL"
        ):
            severity_critical_etas.append(eta)

    # ----------------------------------------
    # RECORD OPTIMIZER ETA
    # ----------------------------------------

    for assignment in optimized:

        eta = assignment["eta"]

        optimized_etas.append(eta)

        if (
            assignment["emergency"].severity.value
            == "CRITICAL"
        ):
            optimized_critical_etas.append(eta)

    # ----------------------------------------
    # RECORD RAW BENCHMARK DATA
    # ----------------------------------------

    for emergency in emergencies:

        emergency_id = emergency.id

        nearest_assignment = next(
            assignment
            for assignment in nearest
            if assignment["emergency"].id
            == emergency_id
        )

        severity_assignment = next(
            assignment
            for assignment in severity_greedy
            if assignment["emergency"].id
            == emergency_id
        )

        optimized_assignment = next(
            assignment
            for assignment in optimized
            if assignment["emergency"].id
            == emergency_id
        )

        nearest_eta = nearest_assignment["eta"]
        severity_eta = severity_assignment["eta"]
        optimized_eta = optimized_assignment["eta"]

        severity_weight = SEVERITY_WEIGHTS[
            emergency.severity
        ]

        nearest_weighted_cost = (
            nearest_eta * severity_weight
        )

        severity_greedy_weighted_cost = (
            severity_eta * severity_weight
        )

        optimizer_weighted_cost = (
            optimized_eta * severity_weight
        )

        benchmark_records.append({
            "emergency_id": emergency.id,
            "severity": emergency.severity.value,
            "nearest_eta": nearest_eta,
            "severity_greedy_eta": severity_eta,
            "optimizer_eta": optimized_eta,
            "nearest_weighted_cost": (
                nearest_weighted_cost
            ),
            "severity_greedy_weighted_cost": (
                severity_greedy_weighted_cost
            ),
            "optimizer_weighted_cost": (
                optimizer_weighted_cost
            ),
        })

    successful += 1


# ============================================
# BASIC RESULTS
# ============================================

print()
print("🧠 THREE-STRATEGY BENCHMARK")
print("========================================")

print(
    f"Requested Simulations: "
    f"{NUM_SIMULATIONS}"
)

print(
    f"Successful Simulations: "
    f"{successful}"
)

print(
    f"OSRM Failures: "
    f"{failures}"
)


if successful == 0:

    print()
    print("No successful simulations.")
    raise SystemExit


nearest_average = (
    sum(nearest_costs)
    / len(nearest_costs)
)

severity_average = (
    sum(severity_costs)
    / len(severity_costs)
)

optimized_average = (
    sum(optimized_costs)
    / len(optimized_costs)
)


nearest_to_optimizer = (
    (
        nearest_average
        - optimized_average
    )
    / nearest_average
) * 100


severity_to_optimizer = (
    (
        severity_average
        - optimized_average
    )
    / severity_average
) * 100


print()
print("📊 AVERAGE WEIGHTED RESPONSE COST")
print("----------------------------------------")

print(
    f"Nearest ETA: "
    f"{nearest_average:.2f}"
)

print(
    f"Severity Greedy: "
    f"{severity_average:.2f}"
)

print(
    f"Global Optimizer: "
    f"{optimized_average:.2f}"
)


print()
print("🚀 OPTIMIZATION IMPACT")
print("----------------------------------------")

print(
    f"Optimizer vs Nearest ETA: "
    f"{nearest_to_optimizer:.2f}%"
)

print(
    f"Optimizer vs Severity Greedy: "
    f"{severity_to_optimizer:.2f}%"
)


# ============================================
# DETAILED EVALUATION
# ============================================

nearest_metrics = evaluate_strategy(
    nearest_etas,
    nearest_costs,
)

severity_metrics = evaluate_strategy(
    severity_etas,
    severity_costs,
)

optimized_metrics = evaluate_strategy(
    optimized_etas,
    optimized_costs,
)


strategies = {
    "Nearest ETA": nearest_metrics,
    "Severity Greedy": severity_metrics,
    "Global Optimizer": optimized_metrics,
}


print_evaluation(
    strategies
)


# ============================================
# CRITICAL EMERGENCY ANALYSIS
# ============================================

nearest_critical = evaluate_critical_cases(
    nearest_critical_etas
)

severity_critical = evaluate_critical_cases(
    severity_critical_etas
)

optimized_critical = evaluate_critical_cases(
    optimized_critical_etas
)


print()
print("🚨 CRITICAL EMERGENCY ANALYSIS")
print("========================================")

print(
    f"Critical Cases: "
    f"{optimized_critical['count']}"
)


if optimized_critical["count"] > 0:

    print(
        f"Nearest ETA: "
        f"{nearest_critical['average_eta']:.2f} min"
    )

    print(
        f"Severity Greedy: "
        f"{severity_critical['average_eta']:.2f} min"
    )

    print(
        f"Global Optimizer: "
        f"{optimized_critical['average_eta']:.2f} min"
    )

    critical_improvement = improvement_percentage(
        nearest_critical["average_eta"],
        optimized_critical["average_eta"],
    )

    print(
        f"Optimizer vs Nearest: "
        f"{critical_improvement:.2f}%"
    )

else:

    print(
        "No critical emergencies were generated."
    )


# ============================================
# EXPORT RAW RESULTS
# ============================================

export_benchmark_results(
    benchmark_records
)