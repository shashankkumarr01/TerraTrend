
import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

# 1. Define project folders
project = Path(__file__).resolve().parent.parent

input_folder = project / "data" / "raw" / "merra2"
output_folder = project / "data" / "processed"

output_folder.mkdir(parents=True, exist_ok=True)

# 2. Find all NASA NetCDF files
files = sorted(input_folder.glob("*.nc4"))

if not files:
    raise FileNotFoundError("No MERRA-2 files found")

print("Total files found:", len(files))

all_data = []

# 3. Process every monthly file
for index, file_path in enumerate(files, start=1):

    print(f"\n[{index}/{len(files)}] Processing: {file_path.name}")

    with xr.open_dataset(file_path, engine="netcdf4") as ds:

        if "T2M" not in ds:
            raise ValueError(f"T2M variable not found: {file_path.name}")

        # 4. Extract temperature
        temperature = ds["T2M"]

        # 5. Remove invalid and missing values
        temperature = temperature.where(
            np.isfinite(temperature) & (temperature < 1e10)
        )

        # 6. Convert Kelvin to Celsius
        temperature_c = temperature - 273.15

        # 7. Convert to Pandas DataFrame
        df = temperature_c.to_dataframe(
            name="temperature_c"
        ).reset_index()

        # 8. Rename coordinate columns
        df = df.rename(columns={
            "lat": "latitude",
            "lon": "longitude"
        })

        # 9. Preserve original Kelvin values
        df["temperature_k"] = df["temperature_c"] + 273.15

        # 10. Select required columns
        df = df[
            [
                "time",
                "latitude",
                "longitude",
                "temperature_k",
                "temperature_c"
            ]
        ]

        # 11. Remove missing values
        df = df.dropna(subset=["temperature_c"])

        all_data.append(df)

# 12. Combine all monthly files
final_df = pd.concat(all_data, ignore_index=True)

# 13. Sort records
final_df = final_df.sort_values(
    ["time", "latitude", "longitude"]
).reset_index(drop=True)

# 14. Save combined CSV
output_file = output_folder / "merra2_temperature_2001_2020.csv"

final_df.to_csv(output_file, index=False)

# 15. Display results
print("\n========== PROCESSING COMPLETED ==========")

print("Files processed:", len(files))
print("Total records:", len(final_df))
print("Output file:", output_file)

print("\nTemperature summary:")
print(final_df["temperature_c"].describe())

print("\nMissing values:")
print(final_df.isna().sum())

print("\nDate range:")
print(final_df["time"].min(), "to", final_df["time"].max())
