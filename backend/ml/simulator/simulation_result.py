from pydantic import BaseModel


class SimulationResult(BaseModel):

    expected_pit_loss: float

    expected_rejoin_position: float

    expected_traffic_loss: float

    expected_finish_position: float

    expected_average_pace: float | None = None

    expected_degradation_seconds: float | None = None

    expected_overtakes: float | None = None