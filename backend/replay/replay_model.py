from pydantic import BaseModel
from domain.race_state import RaceState
class RaceReplay(BaseModel):
    season:int
    event_name:str
    total_laps:int
    states:list[RaceState]
    