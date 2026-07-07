# scripts/debug_lap1.py

from ingestion.fastf1_client import FastF1Client

client = FastF1Client()

session = client.get_session(
    season=2024,
    grand_prix="Monaco Grand Prix",
    session_type="R",
)

lap1 = session.laps[
    session.laps["LapNumber"] == 1
]

print(
    lap1[
        [
            "Driver",
            "LapTime",
            "Time",
            "LapStartTime",
            "Position",
        ]
    ]
)
