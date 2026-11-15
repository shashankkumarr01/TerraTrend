# 🌍 TerraTrend

### Exploring Climate Trends Across Tamil Nadu Using NASA Earth Science Data

TerraTrend is an interactive climate data analysis and visualization platform developed for the **NASA Space Apps Challenge 2026**.

The platform uses NASA Earth science datasets to explore historical climate patterns across Tamil Nadu, India, through interactive geographical maps, district-level analysis and data visualizations.

## 🚀 Key Features

- **Interactive Tamil Nadu Map:** Explore climate information across Tamil Nadu districts.
- **Annual Climate Trends:** Analyze historical climate patterns over multiple years.
- **Monthly Climate Analysis:** Explore monthly variations in climate data.
- **District Comparison:** Compare climate trends between different districts.
- **Dataset Coverage:** View available data coverage across districts and time periods.
- **Interactive Dashboard:** Visualize climate information through charts and geographical representations.
- **REST API:** Retrieve processed climate data through FastAPI endpoints.

## 🛰️ NASA Data Source

TerraTrend uses NASA's MERRA-2 (Modern-Era Retrospective Analysis for Research and Applications, Version 2) dataset.

| Parameter | Details |
|---|---|
| Dataset | MERRA-2 |
| Product | M2TMNXSLV |
| Variable | T2M |
| Description | 2-metre air temperature |
| Provider | NASA |
| Data Portal | NASA GES DISC |

Data portal: https://disc.gsfc.nasa.gov/

## 🛠️ Technology Stack

### Frontend
- React.js
- JavaScript
- CSS
- Recharts
- React Leaflet
- Leaflet

### Backend
- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Xarray
- NetCDF4

### Data Processing
- NASA MERRA-2
- NetCDF-4
- CSV datasets
- Python data processing scripts

## 📁 Project Structure

```text
TerraTrend/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── coverage.py
│   │   │   └── trends.py
│   │   └── main.py
│   │
│   ├── analyze_climate_trends.py
│   ├── check_spatial_coverage.py
│   ├── export_district_csvs.py
│   ├── process_districtwise.py
│   ├── process_merra2.py
│   ├── validate_climate_data.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
│
├── data/
│   └── analysis/
│       ├── annual/
│       └── monthly/
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/shashankkumarr01/TerraTrend.git

cd TerraTrend
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open the local URL displayed in your terminal.

## 🔗 API Endpoints

The backend provides REST APIs for climate data exploration.

| Endpoint | Purpose |
|---|---|
| `/api/coverage/` | Retrieve dataset coverage information |
| Trends endpoints | Retrieve annual, monthly and comparison data |

For the complete available endpoint list, visit:

http://127.0.0.1:8000/docs

## 🎯 Project Objective

TerraTrend aims to make complex Earth science datasets easier to understand by transforming historical climate information into accessible geographical and statistical visualizations.

By connecting NASA Earth science data with district-level exploration, the platform helps users investigate climate patterns across Tamil Nadu.

## 👥 Team

**Team Vibe Coders 001**

Developed for the NASA Space Apps Challenge 2026.

## 📜 Acknowledgements

- NASA Earth Science
- NASA MERRA-2
- NASA GES DISC
- NASA Space Apps Challenge 2026