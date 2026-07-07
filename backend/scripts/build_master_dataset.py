# backend/ml/build_master_dataset.py

from pathlib import Path
import pandas as pd


def main():

    season_dir = Path(
        "data/ml/v1/seasons"
    )

    season_files = sorted(
        season_dir.glob(
            "season_*.parquet"
        )
    )

    if not season_files:
        raise ValueError(
            "No season files found"
        )

    dfs = []

    for file in season_files:

        df = pd.read_parquet(file)

        print(
            f"Loading {file.name}: "
            f"{df.shape}"
        )

        dfs.append(df)

    master_df = pd.concat(
        dfs,
        ignore_index=True
    )

    print("\nMASTER DATASET")

    print(master_df.shape)

    print(
        master_df["season"]
        .value_counts()
        .sort_index()
    )

    output_path = (
        "data/ml/v1/master_dataset.parquet"
    )

    master_df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"\nSaved: {output_path}"
    )


if __name__ == "__main__":
    main()