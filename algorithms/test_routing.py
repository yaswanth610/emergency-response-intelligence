from simulation.generator import (
    generate_ambulances,
    generate_emergency,
)

from algorithms.routing import get_route


ambulances = generate_ambulances(1)

emergency = generate_emergency()

ambulance = ambulances[0]


route = get_route(
    ambulance.latitude,
    ambulance.longitude,
    emergency.latitude,
    emergency.longitude,
)


print("\n🗺️ ROAD ROUTING")
print("============================")

print(
    f"Ambulance: {ambulance.id}"
)

print(
    f"Emergency: {emergency.id}"
)


if route:

    print(
        f"Road Distance: "
        f"{route['distance_km']:.2f} km"
    )

    print(
        f"Road ETA: "
        f"{route['duration_minutes']:.2f} minutes"
    )

    print(
        f"Route Points: "
        f"{len(route['geometry']['coordinates'])}"
    )

else:

    print("❌ Route not found.")