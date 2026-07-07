import pandas as pd


class PaceTargetBuilder:

    def build(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        working_df = df.copy()

        required = [
            "fuel_corrected_lap_time",
            "baseline_pace",
        ]

        working_df = working_df.dropna(
            subset=required
        )

        working_df[
            "pace_delta"
        ] = (
            working_df[
                "fuel_corrected_lap_time"
            ]
            -
            working_df[
                "baseline_pace"
            ]
        )

        working_df = working_df[
            working_df[
                "pace_delta"
            ].between(
                -2,
                8,
            )
        ]

        print()
        print(  
            "PACE DELTA DATASET"
        )

        print(
            working_df.shape
        )

        print()

        print(
            working_df[
                "pace_delta"
            ].describe()
        )

        return working_df