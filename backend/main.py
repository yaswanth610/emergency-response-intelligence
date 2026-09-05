from fastapi import FastAPI
from pydantic import BaseModel

from simulation.generator import (
    generate_ambulances,
    generate_hospitals,
)
from simulation.models import Emergency, EmergencySeverity
from algorithms.response_engine import handle_emergency


app = FastAPI(
    title="Emergency Response Intelligence System",
    version="0.3.0",
)


# Simulated city state
ambulances = generate_ambulances(10)
hospitals = generate_hospitals(5)


class DispatchRequest(BaseModel):
    latitude: float
    longitude: float
    severity: EmergencySeverity


@app.get("/")
def root():
    return {
        "system": "Emergency Response Intelligence System",
        "status": "online",
        "version": "0.3.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/ambulances")
def get_ambulances():
    return {
        "count": len(ambulances),
        "ambulances": [
            {
                "id": ambulance.id,
                "latitude": ambulance.latitude,
                "longitude": ambulance.longitude,
                "status": ambulance.status.value,
            }
            for ambulance in ambulances
        ],
    }


@app.get("/hospitals")
def get_hospitals():
    return {
        "count": len(hospitals),
        "hospitals": [
            {
                "id": hospital.id,
                "name": hospital.name,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
                "total_beds": hospital.total_beds,
                "available_beds": hospital.available_beds,
                "icu_total": hospital.icu_total,
                "icu_available": hospital.icu_available,
            }
            for hospital in hospitals
        ],
    }


@app.post("/dispatch")
def dispatch_emergency(request: DispatchRequest):

    emergency = Emergency(
        id=f"E{__import__('random').randint(1000, 9999)}",
        latitude=request.latitude,
        longitude=request.longitude,
        severity=request.severity,
    )

    result = handle_emergency(
        ambulances,
        hospitals,
        emergency,
    )

    response = {
        "emergency": {
            "id": emergency.id,
            "latitude": emergency.latitude,
            "longitude": emergency.longitude,
            "severity": emergency.severity.value,
        },
        "ambulance": None,
        "hospital": None,
    }

    if result["ambulance"]:
        ambulance_result = result["ambulance"]

        response["ambulance"] = {
            "id": ambulance_result["ambulance"].id,
            "distance_km": round(
                ambulance_result["distance"],
                2,
            ),
            "eta_minutes": round(
                ambulance_result["eta"],
                2,
            ),
            "priority_score": round(
                ambulance_result["score"],
                2,
            ),
            "route": ambulance_result["geometry"],
        }

    if result["hospital"]:
        hospital_result = result["hospital"]

        response["hospital"] = {
            "id": hospital_result["hospital"].id,
            "name": hospital_result["hospital"].name,
            "distance_km": round(
                hospital_result["distance"],
                2,
            ),
            "eta_minutes": round(
                hospital_result["eta"],
                2,
            ),
            "available_beds": (
                hospital_result["hospital"].available_beds
            ),
            "icu_available": (
                hospital_result["hospital"].icu_available
            ),
            "route": hospital_result["geometry"],
        }

    return response