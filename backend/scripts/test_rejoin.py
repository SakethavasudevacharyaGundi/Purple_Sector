import pandas as pd

df = pd.read_parquet(
    "data/ml/features/driver_elo.parquet"
)

print()
print("=" * 80)
print("FIRST 50 ROWS")
print("=" * 80)

print(
    df.head(50)
)

print()
print("=" * 80)
print("FIRST 20 RACES")
print("=" * 80)

print(

    df[
        [
            "season",
            "event_name",
        ]
    ]

    .drop_duplicates()

    .head(20)

)