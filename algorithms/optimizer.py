from functools import lru_cache

from simulation.models import EmergencySeverity
from algorithms.dispatch import SEVERITY_WEIGHTS


def optimize_assignments(
    ambulances,
    emergencies,
    eta_matrix,
):
    """
    Find the ambulance assignment that minimizes
    total severity-weighted response time.

    eta_matrix format:

    {
        emergency_id: {
            ambulance_id: eta_minutes
        }
    }

    Each ambulance can be assigned to at most
    one emergency.

    Returns:
        List of assignment dictionaries.
    """

    if not emergencies:
        return []

    if not ambulances:
        return []

    # We need at least one ambulance per emergency.
    if len(ambulances) < len(emergencies):
        raise ValueError(
            "Not enough ambulances for all emergencies."
        )

    ambulance_ids = tuple(
        ambulance.id
        for ambulance in ambulances
    )

    emergency_ids = tuple(
        emergency.id
        for emergency in emergencies
    )

    # ----------------------------------------
    # Cost function
    # ----------------------------------------

    def assignment_cost(
        emergency,
        ambulance_id,
    ):
        eta = eta_matrix.get(
            emergency.id,
            {},
        ).get(
            ambulance_id
        )

        if eta is None:
            return float("inf")

        severity_weight = SEVERITY_WEIGHTS[
            emergency.severity
        ]

        return eta * severity_weight

    # ----------------------------------------
    # Dynamic programming
    # ----------------------------------------

    @lru_cache(maxsize=None)
    def solve(
        emergency_index,
        used_mask,
    ):
        """
        Returns:

        (
            minimum_cost,
            ambulance_indices
        )
        """

        # All emergencies assigned.
        if emergency_index == len(
            emergencies
        ):
            return 0.0, ()

        emergency = emergencies[
            emergency_index
        ]

        best_cost = float("inf")
        best_assignment = None

        for ambulance_index in range(
            len(ambulances)
        ):

            # Ambulance already assigned.
            if used_mask & (
                1 << ambulance_index
            ):
                continue

            ambulance_id = ambulance_ids[
                ambulance_index
            ]

            current_cost = assignment_cost(
                emergency,
                ambulance_id,
            )

            if current_cost == float("inf"):
                continue

            remaining_cost, remaining_assignment = solve(
                emergency_index + 1,
                used_mask
                | (1 << ambulance_index),
            )

            total_cost = (
                current_cost
                + remaining_cost
            )

            if total_cost < best_cost:

                best_cost = total_cost

                best_assignment = (
                    ambulance_index,
                ) + remaining_assignment

        return (
            best_cost,
            best_assignment,
        )

    total_cost, assignment_indices = solve(
        0,
        0,
    )

    if assignment_indices is None:
        return []

    # ----------------------------------------
    # Build result
    # ----------------------------------------

    assignments = []

    for emergency_index, ambulance_index in enumerate(
        assignment_indices
    ):

        emergency = emergencies[
            emergency_index
        ]

        ambulance = ambulances[
            ambulance_index
        ]

        eta = eta_matrix[
            emergency.id
        ][
            ambulance.id
        ]

        severity_weight = SEVERITY_WEIGHTS[
            emergency.severity
        ]

        weighted_cost = (
            eta * severity_weight
        )

        assignments.append({
            "emergency": emergency,
            "ambulance": ambulance,
            "eta": eta,
            "severity": emergency.severity,
            "weighted_cost": weighted_cost,
        })

    return {
        "assignments": assignments,
        "total_cost": total_cost,
    }