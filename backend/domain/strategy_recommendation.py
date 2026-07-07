from pydantic import BaseModel


class StrategyRecommendation(
    BaseModel
):

    pit_lap: int

    compound: str

    expected_finish_position: float

    expected_rejoin_position: float

    expected_pit_loss: float

    expected_traffic_loss: float