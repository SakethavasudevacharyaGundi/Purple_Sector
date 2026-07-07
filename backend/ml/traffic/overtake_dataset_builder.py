from pathlib import Path

import pandas as pd


class OvertakeDatasetBuilder:

    LOOKAHEAD_LAPS = 3

    def build(
        self,
        master_dataset_path: str,
    ):

        df = pd.read_parquet(
            master_dataset_path
        )

        df = df.dropna(
            subset=[
                "position",
            ]
        )

        df = df.sort_values(
            [
                "season",
                "event_name",
                "driver_number",
                "lap_number",
            ]
        )

        rows = []

        grouped = df.groupby(
            [
                "season",
                "event_name",
                "driver_number",
            ]
        )

        for (
            _,
            driver_df,
        ) in grouped:

            driver_df = (
                driver_df.sort_values(
                    "lap_number"
                )
            )

            lap_lookup = (
                driver_df.set_index(
                    "lap_number"
                )
            )

            for _, row in (
                driver_df.iterrows()
            ):

                if pd.isna(
                    row["position"]
                ):
                    continue

                current_lap = int(
                    row["lap_number"]
                )

                current_position = int(
                    row["position"]
                )

                future_lap = (
                    current_lap
                    + self.LOOKAHEAD_LAPS
                )

                if (
                    future_lap
                    not in lap_lookup.index
                ):
                    continue

                future_position = (
                    lap_lookup.loc[
                        future_lap,
                        "position",
                    ]
                )

                if pd.isna(
                    future_position
                ):
                    continue

                future_position = int(
                    future_position
                )

                overtake_happened = int(
                    future_position
                    < current_position
                )

                gap_ahead = row.get(
                    "gap_ahead",
                    None,
                )

                drs_zone = int(
                    pd.notna(gap_ahead)
                    and gap_ahead <= 1.0
                )

                attack_zone = int(
                    pd.notna(gap_ahead)
                    and gap_ahead <= 2.0
                )

                tyre_age = row.get(
                    "current_tyre_age",
                    0,
                )

                if pd.isna(
                    tyre_age
                ):
                    tyre_age = 0

                compound = row.get(
                    "current_compound",
                    "UNKNOWN",
                )

                if pd.isna(
                    compound
                ):
                    compound = "UNKNOWN"

                compound = str(
                    compound
                )

                compound_age = (
                    f"{compound}_"
                    f"{int(float(tyre_age) // 5)}"
                )

                rows.append(
                    {
                        "season":
                        row["season"],

                        "event_name":
                        row["event_name"],

                        "driver_number":
                        row["driver_number"],

                        "lap_number":
                        row["lap_number"],

                        "position":
                        current_position,

                        "gap_ahead":
                        row.get(
                            "gap_ahead"
                        ),

                        "gap_behind":
                        row.get(
                            "gap_behind"
                        ),

                        "gap_to_leader":
                        row.get(
                            "gap_to_leader"
                        ),

                        "current_compound":
                        compound,

                        "current_tyre_age":
                        tyre_age,

                        "stint":
                        row.get(
                            "stint"
                        ),

                        "track_condition":
                        row.get(
                            "track_condition"
                        ),

                        "current_lap_time":
                        row.get(
                            "current_lap_time"
                        ),

                        "lap_time_delta":
                        row.get(
                            "lap_time_delta"
                        ),

                        "laps_remaining":
                        row.get(
                            "laps_remaining"
                        ),

                        "drs_zone":
                        drs_zone,

                        "attack_zone":
                        attack_zone,

                        "compound_age":
                        compound_age,

                        "overtake_happened":
                        overtake_happened,
                    }
                )

        result = pd.DataFrame(
            rows
        )

        save_path = Path(
            "data/ml/v1/overtake_dataset.parquet"
        )

        save_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        result.to_parquet(
            save_path,
            index=False,
        )

        return result