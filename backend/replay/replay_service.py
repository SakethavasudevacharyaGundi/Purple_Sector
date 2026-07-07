from replay.replay_generator import ReplayGenerator
from replay.replay_repository import ReplayRepository

class ReplayService:
    def __init__(self):
        self.generator = ReplayGenerator()
        self.repository = ReplayRepository()
    def generate_and_store(self,session):
        replay = self.generator.generate(session)
        self.repository.save(replay)
        return replay
    def get_race(self,season:int,event_name:str):
        return self.repository.load(season,event_name)
    def get_lap(self,season:int,event_name:str,lap_number:int):
        replay=self.repository.load(season,event_name)
        return replay.states[lap_number-1]