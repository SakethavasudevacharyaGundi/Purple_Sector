import pandas as pd

from domain.race_state import RaceState
from domain.driver_state import DriverState

from state_builder.track_status_parser import (
    TrackCondition,
)


class HistoricalStateFactory:

    def build(

        self,

        race_df: pd.DataFrame,

        driver_number: str,

        lap_number: int,

    ) -> tuple[RaceState, DriverState]:

        lap_df = race_df[

            race_df["lap_number"]
            ==
            lap_number

        ].copy()

        if lap_df.empty:

            raise ValueError(

                f"No race data found "
                f"for lap {lap_number}"

            )

        driver_row = lap_df[

            lap_df[
                "driver_number"
            ].astype(str)

            ==

            str(driver_number)

        ]

        if driver_row.empty:

            raise ValueError(

                f"Driver {driver_number} "
                f"not found on lap "
                f"{lap_number}"

            )

        driver_row = (
            driver_row.iloc[0]
        )

        drivers = []

        for _, row in lap_df.iterrows():

            driver = DriverState(

                driver_number=str(
                    row["driver_number"]
                ),

                driver_name=str(
                    row["driver_number"]
                ),

                team="UNKNOWN",

                position=(
                    None
                    if pd.isna(
                        row["position"]
                    )
                    else int(
                        row["position"]
                    )
                ),

                current_compound=(
                    None
                    if pd.isna(
                        row[
                            "current_compound"
                        ]
                    )
                    else str(
                        row[
                            "current_compound"
                        ]
                    )
                ),

                current_tyre_age=(
                    None
                    if pd.isna(
                        row[
                            "current_tyre_age"
                        ]
                    )
                    else int(
                        row[
                            "current_tyre_age"
                        ]
                    )
                ),

                stint=(
                    None
                    if pd.isna(
                        row["stint"]
                    )
                    else int(
                        row["stint"]
                    )
                ),

                gap_ahead=float(
                    row["gap_ahead"]
                )
                if pd.notna(
                    row["gap_ahead"]
                )
                else 0.0,

                gap_behind=float(
                    row["gap_behind"]
                )
                if pd.notna(
                    row["gap_behind"]
                )
                else 0.0,

                gap_to_leader=float(
                    row[
                        "gap_to_leader"
                    ]
                )
                if pd.notna(
                    row[
                        "gap_to_leader"
                    ]
                )
                else 0.0,

                last_lap_time=float(
                    row[
                        "current_lap_time"
                    ]
                )
                if pd.notna(
                    row[
                        "current_lap_time"
                    ]
                )
                else None,

            )

            drivers.append(
                driver
            )

        drivers.sort(

            key=lambda d: (

                d.position is None,

                (
                    d.position
                    if d.position
                    is not None
                    else 999
                ),

            )

        )

        race_state = RaceState(
            race_id=(
                f"{driver_row['season']}_"
                f"{driver_row['event_name']}"
            ),
            season=int(driver_row['season']),
            event_name=str(
                driver_row[
                    "event_name"
                ]
            ),

            lap_number=int(
                driver_row[
                    "lap_number"
                ]
            ),

            total_laps=int(
                driver_row[
                    "total_laps"
                ]
            ),

            track_condition=
            TrackCondition.ALL_CLEAR,

            air_temp=float(
                driver_row[
                    "air_temp"
                ]
            )
            if pd.notna(
                driver_row[
                    "air_temp"
                ]
            )
            else None,

            track_temp=float(
                driver_row[
                    "track_temp"
                ]
            )
            if pd.notna(
                driver_row[
                    "track_temp"
                ]
            )
            else None,

            rainfall=bool(
                driver_row[
                    "rainfall"
                ]
            ),

            drivers=drivers,

        )
        selected_driver = next(

            driver

            for driver in drivers

            if (

                driver.driver_number

                ==

                str(driver_number)

            )

        )

        return (

            race_state,

            selected_driver,

        )