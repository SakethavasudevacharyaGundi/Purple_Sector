from pydantic import BaseModel

class OutcomeDistribution(BaseModel):
    position:int
    probability:float
    