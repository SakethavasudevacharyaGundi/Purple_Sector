from pydantic import BaseModel

class recommendation(BaseModel):
    strategy_id:str
    confidencce :float
    explanation:list[str]
    