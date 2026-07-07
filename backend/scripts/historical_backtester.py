from pathlib import Path

import pandas as pd

from domain.driver_state import DriverState
from domain.driver_status import DriverStatus
from domain.race_state import RaceState

from state_builder.track_status_parser import (
    TrackCondition,
)

from ml.simulator.strategy import (
    Strategy,
)

from ml.simulator.strategy_simulator import (
    StrategySimulator,
)


class HistoricalBacktester:

    def __init__(self):

        self.simulator = (

            StrategySimulator()

        )

    def load_dataset(

        self,

    ) -> pd.DataFrame:

        df = pd.read_parquet(

            Path(

                "data/ml/v1/master_dataset.parquet"

            )

        )

        df = (

            df

            .sort_values(

                [

                    "season",

                    "event_name",

                    "driver_number",

                    "lap_number",

                ]

            )

        )

        return df

    def build_race_state(

        self,

        row,

    ) -> RaceState:

        return RaceState(

            race_id=

            f"{row.season}_{row.event_name}",

            season=

            int(row.season),

            event_name=

            row.event_name,

            lap_number=

            int(row.lap_number),

            total_laps=

            int(row.total_laps),

            track_condition=

            TrackCondition(

                row.track_condition

            ),

            air_temp=

            None

            if pd.isna(

                row.air_temp

            )

            else

            float(

                row.air_temp

            ),

            track_temp=

            None

            if pd.isna(

                row.track_temp

            )

            else

            float(

                row.track_temp

            ),

            rainfall=

            bool(

                row.rainfall

            ),

            drivers=[],

        )

    def build_driver_state(

        self,

        row,

    ) -> DriverState:

        return DriverState(

            driver_number=

            str(

                row.driver_number

            ),

            driver_name=

            "",

            team=

            "",

            status=

            DriverStatus.ACTIVE,

            position=

            None

            if pd.isna(

                row.position

            )

            else

            int(

                row.position

            ),

            current_compound=

            row.current_compound,

            current_tyre_age=

            None

            if pd.isna(

                row.current_tyre_age

            )

            else

            int(

                row.current_tyre_age

            ),

            stint=

            None

            if pd.isna(

                row.stint

            )

            else

            int(

                row.stint

            ),

            gap_ahead=

            None

            if pd.isna(

                row.gap_ahead

            )

            else

            float(

                row.gap_ahead

            ),

            gap_behind=

            None

            if pd.isna(

                row.gap_behind

            )

            else

            float(

                row.gap_behind

            ),

            gap_to_leader=

            0.0

            if pd.isna(

                row.gap_to_leader

            )

            else

            float(

                row.gap_to_leader

            ),

            last_lap_time=

            None

            if pd.isna(

                row.current_lap_time

            )

            else

            float(

                row.current_lap_time

            ),

            pit_in_time_seconds=

            None

            if pd.isna(

                row.pit_in_time_seconds

            )

            else

            float(

                row.pit_in_time_seconds

            ),

            pit_out_time_seconds=

            None

            if pd.isna(

                row.pit_out_time_seconds

            )

            else

            float(

                row.pit_out_time_seconds

            ),

        )
    def run(

        self,

    ) -> pd.DataFrame:

        df = self.load_dataset()

        predictions = []

        grouped = df.groupby(

            [

                "season",

                "event_name",

                "driver_number",

            ],

            sort=False,

        )

        for (

            season,

            event_name,

            driver_number,

        ), driver_df in grouped:

            driver_df = (

                driver_df

                .sort_values(

                    "lap_number"

                )

            )

            final_row = (

                driver_df.iloc[-1]

            )

            if (

                pd.isna(

                    final_row.position

                )

            ):

                continue

            actual_finish = int(

                final_row.position

            )

            pit_rows = (

                driver_df[

                    driver_df[

                        "pit_out_time_seconds"

                    ]

                    .notna()

                ]

            )

            if len(

                pit_rows

            ) == 0:

                continue

            pit_row = (

                pit_rows.iloc[0]

            )

            pit_lap = int(

                pit_row.lap_number

            )

            decision_rows = (

                driver_df[

                    driver_df

                    .lap_number

                    ==

                    pit_lap - 1

                ]

            )

            if len(

                decision_rows

            ) == 0:

                continue

            decision_row = (

                decision_rows.iloc[0]

            )

            if pd.isna(

                decision_row.position

            ):

                continue

            race_state = (

                self.build_race_state(

                    decision_row

                )

            )

            driver_state = (

                self.build_driver_state(

                    decision_row

                )

            )

            strategy = Strategy(

                pit_lap=

                pit_lap,

                next_compound=

                pit_row.current_compound,

            )

            try:

                result = (

                    self.simulator

                    .simulate(

                        race_state,

                        driver_state,

                        strategy,

                    )

                )

            except Exception as e:

                print()

                print(

                    "Simulation failed"

                )

                print(

                    season,

                    event_name,

                    driver_number,

                )

                print(e)

                continue

            predicted_finish = int(

                round(

                    result

                    .expected_finish_position

                )

            )

            predictions.append(

                {

                    "season":

                    season,

                    "event_name":

                    event_name,

                    "driver_number":

                    driver_number,

                    "pit_lap":

                    pit_lap,

                    "compound":

                    strategy.next_compound,

                    "predicted_finish":

                    predicted_finish,

                    "actual_finish":

                    actual_finish,

                    "absolute_error":

                    abs(

                        predicted_finish

                        -

                        actual_finish

                    ),

                }

            )

        return pd.DataFrame(

            predictions

        )
    def summarize(

        self,

        predictions: pd.DataFrame,

    ) -> None:

        if predictions.empty:

            print()

            print(
                "No predictions generated."
            )

            return

        mae = float(

            predictions[
                "absolute_error"
            ].mean()

        )

        median_error = float(

            predictions[
                "absolute_error"
            ].median()

        )

        exact_accuracy = (

            (

                predictions[
                    "absolute_error"
                ]

                ==

                0

            )

            .mean()

        )

        within_one = (

            (

                predictions[
                    "absolute_error"
                ]

                <=

                1

            )

            .mean()

        )

        within_two = (

            (

                predictions[
                    "absolute_error"
                ]

                <=

                2

            )

            .mean()

        )

        podium_accuracy = (

            (

                (

                    predictions[
                        "predicted_finish"
                    ]

                    <=

                    3

                )

                ==

                (

                    predictions[
                        "actual_finish"
                    ]

                    <=

                    3

                )

            )

            .mean()

        )

        points_accuracy = (

            (

                (

                    predictions[
                        "predicted_finish"
                    ]

                    <=

                    10

                )

                ==

                (

                    predictions[
                        "actual_finish"
                    ]

                    <=

                    10

                )

            )

            .mean()

        )

        print()

        print("=" * 80)

        print(
            "PURPLE SECTOR HISTORICAL BACKTEST"
        )

        print("=" * 80)

        print()

        print(
            f"Predictions      : {len(predictions)}"
        )

        print(
            f"Mean Abs Error   : {mae:.2f}"
        )

        print(
            f"Median Error     : {median_error:.2f}"
        )

        print(
            f"Exact Accuracy   : {exact_accuracy:.2%}"
        )

        print(
            f"Within ±1        : {within_one:.2%}"
        )

        print(
            f"Within ±2        : {within_two:.2%}"
        )

        print(
            f"Podium Accuracy  : {podium_accuracy:.2%}"
        )

        print(
            f"Points Accuracy  : {points_accuracy:.2%}"
        )

        print()

        print("=" * 80)

    def save(

        self,

        predictions: pd.DataFrame,

    ) -> None:

        output_dir = Path(

            "data/ml/backtesting"

        )

        output_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        output_file = (

            output_dir

            /

            "historical_backtest.parquet"

        )

        predictions.to_parquet(

            output_file,

            index=False,

        )

        print()

        print(

            f"Saved: {output_file}"

        )


def main():

    backtester = (

        HistoricalBacktester()

    )

    predictions = (

        backtester.run()

    )

    backtester.save(

        predictions

    )

    backtester.summarize(

        predictions

    )


if __name__ == "__main__":

    main()