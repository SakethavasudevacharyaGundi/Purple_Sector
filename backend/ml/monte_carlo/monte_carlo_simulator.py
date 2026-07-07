from collections import Counter
import statistics

import numpy as np

from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy import Strategy

from ml.simulator.strategy_simulator import (
    StrategySimulator,
)

from ml.monte_carlo.monte_carlo_result import (
    MonteCarloResult,
)

from ml.monte_carlo.outcome_distribution import (
    OutcomeDistribution,
)

from ml.monte_carlo.race_outcome_simulator import (
    RaceOutcomeSimulator,
)


class MonteCarloSimulator:

    def __init__(self):

        self.strategy_simulator = (
            StrategySimulator()
        )

        self.outcome_simulator = (
            RaceOutcomeSimulator()
        )

    def simulate(

        self,

        race_state: RaceState,

        driver: DriverState,

        strategy: Strategy,

        runs: int = 1000,

    ) -> MonteCarloResult:

        finishes = []

        for _ in range(runs):

            components = (

                self.strategy_simulator
                .simulate_components(
                    race_state,
                    driver,
                    strategy,
                )

            )

            finish_position = (

                self.outcome_simulator
                .simulate(
                    components
                )

            )

            finishes.append(
                finish_position
            )

        counts = Counter(
            finishes
        )

        distributions = []

        for position in sorted(
            counts.keys()
        ):

            probability = (
                counts[position]
                /
                runs
            )

            distributions.append(

                OutcomeDistribution(

                    position=position,

                    probability=round(
                        probability,
                        4,
                    ),
                )

            )

        expected_finish = (
            statistics.mean(
                finishes
            )
        )

        median_finish = (
            statistics.median(
                finishes
            )
        )

        finish_std = (
            statistics.pstdev(
                finishes
            )
        )

        p10_finish = int(
            np.percentile(
                finishes,
                10,
            )
        )

        p90_finish = int(
            np.percentile(
                finishes,
                90,
            )
        )

        podium_probability = (

            len(
                [
                    x
                    for x in finishes
                    if x <= 3
                ]
            )
            /
            runs

        )

        points_probability = (

            len(
                [
                    x
                    for x in finishes
                    if x <= 10
                ]
            )
            /
            runs

        )

        win_probability = (

            len(
                [
                    x
                    for x in finishes
                    if x == 1
                ]
            )
            /
            runs

        )

        return MonteCarloResult(

            expected_finish_position=
            round(
                expected_finish,
                2,
            ),

            median_finish_position=
            round(
                median_finish,
                2,
            ),

            finish_position_std=
            round(
                finish_std,
                2,
            ),

            p10_finish_position=
            p10_finish,

            p90_finish_position=
            p90_finish,

            podium_probability=
            round(
                podium_probability,
                4,
            ),

            points_probability=
            round(
                points_probability,
                4,
            ),

            win_probability=
            round(
                win_probability,
                4,
            ),

            distributions=
            distributions,
        )