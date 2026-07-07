from pathlib import Path

import pandas as pd


class EloEnricher:

    DEFAULT_ELO = 1500.0

    def __init__(self):

        elo_path = Path(
            "data/ml/features/driver_elo.parquet"
        )

        if not elo_path.exists():

            raise FileNotFoundError(

                "Driver ELO dataset not found.\n"
                "Run:\n"
                "python -m scripts.build_driver_elo_dataset"

            )

        self.elo_df = pd.read_parquet(
            elo_path
        )

    def enrich(

        self,

        dataset: pd.DataFrame,

    ) -> pd.DataFrame:

        required_columns = [

            "season",

            "event_name",

            "driver_number",

        ]

        for column in required_columns:

            if column not in dataset.columns:

                raise ValueError(

                    f"Dataset missing required column: "
                    f"{column}"

                )

        enriched = dataset.merge(

            self.elo_df,

            on=[

                "season",

                "event_name",

                "driver_number",

            ],

            how="left",

        )

        enriched["driver_elo"] = (

            enriched["driver_elo"]

            .fillna(
                self.DEFAULT_ELO
            )

            .astype(float)

        )

        return enriched

    def enrich_and_save(

        self,

        input_path: str,

        output_path: str | None = None,

    ) -> pd.DataFrame:

        df = pd.read_parquet(
            input_path
        )

        enriched = self.enrich(
            df
        )

        if output_path is None:

            output_path = input_path

        enriched.to_parquet(

            output_path,

            index=False,

        )

        return enriched