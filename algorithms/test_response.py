from simulation.generator import (
    generate_ambulances,
    generate_hospitals,
    generate_emergency,
)

from algorithms.response_engine import handle_emergency


# Generate simulation data
ambulances = generate_ambulances(10)
hospitals = generate_hospitals(5)
emergency = generate_emergency()


# Handle emergency
result = handle_emergency(
    ambulances,
    hospitals,
    emergency,
)


# =========================
# EMERGENCY
# =========================

print("\n🚨 EMERGENCY RESPONSE")
print("============================")

print(f"Emergency ID: {emergency.id}")
print(f"Severity: {emergency.severity.value}")


# =========================
# AMBULANCE
# =========================

ambulance_result = result["ambulance"]

if ambulance_result:

    ambulance = ambulance_result["ambulance"]

    print("\n🚑 AMBULANCE")
    print("----------------------------")

    print(f"Assigned: {ambulance.id}")
    print(f"Status: {ambulance.status.value}")

    print(
        f"Road Distance: "
        f"{ambulance_result['distance']:.2f} km"
    )

    print(
        f"Road ETA: "
        f"{ambulance_result['eta']:.2f} minutes"
    )

    print(
        f"Priority Score: "
        f"{ambulance_result['score']:.2f}"
    )

    print(
        f"Route Points: "
        f"{len(ambulance_result['geometry']['coordinates'])}"
    )

else:

    print("\n❌ No ambulance available.")


# =========================
# HOSPITAL
# =========================

hospital_result = result["hospital"]

if hospital_result:

    hospital = hospital_result["hospital"]

    print("\n🏥 HOSPITAL")
    print("----------------------------")

    print(f"Destination: {hospital.name}")

    print(
    f"Road Distance: "
    f"{hospital_result['distance']:.2f} km"
   )

    print(
        f"ETA: "
        f"{hospital_result['eta']:.2f} minutes"
    )

    print(
        f"Available Beds: "
        f"{hospital.available_beds}"
    )

    print(
        f"ICU Available: "
        f"{hospital.icu_available}"
    )

    print(
        f"Hospital Score: "
        f"{hospital_result['score']:.2f}"
    )

    print(
    f"Route Points: "
    f"{len(hospital_result['geometry']['coordinates'])}"
    )

else:

    print("\n❌ No suitable hospital available.")