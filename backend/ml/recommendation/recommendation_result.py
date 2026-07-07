from pydantic import BaseModel


class RecommendationResult(BaseModel):

    recommended_pit_lap: int

    recommended_compound: str

    expected_finish_position: float

    points_probability: float

    podium_probability: float

    win_probability: float

    explanation: str