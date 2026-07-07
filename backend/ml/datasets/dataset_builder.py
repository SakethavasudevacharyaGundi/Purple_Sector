# ml/dataset_builder.py

import pandas as pd

from ml.datasets.feature_extractor import (
    FeatureExtractor,
)


class DatasetBuilder:

    def __init__(self):

        self.extractor = FeatureExtractor()

    def build_from_replay(
        self,
        replay,
    ) -> pd.DataFrame:

        rows = []

        states = replay.states

        for state_index in range(
            len(states) - 1
        ):

            current_state = states[state_index]

            next_state = states[state_index + 1]

            next_driver_map = {

                driver.driver_number: driver

                for driver in next_state.drivers
            }

            for driver in current_state.drivers:

                future_driver = (
                    next_driver_map.get(
                        driver.driver_number
                    )
                )

                future_lap_time = None

                if future_driver:

                    future_lap_time = (
                        future_driver.last_lap_time
                    )
                current_lap_time = driver.last_lap_time
                lap_time_delta=None
                if current_lap_time is not None and future_lap_time is not None:
                    lap_time_delta = future_lap_time - current_lap_time

                row = (
                    self.extractor.extract(
                        race_state=current_state,
                        driver_state=driver,
                        future_lap_time=future_lap_time,
                        lap_time_delta=lap_time_delta,
                        season=replay.season,
                    )
                )

                rows.append(
                    row.model_dump()
                )

        return pd.DataFrame(rows)