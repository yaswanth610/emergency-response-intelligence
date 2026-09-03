from simulation.models import EmergencySeverity

from algorithms.routing import get_route


def find_best_hospital(hospitals, emergency):

    ranked = []

    for hospital in hospitals:

        # No beds = cannot accept patient
        if hospital.available_beds <= 0:
            continue

        # Critical patients require ICU
        if (
            emergency.severity == EmergencySeverity.CRITICAL
            and hospital.icu_available <= 0
        ):
            continue

        route = get_route(
            emergency.latitude,
            emergency.longitude,
            hospital.latitude,
            hospital.longitude,
        )

        if route is None:
            continue

        distance = route["distance_km"]
        eta = route["duration_minutes"]

        # --------------------------------
        # Hospital scoring
        # --------------------------------

        if emergency.severity == EmergencySeverity.CRITICAL:

            # ICU is extremely important.
            capacity_score = (
                hospital.icu_available * 5
                + hospital.available_beds
            )

        elif emergency.severity == EmergencySeverity.HIGH:

            capacity_score = (
                hospital.icu_available * 2
                + hospital.available_beds
            )

        else:

            capacity_score = hospital.available_beds

        # Lower score = better hospital
        score = eta / (capacity_score + 1)

        ranked.append({
            "hospital": hospital,
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