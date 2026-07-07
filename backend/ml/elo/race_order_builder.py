from pathlib import Path

import pandas as pd

from ingestion.fastf1_client import (
    FastF1Client,
)


class RaceOrderBuilder:

    def build(

        self,

        start_season: int = 2018,

        end_season: int = 2024,

    ) -> pd.DataFrame:

        client = FastF1Client()

        rows = []

        for season in range(

            start_season,

            end_season + 1,

        ):

            schedule = (
                client.get_schedule(
                    season
                )
            )

            for _, row in schedule.iterrows():

                if (
                    row["EventFormat"]
                    !=
                    "conventional"
                ):
                    continue

                rows.append(
                    {
                        "season":
                        season,

                        "event_name":
                        str(
                            row[
                                "EventName"
                            ]
                        ),

                        "round_number":
                        int(
                            row[
                                "RoundNumber"
                            ]
                        ),
                    }
                )

        return pd.DataFrame(
            rows
        )

    def save(

        self,

        output_path:
        str =
        "data/ml/features/race_schedule.parquet",

    ):

        df = self.build()

        output = Path(
            output_path
        )

        output.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        df.to_parquet(

            output,

            index=False,

        )

        print()
        print(
            f"Saved {output}"
        )
        print()

        print(
            df.head()
        )