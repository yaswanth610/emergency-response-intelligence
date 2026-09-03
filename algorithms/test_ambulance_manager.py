from simulation.generator import generate_ambulances

from algorithms.ambulance_manager import (
    dispatch_ambulance,
    arrive_at_scene,
    start_transport,
    complete_transport,
)


ambulances = generate_ambulances(3)

ambulance = ambulances[0]


print("\n🚑 AMBULANCE LIFECYCLE")
print("============================")


print(
    f"\nAmbulance: {ambulance.id}"
)

print(
    f"Initial Status: "
    f"{ambulance.status.value}"
)


dispatch_ambulance(ambulance)

print(
    f"After Dispatch: "
    f"{ambulance.status.value}"
)


arrive_at_scene(ambulance)

print(
    f"At Scene: "
    f"{ambulance.status.value}"
)


start_transport(ambulance)

print(
    f"Transporting: "
    f"{ambulance.status.value}"
)


complete_transport(ambulance)

print(
    f"Available Again: "
    f"{ambulance.status.value}"
)