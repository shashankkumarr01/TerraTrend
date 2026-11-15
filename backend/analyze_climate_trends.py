
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import linregress
import pymannkendall as mk

# Project paths
project = Path(__file__).resolve().parent.parent

input_folder = project / "data" / "processed" / "districtwise"

output_folder = project / "data" / "analysis"
output_folder.mkdir(parents=True, exist_ok=True)

annual_folder = output_folder / "annual"
monthly_folder = output_folder / "monthly"

annual_folder.mkdir(exist_ok=True)
monthly_folder.mkdir(exist_ok=True)

trend_results = []

# Process each district
district_files = sorted(input_folder.glob("*.csv"))

print("District files found:", len(district_files))

for file in district_files:

    district = file.stem

    print(f"\nAnalyzing: {district}")

    df = pd.read_csv(file)

    df["time"] = pd.to_datetime(df["time"])

    # Monthly data -> annual average
    annual = (
        df.groupby(df["time"].dt.year)["temperature_c"]
        .mean()
        .reset_index(name="annual_temperature_c")
    )

    annual.rename(columns={"time": "year"}, inplace=True)
    annual.columns = ["year", "annual_temperature_c"]

    # Monthly climatology
    monthly = (
        df.groupby(df["time"].dt.month)["temperature_c"]
        .mean()
        .reset_index(name="mean_temperature_c")
    )

    monthly.rename(columns={"time": "month"}, inplace=True)
    monthly.columns = ["month", "mean_temperature_c"]

    # Temperature anomaly relative to 2001-2020 mean
    baseline = annual["annual_temperature_c"].mean()

    annual["temperature_anomaly_c"] = (
        annual["annual_temperature_c"] - baseline
    )

    # Linear trend
    slope, intercept, r_value, p_value, std_err = linregress(
        annual["year"],
        annual["annual_temperature_c"]
    )

    # Mann-Kendall test
    mk_result = mk.original_test(
        annual["annual_temperature_c"].values
    )

    # Sen's slope
    sen_slope = mk_result.slope

    trend_results.append({
        "district": district,
        "mean_temperature_c": annual["annual_temperature_c"].mean(),
        "trend_c_per_decade": slope * 10,
        "linear_p_value": p_value,
        "mann_kendall_trend": mk_result.trend,
        "mann_kendall_p_value": mk_result.p,
        "sen_slope_c_per_year": sen_slope,
        "sen_slope_c_per_decade": sen_slope * 10
    })

    # Save annual results
    annual.to_csv(
        annual_folder / f"{district}_annual.csv",
        index=False
    )

    # Save monthly climatology
    monthly.to_csv(
        monthly_folder / f"{district}_monthly.csv",
        index=False
    )

# Save overall trend summary
summary = pd.DataFrame(trend_results)

summary.to_csv(
    output_folder / "district_climate_trend_summary.csv",
    index=False
)

print("\n========== CLIMATE ANALYSIS COMPLETED ==========")

print(summary.to_string(index=False))

print("\nOutput folder:", output_folder)
