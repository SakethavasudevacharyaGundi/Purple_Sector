from ingestion.fastf1_client import FastF1Client
from state_builder.gap_calculator import GapCalculator

client = FastF1Client()

session = client.get_session(
    season=2024,
    grand_prix="Monaco Grand Prix",
    session_type="R"
)

lap20 = session.laps[
    session.laps["LapNumber"] == 20
]

calculator = GapCalculator()

result = calculator.calculate(lap20)
print("\nCALCULATED GAPS\n")

for driver, gaps in list(result.items())[:5]:
    print(
        f"{driver} | "
        f"Leader={gaps['gap_to_leader']} | "
        f"Ahead={gaps['gap_ahead']} | "
        f"Behind={gaps['gap_behind']}"
    )

print("\nRAW TIMING DATA\n")

print(
    lap20[
        ["Driver", "Position", "Time"]
    ]
    .sort_values("Position")
    .head(5)
)