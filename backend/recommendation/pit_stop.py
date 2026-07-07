from pydantic import BaseModel

class Pitstop(BaseModel):
    lap:int
    compound:str
    