from pydantic import BaseModel


class StrategyRecommendation(BaseModel):

    pit_lap: int

    compound: str

    expected_finish_position: float

    points_probability: float

    podium_probability: float

    win_probability: float