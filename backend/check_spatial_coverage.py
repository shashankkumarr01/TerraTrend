
import pandas as pd
import geopandas as gpd
import shapely
from pathlib import Path

project = Path(__file__).resolve().parent.parent

csv_file = project / "data/processed/merra2_temperature_2001_2020.csv"
geojson_file = project / "data/raw/boundaries/Tamil_Nadu_Districts.geojson"

df = pd.read_csv(csv_file)
districts = gpd.read_file(geojson_file).to_crs("EPSG:4326")

# Create unique grid coordinates
coords = df[["latitude", "longitude"]].drop_duplicates()

points = gpd.GeoDataFrame(
    coords,
    geometry=gpd.points_from_xy(
        coords["longitude"],
        coords["latitude"]
    ),
    crs="EPSG:4326"
)

# Combine all district polygons into one Tamil Nadu boundary
tn_boundary = districts.geometry.union_all()

# covers() includes points lying exactly on the boundary
inside = shapely.covers(
    tn_boundary,
    points.geometry.array
)

points["inside_tamil_nadu"] = inside

inside_points = points[points["inside_tamil_nadu"]]
outside_points = points[~points["inside_tamil_nadu"]]

print("\n========== SPATIAL DIAGNOSTICS ==========")

print("Total unique grid points:", len(points))
print("Inside Tamil Nadu:", len(inside_points))
print("Outside Tamil Nadu:", len(outside_points))

print("\nInside Tamil Nadu coordinates:")
print(inside_points[["latitude", "longitude"]].to_string(index=False))

print("\nOutside Tamil Nadu coordinates:")
print(outside_points[["latitude", "longitude"]].to_string(index=False))

# Save diagnostic results
output = project / "data/processed/spatial_diagnostic.csv"

points.drop(columns="geometry").to_csv(output, index=False)

print("\nDiagnostic file saved:", output)
