from datetime import datetime
from pydantic import BaseModel

class RaceEvent(BaseModel):
    event_id:str
    timestamp:datetime
    event_type:str
    payload:dict    
    