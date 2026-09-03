import csv
from pathlib import Path


def export_benchmark_results(
    records,
    output_file="data/benchmark_results.csv",
):
    """
    Export raw benchmark results to CSV.
    """

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not records:
        print("⚠️ No benchmark records to export.")
        return

    fieldnames = list(records[0].keys())

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(records)

    print()
    print("💾 BENCHMARK DATA EXPORTED")
    print("========================================")
    print(f"File: {output_path}")
    print(f"Records: {len(records)}")