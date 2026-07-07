from pathlib import Path

import pandas as pd

from ingestion.fastf1_client import FastF1Client


class DriverLookupBuilder:

    def build(

        self,

        start_season: int = 2018,

        end_season: int = 2024,

    ) -> pd.DataFrame:

        client = FastF1Client()

        lookup = {}

        for season in range(

            start_season,

            end_season + 1,

        ):

            print()
            print(f"Season {season}")

            schedule = client.get_schedule(
                season
            )

            for _, event in schedule.iterrows():

                if (

                    event["EventFormat"]

                    !=

                    "conventional"

                ):

                    continue

                event_name = str(
                    event["EventName"]
                )

                print(
                    f"  {event_name}"
                )

                session = client.get_session(

                    season,

                    event_name,

                    "R",

                )

                results = session.results

                for _, row in results.iterrows():

                    driver_number = str(
                        row["DriverNumber"]
                    )

                    driver_name = str(
                        row["FullName"]
                    )

                    canonical_number = driver_number

                    if (

                        season >= 2021

                        and

                        driver_number == "1"

                    ):

                        canonical_number = "33"

                    lookup[
                        driver_number
                    ] = {

                        "driver_number":
                        driver_number,

                        "driver_name":
                        driver_name,

                        "canonical_driver_number":
                        canonical_number,

                    }

        return (

            pd.DataFrame(

                lookup.values()

            )

            .sort_values(

                "driver_number"

            )

            .reset_index(

                drop=True

            )

        )

    def save(

        self,

        output_path: str =

        "data/ml/features/driver_lookup.parquet",

    ) -> None:

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

        print(df)


if __name__ == "__main__":

    DriverLookupBuilder().save()