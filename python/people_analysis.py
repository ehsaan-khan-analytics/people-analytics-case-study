"""Privacy-aware People Analytics retention analysis using aggregated outputs only."""

from pathlib import Path
import pandas as pd

DATA = Path("data/workforce.csv")
OUTPUT = Path("outputs")
OUTPUT.mkdir(exist_ok=True)
MIN_GROUP_SIZE = 25
AS_OF_DATE = pd.Timestamp("2025-12-31")


df = pd.read_csv(DATA, parse_dates=["hire_date", "exit_date"])
assert df["employee_id"].is_unique, "Duplicate employee IDs found"
assert (df["scheduled_days"] > 0).all(), "Scheduled days must be positive"
assert (df["absence_days"] >= 0).all(), "Absence days cannot be negative"
assert (df["absence_days"] <= df["scheduled_days"]).all(), "Absence exceeds scheduled days"

df["tenure_days"] = (AS_OF_DATE - df["hire_date"]).dt.days.clip(lower=0)
df["tenure_band"] = pd.cut(
    df["tenure_days"],
    bins=[-1, 364, 729, 1460, float("inf")],
    labels=["Under 12 months", "12-24 months", "2-4 years", "4+ years"],
)
df["voluntary_exit"] = (df["exit_type"] == "Voluntary").astype(int)


def suppressed_group_summary(data, group_cols):
    summary = (
        data.groupby(group_cols, observed=True)
            .agg(
                headcount=("employee_id", "nunique"),
                voluntary_exits=("voluntary_exit", "sum"),
                absence_days=("absence_days", "sum"),
                scheduled_days=("scheduled_days", "sum"),
            )
            .reset_index()
    )
    summary["turnover_pct"] = 100 * summary["voluntary_exits"] / summary["headcount"]
    summary["absence_pct"] = 100 * summary["absence_days"] / summary["scheduled_days"]
    summary["suppressed"] = summary["headcount"] < MIN_GROUP_SIZE
    summary.loc[summary["suppressed"], ["voluntary_exits", "turnover_pct", "absence_pct"]] = pd.NA
    return summary


overall_turnover = 100 * df["voluntary_exit"].mean()
overall_absence = 100 * df["absence_days"].sum() / df["scheduled_days"].sum()

tenure = suppressed_group_summary(df, ["tenure_band"])
tenure.to_csv(OUTPUT / "tenure_summary.csv", index=False)
segments = suppressed_group_summary(df, ["org_unit", "tenure_band", "shift"])
segments.to_csv(OUTPUT / "segment_summary.csv", index=False)

priority = segments[
    (segments["org_unit"] == "Customer Operations")
    & (segments["tenure_band"] == "Under 12 months")
    & (segments["shift"] == "Evening")
]

total_exits = df["voluntary_exit"].sum()
priority_exits = int(priority["voluntary_exits"].fillna(0).iloc[0]) if len(priority) else 0
priority_headcount = int(priority["headcount"].iloc[0]) if len(priority) else 0

print(f"Headcount: {df['employee_id'].nunique():,}")
print(f"Overall voluntary turnover: {overall_turnover:.1f}%")
print(f"Overall absence rate: {overall_absence:.1f}%")
print("\nPriority group: Customer Operations | Under 12 months | Evening")
if len(priority):
    print(priority.to_string(index=False))
    print(f"Share of exits: {100 * priority_exits / total_exits:.1f}%")
    print(f"Share of headcount: {100 * priority_headcount / len(df):.1f}%")

prevented_exits = min(12, priority_exits)
illustrative_cost_avoidance = prevented_exits * 7000
print(f"\nIllustrative cost avoidance if {prevented_exits} exits were prevented: £{illustrative_cost_avoidance:,.0f}")
print("Use aggregated trends to guide support conversations, never individual employment decisions.")
