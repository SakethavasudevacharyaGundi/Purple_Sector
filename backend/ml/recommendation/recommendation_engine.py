from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy_evaluator import (
    StrategyEvaluator,
)

from ml.monte_carlo.monte_carlo_simulator import (
    MonteCarloSimulator,
)

from ml.recommendation.recommendation_result import (
    RecommendationResult,
)


class RecommendationEngine:

    def __init__(self):

        self.strategy_evaluator = (
            StrategyEvaluator()
        )

        self.monte_carlo = (
            MonteCarloSimulator()
        )

    def recommend(

        self,

        race_state: RaceState,

        driver: DriverState,

    ) -> RecommendationResult:

        strategies = (

            self.strategy_evaluator
            .evaluate(
                race_state,
                driver,
            )

        )

        best_result = None

        best_strategy = None

        for candidate in strategies[:10]:

            strategy = (
                candidate["strategy"]
            )

            monte_carlo_result = (

                self.monte_carlo
                .simulate(
                    race_state,
                    driver,
                    strategy,
                )

            )

            if (

                best_result is None

                or

                monte_carlo_result
                .expected_finish_position

                <

                best_result
                .expected_finish_position

            ):

                best_result = (
                    monte_carlo_result
                )

                best_strategy = (
                    strategy
                )

        explanation = (

            f"Pit on lap "
            f"{best_strategy.pit_lap} "
            f"for "
            f"{best_strategy.next_compound}. "
            f"Expected finish "
            f"P{best_result.expected_finish_position:.1f}. "
            f"Points probability "
            f"{best_result.points_probability * 100:.1f}%."
        )

        return RecommendationResult(

            recommended_pit_lap=
            best_strategy.pit_lap,

            recommended_compound=
            best_strategy.next_compound,

            expected_finish_position=
            best_result
            .expected_finish_position,

            points_probability=
            best_result
            .points_probability,

            podium_probability=
            best_result
            .podium_probability,

            win_probability=
            best_result
            .win_probability,

            explanation=
            explanation,
        )