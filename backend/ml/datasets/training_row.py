from pydantic import BaseModel
class TrainingRow(BaseModel):
    season:int
    event_name:str
    circuit_name:str
    driver_number:str
    lap_number:int
    total_laps:int
    position:int|None
    current_compound:str|None
    current_tyre_age:int|None
    stint:int|None
    gap_ahead:float|None
    gap_behind:float|None
    gap_to_leader:float|None
    air_temp:float|None
    track_temp:float|None
    rainfall:bool
    track_condition:str
    laps_remaining:int
    future_lap_time:float|None
    lap_time_delta: float | None
    current_lap_time: float | None
    pit_in_time_seconds: float | None=None
    pit_out_time_seconds: float | None=None

