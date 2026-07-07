# backend/state_builder/weather_parser.py

import bisect

import pandas as pd


class WeatherParser:

    def __init__(
        self,
        weather_df: pd.DataFrame,
    ):

        self.weather_df = (
            weather_df
            .sort_values("Time")
            .reset_index(drop=True)
        )

        self.times = list(
            self.weather_df["Time"]
        )

    def get_weather(
        self,
        session_time: pd.Timedelta,
    ):

        idx = bisect.bisect_right(
            self.times,
            session_time,
        ) - 1

        if idx < 0:
            return None

        return self.weather_df.iloc[idx]