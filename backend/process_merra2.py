import xarray as xr
import pandas as pd
from pathlib import Path

# 1. Define project folders
project = Path(__file__).resolve().parent.parent

input_folder = project / "data" / "raw" / "merra2"
output_folder = project / "data" / "processed"

output_folder.mkdir(parents=True, exist_ok=True)

# 2. Find NASA NetCDF files
files = list(input_folder.glob("*.nc4"))

if not files:
    raise FileNotFoundError("No MERRA-2 files found")

file_path = files[0]

print("Processing:", file_path.name)

# 3. Open NASA dataset
with xr.open_dataset(file_path) as ds:

    if "T2M" not in ds:
        raise ValueError("T2M variable not found")

    # 4. Extract temperature
    temperature = ds["T2M"]

    # 5. Convert Kelvin to Celsius
    temperature_c = temperature - 273.15

    # 6. Convert Xarray data into a Pandas DataFrame
    df = temperature_c.to_dataframe(
        name="temperature_c"
    ).reset_index()

    # 7. Rename columns
    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude"
    })

    # 8. Add original NASA temperature values
    df["temperature_k"] = df["temperature_c"] + 273.15

    # 9. Select useful columns
    df = df[
        [
            "time",
            "latitude",
            "longitude",
            "temperature_k",
            "temperature_c"
        ]
    ]

    # 10. Remove missing temperature records
    df = df.dropna(subset=["temperature_c"])

    # 11. Save as CSV
    output_file = output_folder / "merra2_temperature_june2010.csv"

    df.to_csv(output_file, index=False)

    print("\nProcessing completed!")
    print("Total records:", len(df))
    print("Output file:", output_file)

    print("\nTemperature summary:")
    print(df["temperature_c"].describe())

import xarray as xr
import pandas as pd
from pathlib import Path

# 1. Define project folders
project = Path(__file__).resolve().parent.parent

input_folder = project / "data" / "raw" / "merra2"
output_folder = project / "data" / "processed"

output_folder.mkdir(parents=True, exist_ok=True)

# 2. Find NASA NetCDF files
files = list(input_folder.glob("*.nc4"))

if not files:
    raise FileNotFoundError("No MERRA-2 files found")

file_path = files[0]

print("Processing:", file_path.name)

# 3. Open NASA dataset
with xr.open_dataset(file_path) as ds:

    if "T2M" not in ds:
        raise ValueError("T2M variable not found")

    # 4. Extract temperature
    temperature = ds["T2M"]

    # 5. Convert Kelvin to Celsius
    temperature_c = temperature - 273.15

    # 6. Convert Xarray data into a Pandas DataFrame
    df = temperature_c.to_dataframe(
        name="temperature_c"
    ).reset_index()

    # 7. Rename columns
    df = df.rename(columns={
        "lat": "latitude",
        "lon": "longitude"
    })

    # 8. Add original NASA temperature values
    df["temperature_k"] = df["temperature_c"] + 273.15

    # 9. Select useful columns
    df = df[
        [
            "time",
            "latitude",
            "longitude",
            "temperature_k",
            "temperature_c"
        ]
    ]

    # 10. Remove missing temperature records
    df = df.dropna(subset=["temperature_c"])

    # 11. Save as CSV
    output_file = output_folder / "merra2_temperature_june2010.csv"

    df.to_csv(output_file, index=False)

    print("\nProcessing completed!")
    print("Total records:", len(df))
    print("Output file:", output_file)

    print("\nTemperature summary:")
    print(df["temperature_c"].describe())