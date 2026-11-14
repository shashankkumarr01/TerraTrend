
# TerraTrend

TerraTrend is a climate trend analysis platform built for the
NASA Space Apps Challenge 2026.

## Project Overview

The project analyzes NASA Earth science datasets to identify,
visualize, and understand long-term climate changes across
Tamil Nadu, India.

## Current Development Status

- [x] FastAPI backend setup
- [x] API endpoints implemented and tested
- [x] NASA MERRA-2 dataset integration
- [x] NetCDF-4 file inspection
- [x] Temperature extraction (T2M)
- [x] NetCDF to CSV conversion
- [x] Basic data quality validation
- [ ] Automated monthly data download
- [ ] Tamil Nadu boundary masking
- [ ] Long-term climate trend analysis
- [ ] Data visualization

## Technology Stack

- Python
- FastAPI
- Pandas
- NumPy
- Xarray
- NetCDF4

## Project Structure

```text
TerraTrend/
├── backend/
│   ├── app/
│   ├── main.py
│   ├── inspect_merra2.py
│   ├── process_merra2.py
│   └── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TerraTrend
```

Create a virtual environment:

```bash
python -m venv backend/venv
```

Activate it on Windows:

```powershell
backend\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

## NASA Dataset

TerraTrend uses NASA MERRA-2 data.

Product: M2TMNXSLV  
Variable: T2M  
Description: 2-metre air temperature  
Source: NASA GES DISC

NASA datasets are not included in this repository.
Download the required data separately and place it in:

```text
data/raw/merra2/
```

## Team

NASA Space Apps Challenge 2026  
Project: TerraTrend
