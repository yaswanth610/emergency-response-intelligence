import random
from enum import Enum


class TrafficLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    SEVERE = "SEVERE"


TRAFFIC_SPEEDS = {
    TrafficLevel.LOW: 60,
    TrafficLevel.MEDIUM: 45,
    TrafficLevel.HIGH: 30,
    TrafficLevel.SEVERE: 15,
}


def generate_traffic():
    """
    Generate a random traffic condition.

    Returns:
        Traffic level and estimated speed in km/h.
    """

    level = random.choice(
        list(TrafficLevel)
    )

    speed = TRAFFIC_SPEEDS[level]

    return {
        "level": level,
        "speed": speed,
    }