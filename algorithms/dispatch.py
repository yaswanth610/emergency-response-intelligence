from simulation.models import AmbulanceStatus, EmergencySeverity

from algorithms.routing import get_route


SEVERITY_WEIGHTS = {
    EmergencySeverity.CRITICAL: 4.0,
    EmergencySeverity.HIGH: 2.5,
    EmergencySeverity.MEDIUM: 1.5,
    EmergencySeverity.LOW: 1.0,
}


def find_best_ambulance(ambulances, emergency):

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

        route = get_route(
            ambulance.latitude,
            ambulance.longitude,
            emergency.latitude,
            emergency.longitude,
        )

        if route is None:
            continue

        distance = route["distance_km"]
        eta = route["duration_minutes"]

        score = eta / severity_weight

        ranked.append({
            "ambulance": ambulance,
            "distance": distance,
            "eta": eta,
            "score": score,
            "geometry": route["geometry"],
        })

    if not ranked:
        return None

    ranked.sort(
        key=lambda item: item["score"]
    )

    return ranked[0]