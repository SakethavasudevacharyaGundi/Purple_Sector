#session to racestate stream
from replay.replay_model import RaceReplay
from state_builder.state_builder import StateBuilder

class ReplayGenerator:
    def __init__(self):
        self.state_builder = StateBuilder()
    
    def generate(self,session)->RaceReplay:
        max_lap=session.laps["LapNumber"].dropna().max()
        if(max_lap is None):
            raise ValueError("No lap data available for this session")
        total_laps = int(max_lap)
        states=[]
        for lap in range(1,total_laps+1):
            state = self.state_builder.build_state(
                session=session,
                lap_number=lap,
            )
            states.append(state)
        return RaceReplay(
            season=int(session.event["EventDate"].year),
            event_name=str(session.event["EventName"]),
            total_laps=total_laps,
            states=states,
        )