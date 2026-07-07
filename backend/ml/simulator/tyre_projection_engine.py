import pandas as pd

from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy import Strategy
from ml.simulator.model_loader import ModelLoader


class TyreProjectionEngine:

    def __init__(self):

        self.models = (
            ModelLoader()
        )

    def project(

        self,

        race_state: RaceState,

        driver: DriverState,

        strategy: Strategy,

    ) -> float:

        laps_remaining = (

            race_state.total_laps
            -
            strategy.pit_lap

        )

        total_degradation = 0.0

        tyre_age = 1

        for lap_offset in range(

            laps_remaining

        ):

            features = pd.DataFrame(
                [
                    {
                        "season": 2024,

                        "circuit_name":
                        race_state.event_name,

                        "driver_number":
                        driver.driver_number,

                        "current_compound":
                        strategy.next_compound,

                        "current_tyre_age":
                        tyre_age,

                        "lap_in_stint":
                        tyre_age,

                        "lap_number":
                        strategy.pit_lap
                        +
                        lap_offset,

                        "laps_remaining":
                        laps_remaining
                        -
                        lap_offset,

                        "stint":
                        (
                            driver.stint
                            or 1
                        )
                        +
                        1,

                        "position":
                        driver.position,

                        "gap_ahead":
                        driver.gap_ahead,

                        "gap_behind":
                        driver.gap_behind,

                        "gap_to_leader":
                        driver.gap_to_leader,

                        "track_temp":
                        race_state.track_temp,

                        "air_temp":
                        race_state.air_temp,

                        "rainfall":
                        int(
                            race_state.rainfall
                        ),

                        "baseline_pace":
                        90.0,

                        "race_progress":
                        (
                            strategy.pit_lap
                            +
                            lap_offset
                        )
                        /
                        race_state.total_laps,

                        "tyre_life_ratio":
                        tyre_age
                        /
                        max(
                            tyre_age
                            +
                            laps_remaining,
                            1,
                        ),
                    }
                ]
            )

            degradation = float(

                self.models
                .tyre_model
                .predict(
                    features
                )[0]

            )

            total_degradation += max(
                degradation,
                0.0,
            )

            tyre_age += 1

        total_degradation = round(
            total_degradation,
            2,
        )



        return total_degradation