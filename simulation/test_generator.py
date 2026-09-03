from simulation.generator import (
    generate_ambulances,
    generate_hospitals,
    generate_emergency,
)


ambulances = generate_ambulances(5)
hospitals = generate_hospitals(3)
emergency = generate_emergency()


print("\nAMBULANCES")

for ambulance in ambulances:
    print(ambulance)


print("\nHOSPITALS")

for hospital in hospitals:
    print(hospital)


print("\nEMERGENCY")

print(emergency)