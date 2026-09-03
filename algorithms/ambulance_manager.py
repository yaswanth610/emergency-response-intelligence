from simulation.models import AmbulanceStatus


def dispatch_ambulance(ambulance):
    """
    Mark an ambulance as dispatched.
    """

    if ambulance.status != AmbulanceStatus.AVAILABLE:
        return False

    ambulance.status = AmbulanceStatus.EN_ROUTE

    return True


def arrive_at_scene(ambulance):
    """
    Mark ambulance as arrived at emergency location.
    """

    if ambulance.status != AmbulanceStatus.EN_ROUTE:
        return False

    ambulance.status = AmbulanceStatus.AT_SCENE

    return True


def start_transport(ambulance):
    """
    Mark ambulance as transporting the patient.
    """

    if ambulance.status != AmbulanceStatus.AT_SCENE:
        return False

    ambulance.status = AmbulanceStatus.TRANSPORTING

    return True


def complete_transport(ambulance):
    """
    Return ambulance to available pool.
    """

    if ambulance.status != AmbulanceStatus.TRANSPORTING:
        return False

    ambulance.status = AmbulanceStatus.AVAILABLE

    return True