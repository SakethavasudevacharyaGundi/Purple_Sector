import pandas as pd

df = pd.read_parquet(
    "data/ml/v1/master_dataset.parquet"
)

print(df.shape)

print(
    df["season"]
    .value_counts()
    .sort_index()
)

df = pd.read_parquet(
    "data/ml/v1/tyre_dataset.parquet"
)

print(df.shape)

print(
    df["season"]
    .value_counts()
    .sort_index()
)