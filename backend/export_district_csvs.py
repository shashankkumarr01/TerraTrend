
import pandas as pd
import re
from pathlib import Path

project = Path(__file__).resolve().parent.parent

input_file = (
    project / "data" / "processed" /
    "merra2_temperature_districtwise_2001_2020.csv"
)

output_folder = (
    project / "data" / "processed" / "districtwise"
)

output_folder.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

districts = sorted(df["dtname"].dropna().unique())

print("Total represented districts:", len(districts))

for district in districts:
    district_df = df[df["dtname"] == district].copy()

    filename = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        district
    ).strip("_").lower()

    output_file = output_folder / f"{filename}.csv"

    district_df.to_csv(output_file, index=False)

    print(f"Created: {filename}.csv | Records: {len(district_df)}")

print("\nDistrict CSV export completed!")
print("Output folder:", output_folder)
