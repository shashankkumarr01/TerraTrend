import csv
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/trends",
    tags=["Climate Trends"]
)

# Project root: TerraTrend/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

ANNUAL_DIR = PROJECT_ROOT / "data" / "analysis" / "annual"
MONTHLY_DIR = PROJECT_ROOT / "data" / "analysis" / "monthly"


def get_district_slug(district_name: str) -> str:
    district = district_name.strip().lower()

    district_mapping = {
        "kancheepuram": "kanchipuram",
        "thoothukudi": "tuticorin",
        "tiruvarur": "thiruvarur",
        "viluppuram": "villupuram",
        "vilupuram": "villupuram",
    }

    return district_mapping.get(
        district,
        district.replace(" ", "_").replace("-", "_")
    )


def read_csv_file(file_path: Path):
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Climate data not available for this district"
        )

    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


@router.get("/{district_name}/annual")
def get_annual_trends(district_name: str):
    slug = get_district_slug(district_name)
    file_path = ANNUAL_DIR / f"{slug}_annual.csv"

    records = read_csv_file(file_path)

    return {
        "district": district_name,
        "data_type": "annual_temperature",
        "unit": "degree Celsius",
        "source": "NASA MERRA-2",
        "records": [
            {
                "year": int(row["year"]),
                "annual_temperature_c": float(row["annual_temperature_c"]),
                "temperature_anomaly_c": float(row["temperature_anomaly_c"])
            }
            for row in records
        ]
    }


@router.get("/{district_name}/monthly")
def get_monthly_trends(district_name: str):
    slug = get_district_slug(district_name)
    file_path = MONTHLY_DIR / f"{slug}_monthly.csv"

    records = read_csv_file(file_path)

    return {
        "district": district_name,
        "data_type": "monthly_climatology",
        "unit": "degree Celsius",
        "source": "NASA MERRA-2",
        "records": [
            {
                "month": int(row["month"]),
                "mean_temperature_c": float(row["mean_temperature_c"])
            }
            for row in records
        ]
    }