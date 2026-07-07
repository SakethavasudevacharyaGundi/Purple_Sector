# state_builder/track_status_parser.py

from domain.track_condition import (
    TrackCondition,
)


class TrackStatusParser:

    def __init__(
        self,
        track_status_df,
    ):
        self.track_status_df = (
            track_status_df
        )

    def get_track_condition(
        self,
        session_time,
    ) -> TrackCondition:

        valid_rows = (
            self.track_status_df[
                self.track_status_df["Time"]
                <= session_time
            ]
        )

        if valid_rows.empty:
            return TrackCondition.UNKNOWN

        latest = valid_rows.iloc[-1]

        status = str(
            latest["Status"]
        )

        if status == "1":
            return TrackCondition.ALL_CLEAR

        if status == "2":
            return TrackCondition.YELLOW

        if status == "4":
            return TrackCondition.SAFETY_CAR

        if status == "5":
            return TrackCondition.RED_FLAG

        return TrackCondition.UNKNOWN