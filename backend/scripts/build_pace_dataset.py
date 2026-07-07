from pathlib import Path

import pandas as pd

from ml.pace.pace_target_builder import (
    PaceTargetBuilder,
)


def main():

    df = pd.read_parquet(
        "data/ml/v1/tyre_dataset.parquet"
    )

    builder = PaceTargetBuilder()

    pace_df = builder.build(df)

    output_path = Path(
        "data/ml/v1/pace_dataset.parquet"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    pace_df.to_parquet(
        output_path,
        index=False,
    )

    print()
    print(
        f"Saved: {output_path}"
    )


if __name__ == "__main__":
    main()