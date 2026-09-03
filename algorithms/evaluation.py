from statistics import mean


def percentile(values, percentile_value):
    """
    Calculate a percentile using linear interpolation.
    """

    if not values:
        return None

    sorted_values = sorted(values)

    position = (
        (len(sorted_values) - 1)
        * percentile_value
        / 100
    )

    lower = int(position)

    upper = min(
        lower + 1,
        len(sorted_values) - 1,
    )

    fraction = position - lower

    return (
        sorted_values[lower]
        + (
            sorted_values[upper]
            - sorted_values[lower]
        )
        * fraction
    )


def average(values):
    """
    Calculate the average of a list.
    """

    if not values:
        return None

    return mean(values)


def improvement_percentage(
    baseline,
    optimized,
):
    """
    Calculate percentage improvement.

    Positive value means optimized is better.
    """

    if baseline == 0:
        return 0.0

    return (
        (baseline - optimized)
        / baseline
    ) * 100


def evaluate_strategy(
    response_times,
    weighted_costs,
):
    """
    Generate performance metrics for one strategy.
    """

    if not response_times:
        return {
            "average_eta": None,
            "p95_eta": None,
            "average_weighted_cost": None,
        }

    return {
        "average_eta": average(response_times),
        "p95_eta": percentile(
            response_times,
            95,
        ),
        "average_weighted_cost": average(
            weighted_costs
        ),
    }


def evaluate_critical_cases(
    response_times,
):
    """
    Evaluate response times for critical emergencies.
    """

    if not response_times:
        return {
            "count": 0,
            "average_eta": None,
            "p95_eta": None,
        }

    return {
        "count": len(response_times),
        "average_eta": average(
            response_times
        ),
        "p95_eta": percentile(
            response_times,
            95,
        ),
    }


def compare_strategies(
    baseline_metrics,
    optimized_metrics,
):
    """
    Compare optimized strategy against baseline.
    """

    return {
        "eta_improvement": improvement_percentage(
            baseline_metrics["average_eta"],
            optimized_metrics["average_eta"],
        ),
        "p95_improvement": improvement_percentage(
            baseline_metrics["p95_eta"],
            optimized_metrics["p95_eta"],
        ),
        "weighted_cost_improvement": improvement_percentage(
            baseline_metrics[
                "average_weighted_cost"
            ],
            optimized_metrics[
                "average_weighted_cost"
            ],
        ),
    }


def print_evaluation(strategies):
    """
    Print a formatted strategy comparison.
    """

    print()
    print("📊 PERFORMANCE EVALUATION")
    print("========================================")

    print(
        f"{'Metric':<28}"
        f"{'Nearest':>12}"
        f"{'Greedy':>12}"
        f"{'Optimizer':>12}"
    )

    print("-" * 64)

    nearest = strategies["Nearest ETA"]
    greedy = strategies["Severity Greedy"]
    optimizer = strategies["Global Optimizer"]

    print(
        f"{'Average ETA (min)':<28}"
        f"{nearest['average_eta']:>12.2f}"
        f"{greedy['average_eta']:>12.2f}"
        f"{optimizer['average_eta']:>12.2f}"
    )

    print(
        f"{'95th Percentile ETA':<28}"
        f"{nearest['p95_eta']:>12.2f}"
        f"{greedy['p95_eta']:>12.2f}"
        f"{optimizer['p95_eta']:>12.2f}"
    )

    print(
        f"{'Weighted Response Cost':<28}"
        f"{nearest['average_weighted_cost']:>12.2f}"
        f"{greedy['average_weighted_cost']:>12.2f}"
        f"{optimizer['average_weighted_cost']:>12.2f}"
    )