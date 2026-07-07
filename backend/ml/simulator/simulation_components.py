from pydantic import BaseModel


class SimulationComponents(BaseModel):

    pit_loss: float

    rejoin_position: float

    traffic_loss: float

    average_pace: float = 0.0

    degradation_seconds: float = 0.0

    expected_overtakes: float = 0.0
    

