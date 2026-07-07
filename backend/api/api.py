from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from pathlib import Path

from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy import Strategy
from ml.simulator.strategy_simulator import (
    StrategySimulator,
)

from ml.monte_carlo.monte_carlo_simulator import (
    MonteCarloSimulator,
)

from ml.backtesting.historical_state_factory import HistoricalStateFactory

app = FastAPI(
    title="Purple Sector API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

strategy_simulator = StrategySimulator()
monte_carlo_simulator = MonteCarloSimulator()
state_factory = HistoricalStateFactory()

# Mapping for 3-letter acronym to driver number (temporary fix, should be dynamic)
DRIVER_MAP = {
    "NOR": "4",
    "VER": "1",
    "HAM": "44",
    "LEC": "16",
    "SAI": "55",
    "RUS": "63",
    "PIA": "81",
    "PER": "11",
    "ALO": "14",
    "STR": "18"
}

class SetupRequest(BaseModel):
    season: int
    gp: str
    lap: int
    driver: str

@app.get("/health")
def health():
    return {"status": "healthy"}

# Extended Driver Info Map for ELO endpoint
DRIVER_INFO = {
    4: ("NOR", "McLaren"),
    33: ("VER", "Red Bull Racing"),
    44: ("HAM", "Mercedes"),
    16: ("LEC", "Ferrari"),
    55: ("SAI", "Ferrari"),
    63: ("RUS", "Mercedes"),
    81: ("PIA", "McLaren"),
    11: ("PER", "Red Bull Racing"),
    14: ("ALO", "Aston Martin"),
    18: ("STR", "Aston Martin"),
    22: ("TSU", "RB"),
    23: ("ALB", "Williams"),
    24: ("ZHO", "Kick Sauber"),
    20: ("MAG", "Haas"),
    27: ("HUL", "Haas"),
    77: ("BOT", "Kick Sauber"),
    30: ("LAW", "RB"),
    10: ("GAS", "Alpine"),
    43: ("COL", "Williams"),
    7: ("DOO", "Alpine"),
    1: ("VER", "Red Bull Racing"),
}

@app.get("/elo")
def get_elo_rankings():
    elo_file = Path("data/ml/features/driver_elo.parquet")
    if not elo_file.exists():
        return {"error": "Elo data not found"}
        
    df = pd.read_parquet(elo_file)
    latest_season = df["season"].max()
    latest_df = df[df["season"] == latest_season]
    latest_round = latest_df["round_number"].max()
    
    current_elo_df = latest_df[latest_df["round_number"] == latest_round]
    
    # Sort by elo descending
    sorted_df = current_elo_df.sort_values("driver_elo", ascending=False)
    
    rankings = []
    for _, row in sorted_df.iterrows():
        driver_num = int(row["canonical_driver_number"])
        driver_name = str(row["driver_name"]).replace('\ufffd', 'e') # Handle weird encoding like Pérez
        
        info = DRIVER_INFO.get(driver_num, ("UNK", "Unknown"))
        driver_id = info[0]
        team = info[1]
        
        rankings.append({
            "id": driver_id,
            "name": driver_name,
            "team": team,
            "elo": int(row["driver_elo"]),
            "trend": "same" # Keeping mock trend as requested in plan
        })
        
    return rankings
import glob
from fastapi import HTTPException

@app.get("/metadata/seasons")
def get_seasons():
    season_files = Path("data/ml/v1/seasons").glob("season_*.parquet")
    seasons = []
    for f in season_files:
        try:
            year = int(f.stem.split("_")[1])
            seasons.append(year)
        except ValueError:
            pass
    return sorted(seasons, reverse=True)

@app.get("/metadata/{season}")
def get_season_metadata(season: int):
    season_file = Path(f"data/ml/v1/seasons/season_{season}.parquet")
    if not season_file.exists():
        raise HTTPException(status_code=404, detail=f"Season {season} data not found")
        
    df = pd.read_parquet(season_file)
    
    # Get max laps per event
    max_laps = df.groupby("event_name")["lap_number"].max().to_dict()
    
    # Get unique driver numbers that appear in this season
    driver_nums = df["driver_number"].unique()
    
    # Filter only drivers we can map
    drivers_list = []
    for d_num in driver_nums:
        try:
            d = int(d_num)
            if d in DRIVER_INFO:
                drivers_list.append({
                    "id": DRIVER_INFO[d][0],
                    "name": DRIVER_INFO[d][0] + " - " + DRIVER_INFO[d][1]
                })
        except ValueError:
            pass

    return {
        "season": season,
        "events": [{"name": k, "max_laps": int(v)} for k, v in max_laps.items()],
        "drivers": drivers_list
    }

@app.post("/setup")
def setup_race(request: SetupRequest):
    driver_num = DRIVER_MAP.get(request.driver, "4")
    
    # Load dataset for the season
    season_file = Path(f"data/ml/v1/seasons/season_{request.season}.parquet")
    if not season_file.exists():
        raise HTTPException(status_code=400, detail=f"Season {request.season} data not found.")
        
    df = pd.read_parquet(season_file)
    
    # Exact match on event name is better if we have metadata
    race_df = df[df['event_name'] == request.gp]
    
    if race_df.empty:
        # Fallback to substring match for backwards compatibility
        race_df = df[df['event_name'].str.contains(request.gp.split(' ')[0], case=False, na=False)]
        if race_df.empty:
            raise HTTPException(status_code=400, detail=f"Race {request.gp} not found in {request.season}.")
        
    try:
        race_state, _ = state_factory.build(race_df, driver_num, request.lap)
        # Ensure the driver actually exists in this state
        if not any(d.driver_number == driver_num for d in race_state.drivers):
            raise HTTPException(status_code=400, detail=f"Driver {request.driver} not found in lap {request.lap}. They may have retired.")
        return race_state
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to build race state: {str(e)}")


@app.post("/simulate")
def simulate(
    race_state: RaceState,
    driver: DriverState,
    strategy: Strategy,
):
    return strategy_simulator.simulate(
        race_state,
        driver,
        strategy,
    )


@app.post("/simulate/components")
def simulate_components(
    race_state: RaceState,
    driver: DriverState,
    strategy: Strategy,
):
    return strategy_simulator.simulate_components(
        race_state,
        driver,
        strategy,
    )


@app.post("/monte-carlo")
def monte_carlo(
    race_state: RaceState,
    driver: DriverState,
    strategy: Strategy,
    runs: int = 1000,
):
    return monte_carlo_simulator.simulate(
        race_state,
        driver,
        strategy,
        runs,
    )


class CustomSimulateRequest(BaseModel):
    race_state: RaceState
    driver: DriverState
    pit_lap: int
    next_compound: str

@app.post("/simulate/custom")
def simulate_custom(request: CustomSimulateRequest):
    try:
        strategy = Strategy(
            pit_lap=request.pit_lap,
            next_compound=request.next_compound
        )
        
        # 1. Run Strategy Components to get Time Losses
        components = strategy_simulator.simulate_components(request.race_state, request.driver, strategy)
        
        pit_loss = components.pit_loss
        traffic_loss = components.traffic_loss
        deg_loss = components.degradation_seconds
        
        # 2. Run Monte Carlo with 100 runs for custom sim
        mc_result = monte_carlo_simulator.simulate(request.race_state, request.driver, strategy, runs=100)
        
        # 3. Format for UI
        distribution = [
            {"position": "P1", "probability": round(mc_result.win_probability * 100)},
            {"position": "P2", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 2), 0)},
            {"position": "P3", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 3), 0)},
            {"position": "P4", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 4), 0)},
            {"position": "P5", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 5), 0)},
            {"position": "P6+", "probability": sum(d.probability * 100 for d in mc_result.distributions if d.position > 5)},
        ]
        
        return {
            "pitLap": strategy.pit_lap,
            "compound": strategy.next_compound,
            "expectedFinish": f"P{int(mc_result.expected_finish_position)}",
            "medianPosition": int(mc_result.median_finish_position),
            "stdDev": round(mc_result.finish_position_std, 1),
            "winProb": round(mc_result.win_probability * 100),
            "podiumProb": round(mc_result.podium_probability * 100),
            "pointsProb": round(mc_result.points_probability * 100),
            "pitLoss": f"{pit_loss:.1f}s",
            "trafficLoss": f"{traffic_loss:.1f}s",
            "degLoss": f"{deg_loss:.1f}s",
            "expectedOvertakes": round(components.expected_overtakes, 1),
            "rejoinPosition": f"P{int(components.rejoin_position)}",
            "distribution": distribution
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate custom simulation: {str(e)}")


from ml.recommendation.recommendation_engine import RecommendationEngine
recommendation_engine = RecommendationEngine()

class RecommendRequest(BaseModel):
    race_state: RaceState
    driver: DriverState

@app.post("/recommend")
def recommend_strategies(request: RecommendRequest):
    try:
        # This endpoint mimics what RecommendationEngine does, but returns top 3 for the UI
        strategies = recommendation_engine.strategy_evaluator.evaluate(request.race_state, request.driver)
        
        if not strategies:
            raise HTTPException(status_code=400, detail="No viable strategies found for this driver at this lap.")
            
        results = []
        
        # Evaluate top 3 candidates to save time (Monte carlo is expensive)
        for i, candidate in enumerate(strategies[:3]):
            strategy = candidate["strategy"]
            
            # 1. Run Strategy Components to get Time Losses
            components = strategy_simulator.simulate_components(request.race_state, request.driver, strategy)
            
            pit_loss = components.pit_loss
            traffic_loss = components.traffic_loss
            deg_loss = components.degradation_seconds
            
            # 2. Run Monte Carlo with 50 runs
            mc_result = monte_carlo_simulator.simulate(request.race_state, request.driver, strategy, runs=50)
            
            # 3. Format for UI
            distribution = [
                {"position": "P1", "probability": round(mc_result.win_probability * 100)},
                {"position": "P2", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 2), 0)},
                {"position": "P3", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 3), 0)},
                {"position": "P4", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 4), 0)},
                {"position": "P5", "probability": next((d.probability * 100 for d in mc_result.distributions if d.position == 5), 0)},
                {"position": "P6+", "probability": sum(d.probability * 100 for d in mc_result.distributions if d.position > 5)},
            ]
            
            results.append({
                "rank": i + 1,
                "pitLap": strategy.pit_lap,
                "compound": strategy.next_compound,
                "expectedFinish": f"P{int(mc_result.expected_finish_position)}",
                "winProb": round(mc_result.win_probability * 100),
                "podiumProb": round(mc_result.podium_probability * 100),
                "pointsProb": round(mc_result.points_probability * 100),
                "pitLoss": f"{pit_loss:.1f}s",
                "trafficLoss": f"{traffic_loss:.1f}s",
                "degLoss": f"{deg_loss:.1f}s",
                # Determine color based on rank for UI
                "color": ["bg-purple-500", "bg-rose-500", "bg-blue-500"][i],
                "textColor": ["text-purple-400", "text-rose-400", "text-blue-400"][i],
                "borderColor": ["border-purple-500/50", "border-rose-500/50", "border-blue-500/50"][i],
                "distribution": distribution
            })
            
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate recommendations: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )