
import pandas as pd
import geopandas as gpd
from pathlib import Path

# Project paths
project = Path(__file__).resolve().parent.parent

csv_file = project / "data" / "processed" / "merra2_temperature_2001_2020.csv"

geojson_file = project / "data" / "raw" / "boundaries" / "Tamil_Nadu_Districts.geojson"

output_folder = project / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

# 1. Read MERRA-2 CSV
print("Reading MERRA-2 dataset...")
df = pd.read_csv(csv_file)

print("Original records:", len(df))

# 2. Read Tamil Nadu district boundaries
print("\nReading district boundaries...")
districts = gpd.read_file(geojson_file)

print("Districts found:", len(districts))

if districts.crs is None:
    raise ValueError("District boundary CRS is missing.")

districts = districts.to_crs("EPSG:4326")

# 3. Convert CSV coordinates into geographic points
points = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(
        df["longitude"],
        df["latitude"]
    ),
    crs="EPSG:4326"
)

# 4. Assign grid points to district polygons
print("\nAssigning grid points to districts...")

district_data = districts[["dtname", "geometry"]]

joined = gpd.sjoin(
    points,
    district_data,
    how="left",
    predicate="within"
)

# 5. Separate matched and unmatched points
tamil_nadu = joined[joined["dtname"].notna()].copy()

unassigned = joined[joined["dtname"].isna()].copy()

# Remove spatial columns before saving
tamil_nadu = tamil_nadu.drop(
    columns=["geometry", "index_right"],
    errors="ignore"
)

unassigned = unassigned.drop(
    columns=["geometry", "index_right"],
    errors="ignore"
)

# 6. Save Tamil Nadu-only dataset
tn_file = output_folder / "merra2_temperature_tamil_nadu_2001_2020.csv"

tamil_nadu.to_csv(tn_file, index=False)

# 7. Save district-wise dataset
district_file = output_folder / "merra2_temperature_districtwise_2001_2020.csv"

tamil_nadu.to_csv(district_file, index=False)

# 8. Save unmatched grid points for inspection
unassigned_file = output_folder / "merra2_unassigned_gridpoints_2001_2020.csv"

unassigned.to_csv(unassigned_file, index=False)

# 9. Calculate district coverage
coverage = (
    tamil_nadu.groupby("dtname")
    .apply(
        lambda group: group[
            ["latitude", "longitude"]
        ].drop_duplicates().shape[0]
    )
    .reset_index(name="grid_points")
)

all_districts = pd.DataFrame({
    "dtname": districts["dtname"].unique()
})

coverage = all_districts.merge(
    coverage,
    on="dtname",
    how="left"
)

coverage["grid_points"] = coverage["grid_points"].fillna(0).astype(int)

coverage_file = output_folder / "district_grid_coverage.csv"
coverage.to_csv(coverage_file, index=False)

# 10. Display results
print("\n========== PROCESSING COMPLETED ==========")

print("Original records:", len(df))
print("Tamil Nadu records:", len(tamil_nadu))
print("Unassigned records:", len(unassigned))

print("\nDistrict grid coverage:")
print(coverage.to_string(index=False))

print("\nDistricts without grid points:")
print(
    coverage[coverage["grid_points"] == 0]["dtname"].to_list()
)

print("\nOutput files:")
print(tn_file)
print(district_file)
print(unassigned_file)
print(coverage_file)
