from pathlib import Path

from ml.traffic.traffic_loss_dataset_builder import (
    TrafficLossDatasetBuilder,
)


builder = (
    TrafficLossDatasetBuilder()
)

df = builder.build(
    "data/ml/v1/master_dataset.parquet"
)

output = Path(
    "data/ml/v1/traffic_loss_dataset.parquet"
)

df.to_parquet(
    output,
    index=False,
)

print()
print("ROWS")
print(len(df))

print()
print(df.head())

print()
print(
    df["traffic_loss"]
    .describe()
)

print()
print(
    f"Saved: {output}"
)