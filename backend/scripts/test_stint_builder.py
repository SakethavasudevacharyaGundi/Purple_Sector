import pandas as pd

from ml.stint_builder import (
    StintDatasetBuilder,
)

df = pd.read_parquet(
    "data/ml/v1/master_dataset.parquet"
)

builder = (
    StintDatasetBuilder()
)

stint_df = builder.build(
    df
)

print()

print(
    stint_df[
        [
            "driver_number",
            "lap_number",
            "stint",
            "current_compound",
            "current_tyre_age",
            "current_lap_time",
            "stint_best_lap",
            "degradation_seconds",
        ]
    ]
    .head(30)
)