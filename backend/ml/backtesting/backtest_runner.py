import pandas as pd

from ml.backtesting.backtest_result import (
    BacktestResult,
)

from ml.backtesting.strategy_extractor import (
    StrategyExtractor,
)

from ml.backtesting.historical_state_factory import (
    HistoricalStateFactory,
)

from ml.backtesting.metrics_calculator import (
    MetricsCalculator,
)

from ml.monte_carlo.monte_carlo_simulator import (
    MonteCarloSimulator,
)


class BacktestRunner:

    def __init__(self):

        self.dataset = pd.read_parquet(
            "data/ml/v1/master_dataset.parquet"
        )

        self.strategy_extractor = (
            StrategyExtractor()
        )

        self.state_factory = (
            HistoricalStateFactory()
        )

        self.monte_carlo = (
            MonteCarloSimulator()
        )

        self.metrics = (
            MetricsCalculator()
        )

    def run_race(

        self,

        season: int,

        event_name: str,

        state_lap: int,

        monte_carlo_runs: int = 500,

    ):

        race_df = self.dataset[

            (self.dataset["season"] == season)

            &

            (
                self.dataset["event_name"]
                ==
                event_name
            )

        ].copy()

        if race_df.empty:

            raise ValueError(

                f"No data found for "

                f"{season} "

                f"{event_name}"

            )

        results = []

        driver_numbers = sorted(

            race_df[
                "driver_number"
            ]
            .astype(str)
            .unique()

        )

        for driver_number in driver_numbers:

            result = self.run_driver(

                race_df=race_df,

                driver_number=
                driver_number,

                state_lap=
                state_lap,

                monte_carlo_runs=
                monte_carlo_runs,

            )

            if result is not None:

                results.append(
                    result
                )

        results_df = pd.DataFrame(

            [
                result.model_dump()
                for result in results
            ]

        )

        metrics = (

            self.metrics
            .calculate(
                results_df
            )

        )

        return (

            results_df,

            metrics,

        )

    def run_driver(

        self,

        race_df: pd.DataFrame,

        driver_number: str,

        state_lap: int,

        monte_carlo_runs: int,

    ) -> BacktestResult | None:

        strategy = (

            self.strategy_extractor
            .extract(

                race_df=race_df,

                driver_number=
                driver_number,

                state_lap=
                state_lap,

            )

        )

        if strategy is None:

            return None

        race_state, driver = (

            self.state_factory
            .build(

                race_df=race_df,

                driver_number=
                driver_number,

                lap_number=
                state_lap,

            )

        )

        monte_carlo_result = (

            self.monte_carlo
            .simulate(

                race_state=
                race_state,

                driver=
                driver,

                strategy=
                strategy,

                runs=
                monte_carlo_runs,

            )

        )

        driver_history = race_df[

            race_df[
                "driver_number"
            ]
            .astype(str)

            ==

            str(driver_number)

        ].sort_values(
            "lap_number"
        )

        actual_finish = int(

            driver_history
            .iloc[-1][
                "position"
            ]

        )

        predicted_finish = (

            monte_carlo_result
            .expected_finish_position

        )

        error = abs(

            predicted_finish

            -

            actual_finish

        )

        return BacktestResult(

            season=int(

                race_state
                .race_id
                .split("_")[0]

            ),

            event_name=
            race_state.event_name,

            driver_number=
            driver_number,

            state_lap=
            state_lap,

            actual_pit_lap=
            strategy.pit_lap,

            actual_compound=
            strategy.next_compound,

            predicted_finish=
            round(
                predicted_finish,
                2,
            ),

            actual_finish=
            actual_finish,

            error=
            round(
                error,
                2,
            ),

        )

    def print_summary(

        self,

        results_df: pd.DataFrame,

        metrics: dict,

    ):

        print()

        print("=" * 100)
        print("BACKTEST RESULTS")
        print("=" * 100)

        print()

        print(

            results_df[
                [
                    "driver_number",
                    "predicted_finish",
                    "actual_finish",
                    "error",
                    "actual_pit_lap",
                    "actual_compound",
                ]
            ]
            .sort_values(
                "error"
            )

        )

        print()

        print("=" * 100)
        print("METRICS")
        print("=" * 100)

        print()

        for key, value in metrics.items():

            print(
                f"{key}: {value}"
            )

        print()