import pandas as pd


class StintDatasetBuilder:

    def build(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        working_df = df.copy()

        working_df = working_df.dropna(
            subset=[
                "current_lap_time",
                "current_compound",
                "current_tyre_age",
                "stint",
            ]
        )

        working_df = working_df.sort_values(
            [
                "season",
                "event_name",
                "driver_number",
                "lap_number",
            ]
        )

        stint_groups = [

            "season",
            "event_name",
            "driver_number",
            "stint",
        ]

        working_df[
            "stint_best_lap"
        ] = (

            working_df
            .groupby(stint_groups)[
                "current_lap_time"
            ]
            .transform("min")

        )

        working_df[
            "stint_mean_lap"
        ] = (

            working_df
            .groupby(stint_groups)[
                "current_lap_time"
            ]
            .transform("mean")

        )

        working_df[
            "stint_median_lap"
        ] = (

            working_df
            .groupby(stint_groups)[
                "current_lap_time"
            ]
            .transform("median")

        )

        working_df[
            "degradation_seconds"
        ] = (

            working_df[
                "current_lap_time"
            ]

            -

            working_df[
                "stint_best_lap"
            ]

        )

        return working_df