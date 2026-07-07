import pandas as pd


class TrafficLossDatasetBuilder:

    LOOKAHEAD_LAPS = 5

    def build(
        self,
        master_dataset_path: str,
    ):

        df = pd.read_parquet(
            master_dataset_path
        )

        rows = []

        grouped = df.groupby(
            [
                "season",
                "event_name",
                "driver_number",
            ]
        )

        for _, driver_df in grouped:

            driver_df = (
                driver_df
                .sort_values(
                    "lap_number"
                )
                .reset_index(
                    drop=True
                )
            )

            pit_rows = driver_df[
                driver_df[
                    "pit_in_time_seconds"
                ].notna()
            ]

            for _, pit_row in pit_rows.iterrows():

                lap = int(
                    pit_row[
                        "lap_number"
                    ]
                )

                future = driver_df[
                    driver_df[
                        "lap_number"
                    ]
                    ==
                    lap
                    +
                    self.LOOKAHEAD_LAPS
                ]

                if future.empty:
                    continue

                future_position = (
                    future.iloc[0][
                        "position"
                    ]
                )

                rejoin_position = (
                    pit_row[
                        "position"
                    ]
                )

                if (
                    pd.isna(
                        future_position
                    )
                    or
                    pd.isna(
                        rejoin_position
                    )
                ):
                    continue

                future_position = int(
                    future_position
                )

                rejoin_position = int(
                    rejoin_position
                )

                gap_ahead = pit_row[
                    "gap_ahead"
                ]

                gap_behind = pit_row[
                    "gap_behind"
                ]

                tyre_age = pit_row[
                    "current_tyre_age"
                ]

                if pd.isna(
                    gap_ahead
                ):
                    gap_ahead = -1.0

                if pd.isna(
                    gap_behind
                ):
                    gap_behind = -1.0

                if pd.isna(
                    tyre_age
                ):
                    tyre_age = 0.0

                rows.append(
                    {
                        "season":
                        pit_row[
                            "season"
                        ],

                        "event_name":
                        pit_row[
                            "event_name"
                        ],

                        "driver_number":
                        pit_row[
                            "driver_number"
                        ],

                        "lap_number":
                        lap,

                        "rejoin_position":
                        rejoin_position,

                        "gap_ahead":
                        float(
                            gap_ahead
                        ),

                        "gap_behind":
                        float(
                            gap_behind
                        ),

                        "current_compound":
                        str(
                            pit_row[
                                "current_compound"
                            ]
                        ),

                        "current_tyre_age":
                        float(
                            tyre_age
                        ),

                        "traffic_loss":
                        (
                            future_position
                            -
                            rejoin_position
                        ),
                    }
                )

        dataset = pd.DataFrame(
            rows
        )

        return dataset