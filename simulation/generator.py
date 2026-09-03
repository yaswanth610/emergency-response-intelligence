import random

from simulation.models import (
    Ambulance,
    Hospital,
    Emergency,
    AmbulanceStatus,
    EmergencySeverity,
)


# Approximate center of our simulated city
CITY_LATITUDE = 12.9716
CITY_LONGITUDE = 79.1597


def random_location():
    latitude = CITY_LATITUDE + random.uniform(-0.05, 0.05)
    longitude = CITY_LONGITUDE + random.uniform(-0.05, 0.05)

    return latitude, longitude


def generate_ambulances(count=10):
    ambulances = []

    for i in range(1, count + 1):
        lat, lon = random_location()

        ambulances.append(
            Ambulance(
                id=f"A{i:03}",
                latitude=lat,
                longitude=lon,
                status=AmbulanceStatus.AVAILABLE,
            )
        )

    return ambulances


def generate_hospitals(count=5):
    hospitals = []

    for i in range(1, count + 1):
        lat, lon = random_location()

        total_beds = random.randint(50, 200)
        available_beds = random.randint(10, total_beds)

        icu_total = random.randint(5, 30)
        icu_available = random.randint(0, icu_total)

        hospitals.append(
            Hospital(
                id=f"H{i:03}",
                name=f"Hospital {i}",
                latitude=lat,
                longitude=lon,
                total_beds=total_beds,
                available_beds=available_beds,
                icu_total=icu_total,
                icu_available=icu_available,
            )
        )

    return hospitals


def generate_emergency():
    lat, lon = random_location()

    severity = random.choice(
        list(EmergencySeverity)
    )

    return Emergency(
        id=f"E{random.randint(1000, 9999)}",
        latitude=lat,
        longitude=lon,
        severity=severity,
    )