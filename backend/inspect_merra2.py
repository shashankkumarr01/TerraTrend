
import xarray as xr
from pathlib import Path

# Locate project directory
project = Path(__file__).resolve().parent.parent

# Locate NASA data
data_folder = project / "data" / "raw" / "merra2"

files = list(data_folder.glob("*.nc4"))

if not files:
    raise FileNotFoundError("No .nc4 file found")

file_path = files[0]

# Open NASA NetCDF file
ds = xr.open_dataset(file_path)

print("NASA MERRA-2 FILE")
print(ds)

# Extract temperature
temperature = ds["T2M"]

print("\nTEMPERATURE DETAILS")
print("Shape:", temperature.shape)
print("Units:", temperature.attrs["units"])

# Convert Kelvin to Celsius
temperature_c = temperature - 273.15

print("\nTEMPERATURE STATISTICS")
print("Minimum:", float(temperature_c.min()))
print("Maximum:", float(temperature_c.max()))
print("Mean:", float(temperature_c.mean()))

ds.close()
