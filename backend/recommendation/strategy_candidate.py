from pydantic import BaseModel
from recommendation.strategy_type import StrategyType
from recommendation.pit_stop import Pitstop 

class StrategyCandidate(BaseModel):
    strategy_type:StrategyType
    pit_stops:list[Pitstop]
