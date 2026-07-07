class TyreTrainingView:

    def build(self, df):

        df = df.copy()

        df = df[
            df["track_condition"]
            == "ALL_CLEAR"
        ]

        df = df[
            df["future_lap_time"].notna()
        ]

        df = df[
            df["current_lap_time"].notna()
        ]

        return df