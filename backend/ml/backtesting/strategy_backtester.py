import pandas as pd

from ml.backtesting.backtest_result import (
    BacktestResult,
)

from ml.recommendation.recommendation_engine import (
    RecommendationEngine,
)

from domain.race_state import RaceState
from domain.driver_state import DriverState

from state_builder.track_status_parser import (
    TrackCondition,
)


class StrategyBacktester:

    def __init__(self):

        self.engine = (
            RecommendationEngine()
        )

    def run(

        self,

        dataset_path: str,

        sample_size: int = 50,

    ) -> list[BacktestResult]:

        df = pd.read_parquet(
            dataset_path
        )

        results = []

        grouped = df.groupby(
            [
                "season",
                "event_name",
                "driver_number",
            ]
        )

        processed = 0

        for _, driver_df in grouped:

            if processed >= sample_size:
                break

            driver_df = (
                driver_df.sort_values(
                    "lap_number"
                )
            )

            if len(driver_df) < 30:
                continue

            current_row = (
                driver_df.iloc[
                    len(driver_df) // 2
                ]
            )

            final_row = (
                driver_df.iloc[-1]
            )

            if pd.isna(
                final_row["position"]
            ):
                continue

            race_state = RaceState(

                race_id="backtest",

                event_name=
                current_row["event_name"],

                lap_number=int(
                    current_row["lap_number"]
                ),

                total_laps=int(
                    current_row["total_laps"]
                ),

                track_condition=
                TrackCondition.ALL_CLEAR,

                air_temp=float(
                    current_row.get(
                        "air_temp",
                        25,
                    )
                ),

                track_temp=float(
                    current_row.get(
                        "track_temp",
                        35,
                    )
                ),

                rainfall=False,

                drivers=[],
            )

            driver = DriverState(

                driver_number=str(
                    current_row[
                        "driver_number"
                    ]
                ),

                driver_name="Unknown",

                team="Unknown",

                position=int(
                    current_row[
                        "position"
                    ]
                ),

                current_compound=str(
                    current_row[
                        "current_compound"
                    ]
                ),

                current_tyre_age=int(
                    current_row[
                        "current_tyre_age"
                    ]
                ),

                stint=int(
                    current_row[
                        "stint"
                    ]
                ),

                gap_ahead=float(
                    current_row.get(
                        "gap_ahead",
                        999,
                    )
                ),

                gap_behind=float(
                    current_row.get(
                        "gap_behind",
                        999,
                    )
                ),

                gap_to_leader=float(
                    current_row.get(
                        "gap_to_leader",
                        999,
                    )
                ),
            )

            recommendation = (
                self.engine
                .recommend(
                    race_state,
                    driver,
                )
            )

            actual_finish = float(
                final_row["position"]
            )

            predicted_finish = (
                recommendation
                .expected_finish_position
            )

            error = abs(
                predicted_finish
                -
                actual_finish
            )

            results.append(

                BacktestResult(

                    race=
                    current_row[
                        "event_name"
                    ],

                    driver_number=
                    str(
                        current_row[
                            "driver_number"
                        ]
                    ),

                    actual_finish_position=
                    actual_finish,

                    predicted_finish_position=
                    predicted_finish,

                    error=
                    round(
                        error,
                        2,
                    ),
                )
            )

            processed += 1

        return results