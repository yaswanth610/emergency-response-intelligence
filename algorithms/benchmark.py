import statistics
import requests

from simulation.generator import (
    generate_ambulances,
    generate_emergency,
)

from simulation.models import AmbulanceStatus, EmergencySeverity

from algorithms.distance import haversine_distance
from algorithms.dispatch import SEVERITY_WEIGHTS


# ============================================
# CONFIGURATION
# ============================================

NUM_SIMULATIONS = 100

OSRM_TABLE_URL = (
    "https://router.project-osrm.org/table/v1/driving/"
)


# ============================================
# OSRM ROAD ETA MATRIX
# ============================================

def get_road_etas(ambulances, emergency):
    """
    Get road travel times from every ambulance
    to the emergency using one OSRM table request.

    Returns:
        Dictionary:
        {
            ambulance_id: ETA in minutes
        }

        Returns None if OSRM fails.
    """

    coordinates = []

    for ambulance in ambulances:
        coordinates.append(
            f"{ambulance.longitude},{ambulance.latitude}"
        )

    coordinates.append(
        f"{emergency.longitude},{emergency.latitude}"
    )

    coordinate_string = ";".join(coordinates)

    url = OSRM_TABLE_URL + coordinate_string

    params = {
        "sources": ";".join(
            str(i)
            for i in range(len(ambulances))
        ),
        "destinations": str(len(ambulances)),
        "annotations": "duration",
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != "Ok":
            return None

        durations = data.get("durations")

        if not durations:
            return None

        etas = {}

        for index, ambulance in enumerate(ambulances):

            duration_seconds = durations[index][0]

            if duration_seconds is None:
                continue

            etas[ambulance.id] = (
                duration_seconds / 60
            )

        return etas

    except requests.RequestException:

        return None


# ============================================
# BASELINE DISPATCH
# ============================================

def baseline_dispatch(ambulances, emergency):
    """
    Baseline:
    Choose the geographically nearest ambulance.

    Uses straight-line distance.
    """

    available = [
        ambulance
        for ambulance in ambulances
        if ambulance.status == AmbulanceStatus.AVAILABLE
    ]

    if not available:
        return None

    ranked = []

    for ambulance in available:

        distance = haversine_distance(
            ambulance.latitude,
            ambulance.longitude,
            emergency.latitude,
            emergency.longitude,
        )

        ranked.append({
            "ambulance": ambulance,
            "distance": distance,
        })

    ranked.sort(
        key=lambda item: item["distance"]
    )

    return ranked[0]


# ============================================
# INTELLIGENT DISPATCH
# ============================================

def intelligent_dispatch(
    ambulances,
    emergency,
    road_etas,
):
    """
    Intelligent strategy:

    Road ETA
    +
    Emergency severity

    Lower score = better candidate.
    """

    available = [
        ambulance
        for ambulance in ambulances
        if ambulance.status == AmbulanceStatus.AVAILABLE
    ]

    if not available:
        return None

    severity_weight = SEVERITY_WEIGHTS[
        emergency.severity
    ]

    ranked = []

    for ambulance in available:

        if ambulance.id not in road_etas:
            continue

        eta = road_etas[
            ambulance.id
        ]

        score = eta / severity_weight

        ranked.append({
            "ambulance": ambulance,
            "eta": eta,
            "score": score,
        })

    if not ranked:
        return None

    ranked.sort(
        key=lambda item: item["score"]
    )

    return ranked[0]


# ============================================
# PERCENTILE
# ============================================

def percentile(values, percentage):

    if not values:
        return None

    values = sorted(values)

    index = (
        (len(values) - 1)
        * percentage
        / 100
    )

    lower = int(index)
    upper = lower + 1

    if upper >= len(values):
        return values[lower]

    fraction = index - lower

    return (
        values[lower]
        + (
            values[upper]
            - values[lower]
        )
        * fraction
    )


# ============================================
# BENCHMARK
# ============================================

def run_benchmark():

    baseline_times = []
    intelligent_times = []

    critical_baseline = []
    critical_intelligent = []

    routing_failures = 0

    for simulation_number in range(
        1,
        NUM_SIMULATIONS + 1,
    ):

        # ------------------------------------
        # Generate city
        # ------------------------------------

        ambulances = generate_ambulances(10)

        emergency = generate_emergency()

        # ------------------------------------
        # Baseline
        # ------------------------------------

        baseline_result = baseline_dispatch(
            ambulances,
            emergency,
        )

        if baseline_result is None:
            continue

        # ------------------------------------
        # OSRM matrix
        # ------------------------------------

        road_etas = get_road_etas(
            ambulances,
            emergency,
        )

        if road_etas is None:

            routing_failures += 1

            print(
                f"⚠️ OSRM failed on simulation "
                f"{simulation_number}"
            )

            continue

        # ------------------------------------
        # Intelligent
        # ------------------------------------

        intelligent_result = intelligent_dispatch(
            ambulances,
            emergency,
            road_etas,
        )

        if intelligent_result is None:

            routing_failures += 1

            continue

        # ------------------------------------
        # Actual response ETAs
        # ------------------------------------

        baseline_ambulance = (
            baseline_result["ambulance"]
        )

        intelligent_ambulance = (
            intelligent_result["ambulance"]
        )

        baseline_eta = road_etas.get(
            baseline_ambulance.id
        )

        intelligent_eta = road_etas.get(
            intelligent_ambulance.id
        )

        if (
            baseline_eta is None
            or intelligent_eta is None
        ):
            routing_failures += 1
            continue

        baseline_times.append(
            baseline_eta
        )

        intelligent_times.append(
            intelligent_eta
        )

        # ------------------------------------
        # Critical emergencies
        # ------------------------------------

        if (
            emergency.severity
            == EmergencySeverity.CRITICAL
        ):

            critical_baseline.append(
                baseline_eta
            )

            critical_intelligent.append(
                intelligent_eta
            )

    # ========================================
    # RESULTS
    # ========================================

    print()
    print("🚑 EMERGENCY RESPONSE BENCHMARK")
    print("========================================")

    print(
        f"Requested Simulations: "
        f"{NUM_SIMULATIONS}"
    )

    print(
        f"Successful Simulations: "
        f"{len(intelligent_times)}"
    )

    print(
        f"OSRM Failures: "
        f"{routing_failures}"
    )

    # ========================================
    # OVERALL
    # ========================================

    print()
    print("📊 OVERALL PERFORMANCE")
    print("----------------------------------------")

    if baseline_times:

        baseline_avg = statistics.mean(
            baseline_times
        )

        print(
            f"Baseline Average ETA: "
            f"{baseline_avg:.2f} minutes"
        )

    if intelligent_times:

        intelligent_avg = statistics.mean(
            intelligent_times
        )

        print(
            f"Intelligent Average ETA: "
            f"{intelligent_avg:.2f} minutes"
        )

    if baseline_times and intelligent_times:

        improvement = (
            (
                baseline_avg
                - intelligent_avg
            )
            / baseline_avg
        ) * 100

        print(
            f"Improvement: "
            f"{improvement:.2f}%"
        )

    # ========================================
    # 95TH PERCENTILE
    # ========================================

    print()
    print("📈 RESPONSE TIME DISTRIBUTION")
    print("----------------------------------------")

    if baseline_times:

        print(
            f"Baseline 95th Percentile: "
            f"{percentile(baseline_times, 95):.2f} minutes"
        )

    if intelligent_times:

        print(
            f"Intelligent 95th Percentile: "
            f"{percentile(intelligent_times, 95):.2f} minutes"
        )

    # ========================================
    # CRITICAL
    # ========================================

    print()
    print("🚨 CRITICAL EMERGENCIES")
    print("----------------------------------------")

    print(
        f"Critical Cases: "
        f"{len(critical_intelligent)}"
    )

    if critical_baseline:

        critical_base_avg = statistics.mean(
            critical_baseline
        )

        print(
            f"Baseline Critical ETA: "
            f"{critical_base_avg:.2f} minutes"
        )

    if critical_intelligent:

        critical_int_avg = statistics.mean(
            critical_intelligent
        )

        print(
            f"Intelligent Critical ETA: "
            f"{critical_int_avg:.2f} minutes"
        )

    if (
        critical_baseline
        and critical_intelligent
    ):

        critical_improvement = (
            (
                critical_base_avg
                - critical_int_avg
            )
            / critical_base_avg
        ) * 100

        print(
            f"Critical Improvement: "
            f"{critical_improvement:.2f}%"
        )


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    run_benchmark()