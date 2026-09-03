from algorithms.dispatch import find_best_ambulance
from algorithms.hospital import find_best_hospital
from algorithms.ambulance_manager import dispatch_ambulance


def handle_emergency(
    ambulances,
    hospitals,
    emergency,
):
    ambulance_result = find_best_ambulance(
        ambulances,
        emergency,
    )

    hospital_result = find_best_hospital(
        hospitals,
        emergency,
    )

    if ambulance_result:
        ambulance = ambulance_result["ambulance"]
        dispatch_ambulance(ambulance)

    return {
        "emergency": emergency,
        "ambulance": ambulance_result,
        "hospital": hospital_result,
    }