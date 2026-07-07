import pandas as pd

from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy import Strategy
from ml.simulator.model_loader import ModelLoader
from ml.elo.elo_lookup import DriverEloLookup


class OvertakeProjectionEngine:

    def __init__(self):
        self.models = ModelLoader()
        self.elo_lookup = DriverEloLookup()

    def predict_probability(
        self,
        race_state: RaceState,
        driver: DriverState,
    ) -> float:

        driver_elo = self.elo_lookup.get_driver_elo(
            season=race_state.season,
            event_name=race_state.event_name,
            driver_number=driver.driver_number,
        )

        features = pd.DataFrame([{
            "season": race_state.season,
            "event_name": race_state.event_name,
            "driver_number": driver.driver_number,
            "lap_number": race_state.lap_number,
            "position": driver.position,
            "gap_ahead": driver.gap_ahead,
            "gap_behind": driver.gap_behind,
            "gap_to_leader": driver.gap_to_leader,
            "current_compound": driver.current_compound,
            "current_tyre_age": driver.current_tyre_age,
            "stint": driver.stint,
            "track_condition": race_state.track_condition.value,
            "current_lap_time": driver.last_lap_time,
            "lap_time_delta": 0.0,
            "laps_remaining": (
                race_state.total_laps
                - race_state.lap_number
            ),
            "drs_zone": 1,
            "attack_zone": 1,
            "compound_age": str(driver.current_tyre_age),
            "driver_elo": driver_elo,
        }])

        probability = (
            self.models
            .overtake_model
            .predict_proba(features)[0][1]
        )

        return float(probability)