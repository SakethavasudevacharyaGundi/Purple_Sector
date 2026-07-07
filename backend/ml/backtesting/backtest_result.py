from pydantic import BaseModel


class BacktestResult(BaseModel):

    season: int

    event_name: str

    driver_number: str

    state_lap: int

    actual_pit_lap: int

    actual_compound: str

    predicted_finish: float

    actual_finish: int

    error: float