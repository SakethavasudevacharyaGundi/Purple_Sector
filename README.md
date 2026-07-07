<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg" alt="F1 Logo" width="120" />
  <h1>Purple Sector 🏎️</h1>
  <p><strong>Advanced Formula 1 Strategy Analytics & Race Simulation Platform</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript%20%7C%20Vite-61DAFB?style=for-the-badge&logo=react" alt="Frontend" />
    <img src="https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python-009688?style=for-the-badge&logo=fastapi" alt="Backend" />
    <img src="https://img.shields.io/badge/ML%20Engine-CatBoost%20%7C%20FastF1-FFCC00?style=for-the-badge" alt="Machine Learning" />
    <img src="https://img.shields.io/badge/Data-Parquet-000000?style=for-the-badge" alt="Data" />
  </p>
</div>

<br />

## Overview

**Purple Sector** is a full-stack, AI-driven web application that predicts and analyzes Formula 1 race strategies using Machine Learning. It enables users to run Monte Carlo race simulations, compare pit-stop strategies, visualize race-pace degradation, and gain data-driven insights powered by historical Formula 1 telemetry.

The platform bridges a highly responsive, modern React frontend with a high-performance FastAPI backend, utilizing CatBoost decision trees to accurately model tyre degradation, pit loss, traffic impact, and overtake probabilities.

---

## Features

* **Monte Carlo Race Simulation:** Simulate thousands of race scenarios to calculate exact probabilities for points, podiums, and race wins.
* **AI Strategy Recommendation Engine:** Automatically calculates the mathematically optimal pit lap and tyre compound selection.
* **Dynamic Elo Ranking System:** Real-time driver and team performance tracking over multiple seasons.
* **Granular Race Analytics:** Predicts tyre degradation (soft, medium, hard), traffic loss, pit-lane time loss, and rejoin positions.
* **Modern UI/UX:** Responsive React dashboard built with Tailwind CSS, Lucide Icons, and interactive charts.
* **High-Performance Backend:** Asynchronous FastAPI backend powered by compressed Parquet datasets for lightning-fast inference.

---

## Tech Stack

### Frontend
* **Core:** React 19, TypeScript, Vite
* **Styling & UI:** Tailwind CSS, Shadcn UI components, Lucide React (Icons)
* **Animation & Rendering:** GSAP, Face-api.js, Postprocessing

### Backend
* **Core:** FastAPI, Uvicorn, Python 3.11+
* **Data Processing:** Pandas, PyArrow, NumPy

### Machine Learning & Data Pipeline
* **Telemetry Extraction:** FastF1
* **Models:** CatBoost (Regressor & Classifier), Scikit-learn
* **Storage:** Apache Parquet databases (`.parquet`) and Compiled CatBoost Models (`.cbm`)

---

## Project Structure

```text
Purple_Sector/
│
├── frontend/                     # React Frontend application
│   ├── src/
│   │   ├── components/           # UI Components (Sidebar, Cards, Tabs)
│   │   ├── pages/                # LandingPage, Dashboard, Simulation, EloRanking
│   │   └── lib/                  # API clients and utility functions
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                      # FastAPI & ML Backend
│   ├── api/                      # REST API Endpoints (api.py)
│   ├── ml/                       # Machine Learning Engines
│   │   ├── simulator/            # Strategy & Overtake Simulation
│   │   ├── monte_carlo/          # Probability Distribution Engine
│   │   ├── pace/                 # Pace & Tyre Degradation Prediction
│   │   └── recommendation/       # Optimal Strategy Evaluator
│   ├── scripts/                  # Data Pipeline & Model Training Scripts
│   ├── data/                     # Parquet Datasets & .cbm Models
│   └── requirements.txt          # Python Dependencies
│
└── .gitignore
```

---

## The Machine Learning Pipeline

Purple Sector does not just guess strategies—it learns them. The backend data pipeline operates in several automated phases:

1. **Telemetry Ingestion:** The `scripts/` directory uses the **FastF1** API to scrape raw telemetry, timing data, and track states from the official Formula 1 timing servers.
2. **Feature Engineering:** Data is cleaned and transformed into highly specific DataFrames (Pace, Pit Loss, Overtakes, Traffic, Rejoin Position).
3. **Model Training:** Five distinct **CatBoost** models are trained:
   * `tyre_model.cbm`: Predicts degradation per lap based on compound and track temperature.
   * `pit_loss_model.cbm`: Calculates exact time lost in the pit lane for specific circuits.
   * `traffic_loss_model.cbm`: Models time lost behind slower cars after pitting.
   * `rejoin_position_model.cbm`: Predicts track position post-pitstop.
   * `overtake_model.cbm`: Classifies the probability of successfully passing a car.
4. **Data Compilation:** Historical data is compressed into ultra-lightweight `.parquet` databases.
5. **Inference (Live):** FastAPI loads the `.parquet` datasets and utilizes a Singleton `ModelLoader` to efficiently evaluate thousands of Monte Carlo simulations in milliseconds when a user requests a strategy.

---

## Installation & Setup

### Clone the Repository
```bash
git clone https://github.com/SakethavasudevacharyaGundi/Purple_Sector.git
cd Purple_Sector
```

### Backend Setup (API)
Create and activate a Python virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

Install the backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Start the FastAPI server:
```bash
uvicorn api.api:app --reload
```
*The backend will now be running on `http://127.0.0.1:8000`*

### Frontend Setup (UI)
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm install
```

Start the Vite development server:
```bash
npm run dev
```
*The frontend will now be running on `http://localhost:5173`*

---

## Environment Variables

**Frontend (`frontend/.env`)**
```env
VITE_API_BASE_URL=http://localhost:8000
```

**Backend**
```env
PORT=8000
```

---

## API Endpoints

Purple Sector exposes a rich REST API for F1 data access:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/v1/seasons` | List all available historical seasons |
| **GET** | `/api/v1/seasons/{year}` | Retrieve race schedule for a specific year |
| **GET** | `/api/v1/events/{year}/{event}/setup` | Get initial grid and race states for simulation |
| **POST** | `/api/v1/events/{year}/{event}/simulate` | Run a strategy through the ML simulators |
| **POST** | `/api/v1/events/{year}/{event}/recommend` | Let the AI calculate the mathematically optimal pit strategy |
| **GET** | `/api/v1/elo/driver/{driver_name}` | Get historical Elo ratings for a specific driver |
| **GET** | `/api/v1/elo/team/{team_name}` | Get historical Elo ratings for a specific constructor |

---

## Author

**Sakethavasudev**  
Developed as an advanced Machine Learning and Full Stack Analytics project demonstrating predictive modeling, complex backend API architecture, and interactive, high-performance data visualization.

---

<div align="center">
  <i>Developed for the love of motorsport and data.</i>
</div>
