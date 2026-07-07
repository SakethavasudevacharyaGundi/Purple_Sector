import pandas as pd


class PitLossDatasetBuilder:

    def build(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        pit_in_df = df[
            df["pit_in_time_seconds"]
            .notna()
        ].copy()

        pit_out_df = df[
            df["pit_out_time_seconds"]
            .notna()
        ].copy()

        pit_in_df = pit_in_df[
            [
                "season",
                "event_name",
                "circuit_name",
                "driver_number",
                "lap_number",
                "total_laps",
                "position",
                "current_compound",
                "current_tyre_age",
                "stint",
                "gap_ahead",
                "gap_behind",
                "gap_to_leader",
                "track_temp",
                "air_temp",
                "rainfall",
                "track_condition",
                "laps_remaining",
                "pit_in_time_seconds",
            ]
        ]

        pit_out_df = pit_out_df[
            [
                "season",
                "event_name",
                "driver_number",
                "lap_number",
                "pit_out_time_seconds",
            ]
        ]

        merged = pit_in_df.merge(
            pit_out_df,
            on=[
                "season",
                "event_name",
                "driver_number",
            ],
            how="inner",
            suffixes=(
                "_in",
                "_out",
            ),
        )

        merged = merged[
            merged["lap_number_out"]
            ==
            merged["lap_number_in"] + 1
        ]

        merged["pit_loss_seconds"] = (
            merged[
                "pit_out_time_seconds"
            ]
            -
            merged[
                "pit_in_time_seconds"
            ]
        )

        merged = merged[
            merged[
                "pit_loss_seconds"
            ].between(
                15,
                35,
            )
        ]

        merged["pit_window_ratio"] = (
            merged["lap_number_in"]
            /
            merged["total_laps"]
        )

        merged["race_progress"] = (
            merged["lap_number_in"]
            /
            merged["total_laps"]
        )

        print()
        print(
            "PIT LOSS DATASET"
        )

        print(
            merged.shape
        )

        print()

        print(
            merged[
                "pit_loss_seconds"
            ].describe()
        )

        return merged