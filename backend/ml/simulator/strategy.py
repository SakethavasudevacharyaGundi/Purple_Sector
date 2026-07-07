from pydantic import BaseModel
class Strategy(BaseModel):
    pit_lap:int
    next_compound:str
    