from algorithms.evaluation import (
    percentile,
    average,
    improvement_percentage,
    evaluate_strategy,
)


response_times = [
    5.0,
    7.0,
    8.0,
    10.0,
    12.0,
]


weighted_costs = [
    10.0,
    14.0,
    16.0,
    20.0,
    24.0,
]


metrics = evaluate_strategy(
    response_times,
    weighted_costs,
)


print()
print("🧪 EVALUATION MODULE TEST")
print("========================================")

print(
    f"Average ETA: "
    f"{metrics['average_eta']:.2f} minutes"
)

print(
    f"95th Percentile ETA: "
    f"{metrics['p95_eta']:.2f} minutes"
)

print(
    f"Average Weighted Cost: "
    f"{metrics['average_weighted_cost']:.2f}"
)


print()
print(
    f"90th Percentile Test: "
    f"{percentile(response_times, 90):.2f}"
)

print(
    f"Improvement Test: "
    f"{improvement_percentage(100, 80):.2f}%"
)