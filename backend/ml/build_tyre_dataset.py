import pandas as pd

from ml.tyre_target_builder import (
    TyreTargetBuilder,
)


def main():

    df = pd.read_parquet(
        "data/ml/v1/master_dataset.parquet"
    )

    builder = TyreTargetBuilder()

    tyre_df = builder.build(df)

    print()
    print("SHAPE")
    print(tyre_df.shape)

    print()
    print("TARGET")
    print(
        tyre_df[
            "degradation_seconds"
        ].describe()
    )

    print()
    print("CORRELATION")

    corr = (
        tyre_df[
            "current_tyre_age"
        ].corr(
            tyre_df[
                "degradation_seconds"
            ]
        )
    )

    print(corr)

    print()
    print("MEAN BY TYRE AGE")

    print(
        tyre_df.groupby(
            "current_tyre_age"
        )[
            "degradation_seconds"
        ]
        .mean()
        .head(40)
    )

    tyre_df.to_parquet(
        "data/ml/v1/tyre_dataset.parquet",
        index=False,
    )

    print()
    print(
        "Saved: data/ml/v1/tyre_dataset.parquet"
    )


if __name__ == "__main__":
    main()