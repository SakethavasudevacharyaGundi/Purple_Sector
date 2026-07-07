from pathlib import Path

import pandas as pd


class DriverEloLookup:

    DEFAULT_ELO = 1500.0

    def __init__(self):

        elo_df = pd.read_parquet(

            Path(
                "data/ml/features/driver_elo.parquet"
            )

        )

        self.lookup = {

            (

                int(row.season),

                str(row.event_name),

                str(row.display_number),

            ): float(

                row.driver_elo

            )

            for row in elo_df.itertuples()

        }

    def get_driver_elo(

        self,

        season: int,

        event_name: str,

        driver_number: str,

    ) -> float:

        return self.lookup.get(

            (

                int(season),

                str(event_name),

                str(driver_number),

            ),

            self.DEFAULT_ELO,

        )