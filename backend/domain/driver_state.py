from pydantic import BaseModel
from domain.driver_status import DriverStatus
class DriverState(BaseModel):
    driver_number:str
    driver_name:str
    team:str
    status:DriverStatus=DriverStatus.ACTIVE
    position:int| None=None
    current_compound:str | None=None
    current_tyre_age:int | None=None
    stint:int | None=None
    gap_ahead:float | None=None
    gap_behind:float | None=None
    gap_to_leader:float 
    last_lap_time:float | None=None
    pit_in_this_lap:bool=False
    pit_out_this_lap:bool=False
    is_retired:bool=False
    pit_in_time_seconds: float | None = None
    pit_out_time_seconds: float | None = None


