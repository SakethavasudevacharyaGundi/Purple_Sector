import pandas as pd

from ml.elo.elo_feature_enricher import (
    EloFeatureEnricher,
)

df = pd.read_parquet(
    "data/ml/v1/pace_dataset.parquet"
)

print()
print("Before")
print(df.columns.tolist())

enricher = (
    EloFeatureEnricher()
)

df = enricher.enrich(df)

print()
print("After")
print(df.columns.tolist())

print()

print(
    df[
        [
            "season",
            "event_name",
            "driver_number",
            "driver_elo",
        ]
    ].head()
)

print()

print(
    df["driver_elo"]
    .describe()
)