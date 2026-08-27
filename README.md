# People Analytics Case Study

## First-Year Turnover, Responsible Workforce Insight and Retention Support
![People Analytics portfolio cover](Ehsaan-Khan-People-Analytics-Cover.png)

This independent portfolio project examines where the first-year employee experience may need additional support and how aggregated workforce data can guide a fair, testable retention response.

[**View the complete People Analytics case study (PDF)**](Ehsaan-Khan-People-Analytics-Case-Study.pdf)

> **Portfolio disclosure:** This project uses entirely synthetic workforce data and contains no employer or employee information. Financial benefits are illustrative planning scenarios, not realised outcomes.

## Technical Project Layer

This repository includes a reproducible Python workflow designed around responsible workforce analytics.

- `data/generate_workforce_data.py` — creates 1,240 reproducible synthetic employee records without protected characteristics.
- `python/people_analysis.py` — validates data, creates tenure and segment summaries, calculates turnover and absence metrics, and suppresses small groups.
- `requirements.txt` — Python dependency list.
- `outputs/` is created automatically when the analysis runs.

The generated dataset produces approximately 14% voluntary turnover and ~4.2% absence, with the intended priority group—Customer Operations → Under 12 Months → Evening—showing materially higher turnover than the overall workforce.

## Business Question

**Which workforce groups are contributing most strongly to avoidable turnover, and where should retention action begin without applying a blanket policy?**

The intended audience is people leadership, operations and workforce planning.

## Python Techniques Demonstrated

- `pandas` data loading and date handling
- Tenure-band creation with `pd.cut`
- Grouped aggregations
- Reusable analytical functions
- Data-validation assertions
- Privacy suppression for small groups
- CSV output generation
- Business scenario modelling

## Responsible Analytics Safeguards

- No protected characteristics are generated or analysed.
- Results are aggregated before interpretation.
- Groups below 25 employees are suppressed.
- No individual employee risk scores are created.
- The analysis is intended to guide support conversations, not individual employment decisions.
- Human review remains essential before any intervention.

## Key Business Finding

The strongest signal appears among first-year employees working evening shifts in Customer Operations. The appropriate response is therefore a focused onboarding and manager-support pilot rather than an employee-level predictive model or blanket retention policy.

## Recommended 90-Day Support Pilot

| Stage | Proposed action |
| --- | --- |
| Day 0 | Confirm role and shift expectations |
| Day 30 | Hold a structured manager check-in |
| Day 60 | Conduct a stay conversation |
| Day 90 | Review the pattern and adapt support |

## How to Run

1. Install dependencies with `pip install -r requirements.txt`.
2. Run `python data/generate_workforce_data.py`.
3. Run `python python/people_analysis.py`.
4. Inspect `outputs/tenure_summary.csv` and `outputs/segment_summary.csv`.

## Working Style

I use AI assistance where appropriate to accelerate technical implementation, while retaining ownership of the business question, analytical logic, validation, interpretation and communication of results.

**Protect privacy → Validate the data → Find the aggregated signal → Focus support → Measure before scaling**
