import json
from pathlib import Path
from ingestion.fastf1_client import FastF1Client

class RaceDownloader:
    def __init__(self)->None:
        self.client = FastF1Client()

    def download_race(
            self,
            season:int,
            grand_prix:str,
            session_type:str="R"
    )->None:
        print(f"Downloading data for {season} {grand_prix} {session_type}")
        session = self.client.get_session(
            season=season,
            grand_prix =grand_prix,
            session_type=session_type
        )
        race_slug=(grand_prix.replace(" grand prix","").replace(" ","_").lower())
        output_dir =Path("data/raw")/str(season)/race_slug
        output_dir.mkdir(parents=True, exist_ok=True)
        self._save_metadata(session, output_dir)#_ it is only meant to be used inside this class and not called in others
        self._save_results(session, output_dir)
        self._save_laps(session, output_dir)
        self._save_weather(session,output_dir)
        print("Download Complete")

    def _save_metadata(self, session, output_dir:Path)->None:
        metadata = {
            "event_name":str(session.event["EventName"]),
            "location":str(session.event["Location"]),
            "country":str(session.event["Country"]),
            "session":str(session.name),

        }
        with open(output_dir / "session_info.json", "w") as f:
            json.dump(metadata, f, indent=4)#Add exactly 4 spaced from the left margin, lines to make it more  transalte the results to json

    def _save_results(self, session, output_dir:Path)->None:
        session.results.to_json(output_dir / "results.json", orient="records",indent=4)

    def _save_laps(self,session, output_dir:Path)->None:
        session.laps.to_parquet(output_dir / "laps.parquet", index=False)#highly compressed binary,columnar storage format suitable for time series kind of data

    def _save_weather(self, session, output_dir:Path)->None:
        session.weather_data.to_parquet(output_dir / "weather.parquet", index=False)