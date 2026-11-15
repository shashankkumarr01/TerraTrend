
import pandas as pd
from pathlib import Path

project = Path(__file__).resolve().parent.parent

annual_folder = project / "data/analysis/annual"
monthly_folder = project / "data/analysis/monthly"

summary_file = (
    project / "data/analysis/district_climate_trend_summary.csv"
)

summary = pd.read_csv(summary_file)

print("\n========== TERRATREND DATA VALIDATION ==========")

print("\nDistricts in trend summary:", len(summary))

print("\nChecking individual district files...")

errors = []

for district in summary["district"]:

    annual_file = annual_folder / f"{district}_annual.csv"
    monthly_file = monthly_folder / f"{district}_monthly.csv"

    if not annual_file.exists() or not monthly_file.exists():
        errors.append(f"{district}: Missing output file")
        continue

    annual = pd.read_csv(annual_file)
    monthly = pd.read_csv(monthly_file)

    if len(annual) != 20:
        errors.append(f"{district}: Expected 20 annual records")

    if len(monthly) != 12:
        errors.append(f"{district}: Expected 12 monthly values")

    if annual.isna().any().any():
        errors.append(f"{district}: Missing annual values")

    if monthly.isna().any().any():
        errors.append(f"{district}: Missing monthly values")

    if annual["year"].duplicated().any():
        errors.append(f"{district}: Duplicate years")

    if set(annual["year"]) != set(range(2001, 2021)):
        errors.append(f"{district}: Incorrect year coverage")

print("\nChecking trend summary...")

if summary.isna().any().any():
    errors.append("Trend summary contains missing values")

if summary["district"].duplicated().any():
    errors.append("Duplicate districts in summary")

print("\n========== VALIDATION RESULT ==========")

if errors:
    print("Issues found:")
    for error in errors:
        print("-", error)
else:
    print("All checks passed!")
    print("Districts validated:", len(summary))
    print("Annual records per district: 20")
    print("Monthly climatology values per district: 12")

print("\nValidation completed.")

