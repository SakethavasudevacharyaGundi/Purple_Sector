from pathlib import Path

import pandas as pd

from ml.elo.elo_calculator import (
    EloCalculator,
)


def main():

    print()
    print(
        "Loading master dataset..."
    )

    df = pd.read_parquet(
        "data/ml/v1/master_dataset.parquet"
    )

    schedule_df = pd.read_parquet(
        "data/ml/features/race_schedule.parquet"
    )

    race_results = (

        df

        .sort_values(

            [

                "season",

                "event_name",

                "lap_number",

            ]

        )

        .groupby(

            [

                "season",

                "event_name",

                "driver_number",

            ],

            as_index=False,

        )

        .last()

        [

            [

                "season",

                "event_name",

                "driver_number",

                "position",

            ]

        ]

    )

    race_results = race_results.rename(

        columns={

            "driver_number":
            "DriverNumber",

            "position":
            "Position",

        }

    )

    race_results = (

        race_results.merge(

            schedule_df,

            on=[

                "season",

                "event_name",

            ],

            how="left",

        )

    )

    missing_rounds = (

        race_results[
            "round_number"
        ]

        .isna()

        .sum()

    )

    if missing_rounds > 0:

        raise ValueError(

            f"{missing_rounds} races "

            f"are missing round numbers."

        )

    race_results = (

        race_results.sort_values(

            [

                "season",

                "round_number",

                "Position",

            ]

        )

    )

    elo_calculator = (
        EloCalculator()
    )

    driver_elo_df = (

        elo_calculator
        .build_driver_elos(

            race_results

        )

    )

    output_dir = Path(
        "data/ml/features"
    )

    output_dir.mkdir(

        parents=True,

        exist_ok=True,

    )

    output_file = (

        output_dir

        /

        "driver_elo.parquet"

    )

    driver_elo_df.to_parquet(

        output_file,

        index=False,

    )

    print()
    print(
        f"Saved: {output_file}"
    )

    print()

    print(

        driver_elo_df.tail(20)

    )


if __name__ == "__main__":

    main()