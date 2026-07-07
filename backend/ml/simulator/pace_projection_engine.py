import pandas as pd

from domain.race_state import (
    RaceState,
)

from domain.driver_state import (
    DriverState,
)

from ml.simulator.strategy import (
    Strategy,
)

from ml.simulator.model_loader import (
    ModelLoader,
)


class PaceProjectionEngine:

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

        total_lap_time = 0.0

        tyre_age = 1

        for _ in range(
            laps_remaining
        ):

            features = pd.DataFrame(
                [
                    {
                        "season": 2024,

                        "event_name":
                        race_state.event_name,

                        "driver_number":
                        driver.driver_number,

                        "lap_number":
                        strategy.pit_lap
                        +
                        tyre_age,

                        "current_compound":
                        strategy.next_compound,

                        "current_tyre_age":
                        tyre_age,

                        "track_temp":
                        race_state.track_temp,

                        "air_temp":
                        race_state.air_temp,

                        "rainfall":
                        int(
                            race_state.rainfall
                        ),

                        "track_condition":
                        race_state.track_condition.value,

                        "position":
                        driver.position,

                        "gap_ahead":
                        driver.gap_ahead,

                        "gap_behind":
                        driver.gap_behind,

                        "gap_to_leader":
                        driver.gap_to_leader,

                        "stint":
                        (
                            driver.stint
                            + 1
                        ),
                    }
                ]
            )

            lap_time = float(

                self.models
                .pace_model
                .predict(
                    features
                )[0]

            )

            total_lap_time += (
                lap_time
            )

            tyre_age += 1

        return (
            total_lap_time
            /
            max(
                laps_remaining,
                1,
            )
        )