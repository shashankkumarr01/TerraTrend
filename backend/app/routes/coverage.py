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
            "end_year": 2020
        },

        "datasets": [
            {
                "variable": "temperature",
                "source": "NASA MERRA-2",
                "product": "M2TMNXSLV",
                "status": "partially_available",
                "real_data_districts": 30,
                "dummy_data_districts": 8,
                "total_districts": 38,
                "details": (
                    "30 districts have processed NASA MERRA-2 "
                    "temperature data. 8 districts contain "
                    "dummy test data."
                )
            },
            {
                "variable": "precipitation",
                "source": "NASA GPM IMERG",
                "status": "integration_pending",
                "details": (
                    "Precipitation data integration is pending."
                )
            }
        ],

        "coverage_verified": False,

        "message": (
            "Temperature data is available for dashboard "
            "testing. Independent scientific validation is "
            "still pending. Dummy test data is clearly "
            "separated from NASA-derived data."
        )
    }