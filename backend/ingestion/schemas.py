from pydantic import BaseModel

class RaceMetadata(BaseModel):
    season:int
    gp_name:str
    session_type:str
    event_name:str
    circuit_name:str

