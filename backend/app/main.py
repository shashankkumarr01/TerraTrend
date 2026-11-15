from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import districts, coverage, trends

app = FastAPI(
    title="TerraTrend API",
    description="NASA-powered climate trend analysis for Tamil Nadu",
    version="1.0.0"
)

# Enable frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(districts.router)
app.include_router(coverage.router)
app.include_router(trends.router)

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