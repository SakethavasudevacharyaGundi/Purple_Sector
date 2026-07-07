import pandas as pd

from ml.simulator.strategy import (
    Strategy,
)


class StrategyExtractor:

    def extract(

        self,

        race_df: pd.DataFrame,

        driver_number: str,

        state_lap: int,

    ) -> Strategy | None:

        driver_df = race_df[

            race_df[
                "driver_number"
            ].astype(str)

            ==

            str(driver_number)

        ].sort_values(
            "lap_number"
        )

        future_rows = driver_df[

            driver_df[
                "lap_number"
            ]
            >
            state_lap

        ]

        pit_rows = future_rows[

            future_rows[
                "pit_in_time_seconds"
            ].notna()

        ]

        if pit_rows.empty:

            return None

        pit_lap = int(

            pit_rows.iloc[0][
                "lap_number"
            ]

        )

        post_pit_rows = future_rows[

            future_rows[
                "lap_number"
            ]
            >
            pit_lap

        ]

        if post_pit_rows.empty:

            return None

        next_compound = str(

            post_pit_rows.iloc[0][
                "current_compound"
            ]

        )

        return Strategy(

            pit_lap=pit_lap,

            next_compound=
            next_compound,
        )