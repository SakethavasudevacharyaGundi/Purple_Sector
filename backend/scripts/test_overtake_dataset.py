from ml.traffic.overtake_dataset_builder import (
    OvertakeDatasetBuilder,
)


builder = (
    OvertakeDatasetBuilder()
)

df = builder.build(
    "data/ml/v1/master_dataset.parquet"
)

print()
print("ROWS")
print(len(df))

print()

print(
    df.head()
)

print()

print(
    "CLASS BALANCE"
)

print(
    df["overtake_happened"]
    .value_counts()
)

print()

print(
    "OVERTAKE RATE"
)

print(
    df["overtake_happened"]
    .mean()
)