import pandas as pd

df = pd.read_parquet(
    "data/ml/v1/master_dataset.parquet"
)

print(
    df[df["season"] == 2024][
        [
            "pit_in_time_seconds",
            "pit_out_time_seconds",
        ]
    ]
    .notna()
    .sum()
)