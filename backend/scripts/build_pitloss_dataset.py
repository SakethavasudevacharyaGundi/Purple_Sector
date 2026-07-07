from pathlib import Path

import pandas as pd

from ml.pitloss.pitloss_dataset_builder import (
    PitLossDatasetBuilder,
)


def main():

    df = pd.read_parquet(
        "data/ml/v1/master_dataset.parquet"
    )

    builder = (
        PitLossDatasetBuilder()
    )

    pit_df = builder.build(df)

    output_path = Path(
        "data/ml/v1/pit_loss_dataset.parquet"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    pit_df.to_parquet(
        output_path,
        index=False,
    )

    print()
    print(
        f"Saved: {output_path}"
    )
    pit_df.groupby(
        "circuit_name"
    )["pit_loss_seconds"].agg(
        [
            "count",
            "mean",
            "std",
        ]
    )
if __name__ == "__main__":
    main()