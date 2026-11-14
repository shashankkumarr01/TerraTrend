from fastapi import APIRouter

router = APIRouter(
    prefix="/api/coverage",
    tags=["Dataset Coverage"]
)


@router.get("/")
def get_data_coverage():

    return {
        "region": "Tamil Nadu",
        "requested_period": {
            "start_year": 2001,
            "end_year": 2024
        },
        "datasets": [
            {
                "variable": "temperature",
                "source": "NASA MERRA-2",
                "product": "M2TMNXSLV",
                "status": "pending_validation"
            },
            {
                "variable": "precipitation",
                "source": "NASA GPM IMERG",
                "status": "pending_validation"
            }
        ],
        "coverage_verified": False,
        "message": "Actual dataset files and temporal coverage "
                   "must be checked before analysis."
    }