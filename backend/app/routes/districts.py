
from fastapi import APIRouter, HTTPException

from app.services.district_service import (
    get_all_districts,
    get_district_count
)

router = APIRouter(
    prefix="/api/districts",
    tags=["Districts"]
)


@router.get("/")
def get_districts():

    districts = get_all_districts()

    return {
        "state": "Tamil Nadu",
        "total_districts": get_district_count(),
        "districts": districts
    }


@router.get("/{district_name}")
def get_district(district_name: str):

    districts = get_all_districts()

    for district in districts:
        if district.lower() == district_name.lower():
            return {
                "district": district,
                "state": "Tamil Nadu",
                "available": True
            }

    raise HTTPException(
        status_code=404,
        detail="District not found"
    )
