from simulation.generator import (
    generate_hospitals,
    generate_emergency,
)

from algorithms.hospital import (
    find_best_hospital,
)


hospitals = generate_hospitals(5)

emergency = generate_emergency()


result = find_best_hospital(
    hospitals,
    emergency,
)


print("\n🚨 EMERGENCY")
print("----------------------")

print(
    f"Emergency ID: {emergency.id}"
)

print(
    f"Severity: {emergency.severity.value}"
)


if result:

    hospital = result["hospital"]
    distance = result["distance"]
    eta = result["eta"]
    score = result["score"]

    print("\n🏥 HOSPITAL DECISION")
    print("----------------------")

    print(
        f"Hospital: {hospital.name}"
    )

    print(
        f"Distance: {distance:.2f} km"
    )

    print(
        f"Estimated Time: {eta:.2f} minutes"
    )

    print(
        f"Available Beds: {hospital.available_beds}"
    )

    print(
        f"ICU Available: {hospital.icu_available}"
    )

    print(
        f"Hospital Score: {score:.2f}"
    )

else:

    print(
        "\n❌ No suitable hospital available."
    )