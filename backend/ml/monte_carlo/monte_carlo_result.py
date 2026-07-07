from pydantic import BaseModel

from ml.monte_carlo.outcome_distribution import (
    OutcomeDistribution,
)


class MonteCarloResult(BaseModel):

    expected_finish_position: float

    median_finish_position: float

    finish_position_std: float

    p10_finish_position: int

    p90_finish_position: int

    podium_probability: float

    points_probability: float

    win_probability: float

    distributions: list[
        OutcomeDistribution
    ]