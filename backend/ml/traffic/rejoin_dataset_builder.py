import pandas as pd


class RejoinDatasetBuilder:

    def build(
        self,
        dataset_path: str,
    ) -> pd.DataFrame:

        df = pd.read_parquet(
            dataset_path
        )

        pit_in_rows = df[
            df["pit_in_time_seconds"]
            .notna()
        ].copy()

        rows = []

        for _, pit_in in pit_in_rows.iterrows():

            season = pit_in["season"]

            event_name = pit_in["event_name"]

            driver_number = pit_in[
                "driver_number"
            ]

            lap_in = pit_in[
                "lap_number"
            ]

            race_df = df[
                (
                    df["season"]
                    == season
                )
                &
                (
                    df["event_name"]
                    == event_name
                )
            ]

            driver_df = race_df[
                race_df[
                    "driver_number"
                ]
                == driver_number
            ].sort_values(
                "lap_number"
            )

            pit_out_candidates = driver_df[
                (
                    driver_df[
                        "lap_number"
                    ]
                    >= lap_in
                )
                &
                (
                    driver_df[
                        "pit_out_time_seconds"
                    ]
                    .notna()
                )
            ]

            if pit_out_candidates.empty:
                continue

            pit_out = (
                pit_out_candidates
                .iloc[0]
            )

            pit_loss = (
                pit_out[
                    "pit_out_time_seconds"
                ]
                -
                pit_in[
                    "pit_in_time_seconds"
                ]
            )

            #
            # remove garbage rows
            #

            if (
                pit_loss < 15
                or pit_loss > 35
            ):
                continue

            #
            # actual position AFTER
            # rejoining race order
            #

            next_lap = (
                pit_out[
                    "lap_number"
                ]
                + 1
            )

            rejoin_row = driver_df[
                driver_df[
                    "lap_number"
                ]
                == next_lap
            ]

            if rejoin_row.empty:
                continue

            actual_position = (
                rejoin_row
                .iloc[0]
                ["position"]
            )

            if pd.isna(
                actual_position
            ):
                continue

            rows.append(
                {
                    "season":
                    season,

                    "event_name":
                    event_name,

                    "driver_number":
                    driver_number,

                    "lap_number":
                    lap_in,

                    "position_before_pit":
                    pit_in[
                        "position"
                    ],

                    "gap_to_leader":
                    pit_in[
                        "gap_to_leader"
                    ],

                    "pit_loss_seconds":
                    pit_loss,

                    "actual_rejoin_position":
                    int(
                        actual_position
                    ),
                }
            )

        print()
        print("USING NEW REJOIN DATASET BUILDER")
        print()
        return pd.DataFrame(
            rows
        )