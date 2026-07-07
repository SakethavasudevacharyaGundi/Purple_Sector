from pydantic import BaseModel

class Simulation_result(BaseModel):
    strategy_id:str
    expected_finish_position:float
    probability_p1:float
    probability_p2:float
    probability_p3:float


