import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================
# PATHS
# ============================================

INPUT_FILE = Path(
    "data/benchmark_results.csv"
)

OUTPUT_DIR = Path(
    "data/charts"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv(
    INPUT_FILE
)

print()
print("📊 BENCHMARK CHART GENERATOR")
print("========================================")

print(
    f"Records loaded: {len(df)}"
)


# ============================================
# STRATEGY NAMES
# ============================================

strategies = [
    "Nearest ETA",
    "Severity Greedy",
    "Global Optimizer",
]


# ============================================
# 1. AVERAGE ETA
# ============================================

average_eta = [
    df["nearest_eta"].mean(),
    df["severity_greedy_eta"].mean(),
    df["optimizer_eta"].mean(),
]

plt.figure(figsize=(9, 6))

plt.bar(
    strategies,
    average_eta,
)

plt.ylabel(
    "Average ETA (minutes)"
)

plt.title(
    "Average Emergency Response ETA"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "average_eta.png",
    dpi=200,
)

plt.close()


# ============================================
# 2. 95TH PERCENTILE ETA
# ============================================

p95_eta = [
    df["nearest_eta"].quantile(0.95),
    df["severity_greedy_eta"].quantile(0.95),
    df["optimizer_eta"].quantile(0.95),
]

plt.figure(figsize=(9, 6))

plt.bar(
    strategies,
    p95_eta,
)

plt.ylabel(
    "95th Percentile ETA (minutes)"
)

plt.title(
    "Worst-Case Response Performance (P95)"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "p95_eta.png",
    dpi=200,
)

plt.close()


# ============================================
# 3. WEIGHTED RESPONSE COST
# ============================================

weighted_cost = [
    df["nearest_weighted_cost"].mean(),
    df["severity_greedy_weighted_cost"].mean(),
    df["optimizer_weighted_cost"].mean(),
]

plt.figure(figsize=(9, 6))

plt.bar(
    strategies,
    weighted_cost,
)

plt.ylabel(
    "Severity-Weighted Response Cost"
)

plt.title(
    "Severity-Weighted Response Cost"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "weighted_cost.png",
    dpi=200,
)

plt.close()


# ============================================
# 4. CRITICAL EMERGENCIES
# ============================================

critical_df = df[
    df["severity"] == "CRITICAL"
]

critical_eta = [
    critical_df["nearest_eta"].mean(),
    critical_df["severity_greedy_eta"].mean(),
    critical_df["optimizer_eta"].mean(),
]

plt.figure(figsize=(9, 6))

plt.bar(
    strategies,
    critical_eta,
)

plt.ylabel(
    "Average ETA (minutes)"
)

plt.title(
    "Critical Emergency Response ETA"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "critical_eta.png",
    dpi=200,
)

plt.close()


# ============================================
# SUMMARY
# ============================================

print()
print("✅ CHARTS GENERATED")
print("========================================")

print(
    f"Charts saved to: {OUTPUT_DIR}"
)

print()
print("Generated files:")

print(
    "1. average_eta.png"
)

print(
    "2. p95_eta.png"
)

print(
    "3. weighted_cost.png"
)

print(
    "4. critical_eta.png"
)