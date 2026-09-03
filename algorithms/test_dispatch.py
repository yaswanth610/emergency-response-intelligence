from simulation.generator import (
    generate_ambulances,
    generate_emergency,
)

from algorithms.dispatch import (
    find_best_ambulance,
)


ambulances = generate_ambulances(10)

emergency = generate_emergency()


result = find_best_ambulance(
    ambulances,
    emergency,
)


print("\n🚨 EMERGENCY")
print("============================")

print(
    f"Emergency ID: {emergency.id}"
)

print(
    f"Severity: {emergency.severity.value}"
)


if result:

    ambulance = result["ambulance"]

    print("\n🚑 DISPATCH DECISION")
    print("----------------------------")

    print(
        f"Ambulance: {ambulance.id}"
    )

    print(
        f"Road Distance: "
        f"{result['distance']:.2f} km"
    )

    print(
        f"Road ETA: "
        f"{result['eta']:.2f} minutes"
    )

    print(
        f"Priority Score: "
        f"{result['score']:.2f}"
    )

    print(
        f"Route Points: "
        f"{len(result['geometry']['coordinates'])}"
    )

else:

    print(
        "\n❌ No ambulance could be routed."
    )