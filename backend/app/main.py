from fastapi import FastAPI

from app.routes import districts, coverage

app = FastAPI(
    title="TerraTrend API",
    description="NASA-powered climate trend analysis for Tamil Nadu",
    version="1.0.0"
)

app.include_router(districts.router)
app.include_router(coverage.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to TerraTrend",
        "status": "Backend is running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "project": "TerraTrend",
        "region": "Tamil Nadu",
        "variables": ["temperature", "precipitation"]
    }


@app.get("/api/variables")
def get_variables():
    return {
        "variables": [
            {
                "id": "temperature",
                "name": "Air Temperature",
                "unit": "degree Celsius",
                "source": "NASA MERRA-2"
            },
            {
                "id": "precipitation",
                "name": "Precipitation",
                "unit": "mm",
                "source": "NASA GPM IMERG"
            }
        ]
    }