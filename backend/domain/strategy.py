from pydantic import BaseModel

class StrategyCandidate(BaseModel):
    strategy_id:str
    pit_lap:int
    