"""Generate a reproducible synthetic workforce dataset for the People Analytics case study."""

import csv
import random
from datetime import date, timedelta

random.seed(44)
ORG_UNITS = ["Customer Operations", "Finance", "Commercial", "Technology"]
ROLES = {
    "Customer Operations": ["Customer Advisor", "Senior Advisor", "Team Coordinator"],
    "Finance": ["Finance Analyst", "Accounts Assistant", "Reporting Analyst"],
    "Commercial": ["Commercial Analyst", "Sales Support", "Pricing Analyst"],
    "Technology": ["Data Analyst", "Support Analyst", "Systems Analyst"],
}
SHIFTS = ["Day", "Evening"]


def generate(path="data/workforce.csv", employees=1240):
    year_start = date(2025, 1, 1)
    year_end = date(2025, 12, 31)
    rows = []

    for i in range(1, employees + 1):
        org = random.choices(ORG_UNITS, weights=[0.40, 0.20, 0.20, 0.20], k=1)[0]
        shift = random.choices(SHIFTS, weights=[0.70, 0.30], k=1)[0]
        role = random.choice(ROLES[org])

        if random.random() < 0.42:
            hire_date = year_start - timedelta(days=random.randint(30, 1600))
        else:
            hire_date = year_start + timedelta(days=random.randint(0, 300))

        tenure_at_year_end = max(0, (year_end - hire_date).days)
        under_12_months = tenure_at_year_end < 365

        voluntary_prob = 0.085
        if under_12_months:
            voluntary_prob += 0.065
        if org == "Customer Operations":
            voluntary_prob += 0.015
        if shift == "Evening":
            voluntary_prob += 0.015

        priority = org == "Customer Operations" and shift == "Evening" and under_12_months
        if priority:
            voluntary_prob += 0.135

        voluntary_exit = random.random() < min(voluntary_prob, 0.42)
        exit_date = ""
        exit_type = ""
        if voluntary_exit:
            earliest = max(hire_date, year_start)
            available_days = max(0, (year_end - earliest).days)
            exit_date_obj = earliest + timedelta(days=random.randint(0, available_days))
            exit_date = exit_date_obj.isoformat()
            exit_type = "Voluntary"

        scheduled_days = random.randint(205, 235)
        absence_rate = max(0, random.gauss(0.041, 0.018))
        if priority:
            absence_rate += 0.008
        absence_days = min(scheduled_days, round(scheduled_days * absence_rate))

        rows.append({
            "employee_id": f"EMP-{i:04d}",
            "org_unit": org,
            "role": role,
            "shift": shift,
            "hire_date": hire_date.isoformat(),
            "exit_date": exit_date,
            "exit_type": exit_type,
            "scheduled_days": scheduled_days,
            "absence_days": absence_days,
        })

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):,} synthetic employee records to {path}")


if __name__ == "__main__":
    generate()
