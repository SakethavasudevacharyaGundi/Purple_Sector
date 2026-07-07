from pathlib import Path

import pandas as pd

from catboost import CatBoostRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def main():

    model_path = Path(
        "data/ml/models/tyre_model.cbm"
    )

    dataset_path = Path(
        "data/ml/v1/tyre_dataset.parquet"
    )

    model = CatBoostRegressor()
    model.load_model(model_path)

    df = pd.read_parquet(
        dataset_path
    )

    test_df = df[
        df["season"] >= 2023
    ].copy()

    features = [

        "season",

        "circuit_name",

        "driver_number",

        "current_compound",
        "current_tyre_age",

        "lap_in_stint",

        "lap_number",
        "laps_remaining",
        "stint",

        "position",

        "gap_ahead",
        "gap_behind",
        "gap_to_leader",

        "track_temp",
        "air_temp",

        "rainfall",

        "baseline_pace",

        "race_progress",
        "tyre_life_ratio",
    ]

    test_df["gap_ahead"] = (
        test_df["gap_ahead"]
        .fillna(999.0)
    )

    test_df["gap_behind"] = (
        test_df["gap_behind"]
        .fillna(999.0)
    )

    test_df["gap_to_leader"] = (
        test_df["gap_to_leader"]
        .fillna(999.0)
    )

    X_test = test_df[
        features
    ]

    y_test = test_df[
        "degradation_seconds"
    ]

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = (
        mean_squared_error(
            y_test,
            predictions,
        )
        ** 0.5
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    print()
    print("OVERALL METRICS")
    print(
        f"MAE:  {mae:.4f}"
    )
    print(
        f"RMSE: {rmse:.4f}"
    )
    print(
        f"R²:   {r2:.4f}"
    )

    test_df["prediction"] = (
        predictions
    )

    print()
    print(
        "COMPOUND MAE"
    )

    for compound in [
        "SOFT",
        "MEDIUM",
        "HARD",
    ]:

        subset = test_df[
            test_df[
                "current_compound"
            ]
            == compound
        ]

        if len(subset) == 0:
            continue

        compound_mae = (
            mean_absolute_error(
                subset[
                    "degradation_seconds"
                ],
                subset[
                    "prediction"
                ],
            )
        )

        print(
            f"{compound}: "
            f"{compound_mae:.4f}"
        )

    print()
    print(
        "AGE-BUCKET MAE"
    )

    test_df["age_bucket"] = pd.cut(
        test_df[
            "current_tyre_age"
        ],
        bins=[
            4,
            10,
            20,
            30,
            40,
        ],
    )

    for bucket, bucket_df in (
        test_df.groupby(
            "age_bucket"
        )
    ):

        bucket_mae = (
            mean_absolute_error(
                bucket_df[
                    "degradation_seconds"
                ],
                bucket_df[
                    "prediction"
                ],
            )
        )

        print(
            f"{bucket}: "
            f"{bucket_mae:.4f}"
        )

    print()
    print(
        "DEGRADATION CURVE CHECK"
    )

    actual_curve = (
        test_df.groupby(
            "current_tyre_age"
        )[
            "degradation_seconds"
        ]
        .mean()
    )

    predicted_curve = (
        test_df.groupby(
            "current_tyre_age"
        )[
            "prediction"
        ]
        .mean()
    )

    comparison = pd.DataFrame(
        {
            "actual":
            actual_curve,

            "predicted":
            predicted_curve,
        }
    )

    comparison["difference"] = (
        comparison["predicted"]
        -
        comparison["actual"]
    )

    print(
        comparison.head(40)
    )

    print()
    print(
        "WORST 20 ERRORS"
    )

    errors = (
        test_df["prediction"]
        -
        test_df[
            "degradation_seconds"
        ]
    ).abs()

    test_df["error"] = errors

    print(
        test_df[
            [
                "circuit_name",
                "driver_number",
                "current_compound",
                "current_tyre_age",
                "actual",
                "prediction",
                "error",
            ]
        ]
        if False
        else
        test_df.assign(
            actual=test_df[
                "degradation_seconds"
            ]
        )[
            [
                "circuit_name",
                "driver_number",
                "current_compound",
                "current_tyre_age",
                "actual",
                "prediction",
                "error",
            ]
        ]
        .sort_values(
            "error",
            ascending=False,
        )
        .head(20)
    )


if __name__ == "__main__":
    main()