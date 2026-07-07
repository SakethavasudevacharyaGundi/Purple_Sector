import pandas as pd

df = pd.read_parquet(
    "data/ml/features/driver_elo.parquet"
)

print(
    df[
        ["season", "event_name"]
    ]
    .drop_duplicates()
    .head(15)
)