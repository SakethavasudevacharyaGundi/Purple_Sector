# backend/state_builder/state_builder.py

import pandas as pd

from domain.driver_state import DriverState
from domain.driver_status import DriverStatus
from domain.race_state import RaceState

from state_builder.track_status_parser import TrackStatusParser
from state_builder.weather_parser import WeatherParser
from state_builder.gap_calculator import GapCalculator


class StateBuilder:

    def __init__(self):

        self.gap_calculator = GapCalculator()

    def build_state(
        self,
        session,
        lap_number: int,
    ) -> RaceState:

        lap_df = session.laps

        current_lap = lap_df[
            lap_df["LapNumber"] == lap_number
        ]

        if current_lap.empty:

            raise ValueError(
                f"No data found for lap {lap_number}"
            )

        gap_data = self.gap_calculator.calculate(
            current_lap
        )

        representative_row = current_lap.iloc[0]

        session_time = representative_row[
            "LapStartTime"
        ]
        lap_end_time = representative_row["Time"]

        track_parser = TrackStatusParser(
            session.track_status
        )

        weather_parser = WeatherParser(
            session.weather_data
        )

        track_condition = (
            track_parser.get_track_condition(
                lap_end_time
            )
        )

        weather_row = (
            weather_parser.get_weather(
                session_time
            )
        )

        drivers: list[DriverState] = []

        for _, row in current_lap.iterrows():

            driver_status = DriverStatus.ACTIVE

            if pd.isna(row["Position"]):
                driver_status = DriverStatus.UNKNOWN

            lap_time_seconds = None

            lap_time = row.get("LapTime")

            if pd.notna(lap_time):
                lap_time_seconds = (
                    lap_time.total_seconds()
                )
            

            driver_gap = gap_data.get(
                str(row["Driver"]),
                {}
            )

            drivers.append(
                DriverState(
                    driver_number=str(
                        row["DriverNumber"]
                    ),

                    driver_name=str(
                        row["Driver"]
                    ),

                    team=str(
                        row["Team"]
                    ),

                    position=(
                        None
                        if pd.isna(
                            row["Position"]
                        )
                        else int(
                            row["Position"]
                        )
                    ),

                    status=driver_status,

                    current_compound=(
                        None
                        if pd.isna(
                            row["Compound"]
                        )
                        else str(
                            row["Compound"]
                        )
                    ),

                    current_tyre_age=(
                        None
                        if pd.isna(
                            row["TyreLife"]
                        )
                        else int(
                            row["TyreLife"]
                        )
                    ),

                    stint=(
                        None
                        if pd.isna(
                            row["Stint"]
                        )
                        else int(
                            row["Stint"]
                        )
                    ),

                    gap_to_leader=
                        driver_gap.get(
                            "gap_to_leader"
                        ),

                    gap_ahead=
                        driver_gap.get(
                            "gap_ahead"
                        ),

                    gap_behind=
                        driver_gap.get(
                            "gap_behind"
                        ),

                    last_lap_time=
                        lap_time_seconds,

                    pit_in_this_lap=
                        pd.notna(
                            row["PitInTime"]
                        ),

                    pit_out_this_lap=
                        pd.notna(
                            row["PitOutTime"]
                        ),
                    pit_in_time_seconds=(
                        None
                        if pd.isna(
                            row["PitInTime"]
                        )
                        else row["PitInTime"].total_seconds()
                    ),

                    pit_out_time_seconds=(
                        None
                        if pd.isna(
                            row["PitOutTime"]
                        )
                        else row["PitOutTime"].total_seconds()
                    ),
                )
            )

        drivers.sort(
            key=lambda driver: (
                driver.position is None,
                (
                    driver.position
                    if driver.position is not None
                    else 999
                )
            )
        )

        return RaceState(
            race_id=(
                f"{session.event['RoundNumber']}_"
                f"{session.event['EventName']}"
            ),

            event_name=str(
                session.event["EventName"]
            ),

            lap_number=lap_number,

            total_laps=int(
                lap_df["LapNumber"]
                .dropna()
                .max()
            ),

            track_condition=track_condition,

            air_temp=(
                None
                if weather_row is None
                else float(
                    weather_row["AirTemp"]
                )
            ),

            track_temp=(
                None
                if weather_row is None
                else float(
                    weather_row["TrackTemp"]
                )
            ),

            rainfall=(
                False
                if weather_row is None
                else bool(
                    weather_row["Rainfall"]
                )
            ),

            drivers=drivers,
        )