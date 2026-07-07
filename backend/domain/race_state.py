from pydantic import BaseModel

from domain.driver_state import DriverState
from state_builder.track_status_parser import TrackCondition


class RaceState(BaseModel):

    race_id: str

    season: int

    event_name: str

    lap_number: int

    total_laps: int

    track_condition: TrackCondition

    air_temp: float | None = None

    track_temp: float | None = None

    rainfall: bool = False

    drivers: list[DriverState]