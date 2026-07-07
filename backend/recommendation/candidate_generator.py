from recommendation.strategy_candidate import StrategyCandidate
from recommendation.strategy_type import StrategyType

class CandidateGenerator:
    def generate(self,race_state,driver_number:str):
        candidates=[]
        current_lap=race_state.lap_number
        compounds=["SOFT","MEDIUM","HARD"]
        for lap_offset in range(1,6):
            target_lap=(current_lap+lap_offset)
            for compound in compounds:
                candidates.append(StrategyCandidate(
                    strategy_type=StrategyType.PIT_STOP,
                    target_lap=target_lap,
                    current_compound=compound
                ))
        candidates.append(StrategyCandidate(strategy_type=StrategyType.STAY_OUT))
        return candidates