import fastf1
from pathlib import Path
#so that we can use the different files as objects by not defining the entire system path

class FastF1Client:

    def __init__(self)->None:
        #setting up objects initial states returning none as its just setting up the client
        cache_dir= Path("data/raw/cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        fastf1.Cache.enable_cache(str(cache_dir))

    def get_session(
            self,
            season:int,
            grand_prix:str,
            session_type:str="R"
    ):
        """
        session_type:
            R=Race
            Q=Qualifying
            FP1=Free Practice 1
            FP2=Free Practice 2
            FP3=Free Practice 3
        """
        session = fastf1.get_session(season, grand_prix, session_type)
        session.load()
        return session
    def get_schedule(self,season:int):
        return fastf1.get_event_schedule(season)
    
    