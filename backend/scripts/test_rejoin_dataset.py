from pathlib import Path

from ml.traffic.rejoin_dataset_builder import (
    RejoinDatasetBuilder,
)

builder = RejoinDatasetBuilder()

df = builder.build(
    "data/ml/v1/master_dataset.parquet"
)

print()
print("ROWS")
print(len(df))

print()
print("HEAD")
print(df.head())

print()
print("DESCRIBE")
print(
    df[
        [
            "position_before_pit",
            "actual_rejoin_position",
            "pit_loss_seconds",
        ]
    ].describe()
)

print()
print("PIT LOSS PERCENTILES")
print(
    df["pit_loss_seconds"]
    .describe(
        percentiles=[
            0.50,
            0.75,
            0.90,
            0.95,
            0.99,
        ]
    )
)

print()
print("BEST PIT LOSSES")
print(
    df.sort_values(
        "pit_loss_seconds",
        ascending=True,
    )
    .head(20)
)

print()
print("WORST PIT LOSSES")
print(
    df.sort_values(
        "pit_loss_seconds",
        ascending=False,
    )
    .head(20)
)

print()
print("REJOIN POSITION DISTRIBUTION")
print(
    df["actual_rejoin_position"]
    .value_counts()
    .sort_index()
)

print()
print("PIT LOSS BY CIRCUIT")
print(
    df.groupby(
        "event_name"
    )["pit_loss_seconds"]
    .agg(
        [
            "count",
            "mean",
            "std",
            "min",
            "max",
        ]
    )
    .sort_values(
        "count",
        ascending=False,
    )
)

print()
print("POSITION CHANGE")

position_change = (
    df["actual_rejoin_position"]
    - df["position_before_pit"]
)

print(
    position_change.describe(
        percentiles=[
            0.50,
            0.75,
            0.90,
            0.95,
            0.99,
        ]
    )
)

print()
print("LARGEST POSITION LOSSES")

tmp = df.copy()

tmp["position_change"] = (
    tmp["actual_rejoin_position"]
    - tmp["position_before_pit"]
)

print(
    tmp.sort_values(
        "position_change",
        ascending=False,
    )
    .head(20)
)

# ---------------------------------
# SAVE DATASET
# ---------------------------------

output_path = Path(
    "data/ml/v1/rejoin_dataset.parquet"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

df.to_parquet(
    output_path,
    index=False,
)

print()
print("DATASET SAVED")
print(output_path)

print()
print("FILE EXISTS")
print(output_path.exists())

print()
print("FINAL SHAPE")
print(df.shape)