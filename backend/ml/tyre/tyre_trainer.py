import pandas as pd

from catboost import CatBoostRegressor

from sklearn.metrics import mean_absolute_error


class TyreTrainer:

    def train(
        self,
        dataset_path: str,
    ):

        df = pd.read_parquet(
            dataset_path
        )

        df["gap_ahead"] = (
            df["gap_ahead"]
            .fillna(999.0)
        )

        df["gap_behind"] = (
            df["gap_behind"]
            .fillna(999.0)
        )

        df["gap_to_leader"] = (
            df["gap_to_leader"]
            .fillna(999.0)
        )

        df["baseline_pace"] = (
            df["baseline_pace"]
            .fillna(
                df["baseline_pace"].median()
            )
        )

        df["track_temp"] = (
            df["track_temp"]
            .fillna(
                df["track_temp"].median()
            )
        )

        df["air_temp"] = (
            df["air_temp"]
            .fillna(
                df["air_temp"].median()
            )
        )
        df["rainfall"] = (
            df["rainfall"]
            .fillna(0)
        )

        df["race_progress"] = (
            df["race_progress"]
            .fillna(0)
        )

        df["tyre_life_ratio"] = (
            df["tyre_life_ratio"]
            .fillna(0)
        )

        df = df.dropna(
            subset=[
                "season",
                "circuit_name",
                "current_compound",
                "current_tyre_age",
                "lap_in_stint",
                "lap_number",
                "laps_remaining",
                "stint",
                "position",
                "degradation_seconds",
            ]
        )

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

        target = (
            "degradation_seconds"
        )

        train_df = df[
            df["season"] <= 2022
        ]

        test_df = df[
            df["season"] >= 2023
        ]

        print()
        print(
            f"Train rows: {len(train_df)}"
        )

        print(
            f"Test rows: {len(test_df)}"
        )

        print()
        print(
            "TRAIN SEASONS"
        )

        print(
            train_df["season"]
            .value_counts()
            .sort_index()
        )

        print()
        print(
            "TEST SEASONS"
        )

        print(
            test_df["season"]
            .value_counts()
            .sort_index()
        )

        X_train = train_df[
            features
        ]

        y_train = train_df[
            target
        ]

        X_test = test_df[
            features
        ]

        y_test = test_df[
            target
        ]

        model = CatBoostRegressor(
            iterations=2000,
            depth=8,
            learning_rate=0.03,
            loss_function="RMSE",
            eval_metric="MAE",
            random_seed=42,
            verbose=100,
        )

        model.fit(
            X_train,
            y_train,
            cat_features=[
                "circuit_name",
                "current_compound",
                "driver_number",
            ],
        )

        predictions = model.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        print()
        print(
            f"MAE: {mae:.4f}"
        )

        print()
        print(
            "FEATURE IMPORTANCE"
        )
        print()

        importance = (
            model.get_feature_importance()
        )

        importance_df = pd.DataFrame(
            {
                "feature": features,
                "importance": importance,
            }
        ).sort_values(
            "importance",
            ascending=False,
        )

        print(
            importance_df
        )

        print()
        print(
            "TOP FEATURES"
        )
        print()

        for _, row in (
            importance_df.head(10)
            .iterrows()
        ):
            print(
                f"{row['feature']}: "
                f"{row['importance']:.2f}"
            )

        errors = (
            pd.Series(
                predictions,
                index=y_test.index,
            )
            - y_test
        ).abs()

        print()
        print(
            "ERROR DISTRIBUTION"
        )

        print(
            errors.describe()
        )

        print()
        print(
            "ERROR PERCENTILES"
        )

        for p in [
            50,
            75,
            90,
            95,
            99,
        ]:
            print(
                f"P{p}: "
                f"{errors.quantile(p/100):.3f}"
            )

        results = (
            X_test.copy()
        )

        results["actual"] = (
            y_test
        )

        results["predicted"] = (
            predictions
        )

        results["error"] = (
            errors
        )

        print()
        print(
            "WORST 25 PREDICTIONS"
        )

        print(
            results
            .sort_values(
                "error",
                ascending=False,
            )
            .head(25)
        )
        print()
        print(
            "WORST RACES"
        )

        worst = (
            results
            .sort_values(
                "error",
                ascending=False,
            )
            .head(500)
        )

        print(
            worst.groupby(
                "circuit_name"
            )
            .size()
            .sort_values(
                ascending=False,
            )
        )

        return (
            model,
            mae,
            X_test,
            y_test,
            predictions,
        )