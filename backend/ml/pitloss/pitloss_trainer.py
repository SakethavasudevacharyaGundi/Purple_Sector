import pandas as pd

from catboost import (
    CatBoostRegressor,
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


class PitLossTrainer:

    def train(
        self,
        dataset_path: str,
    ):

        df = pd.read_parquet(
            dataset_path
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
            .fillna(False)
            .astype(int)
        )

        df["track_condition"] = (
            df["track_condition"]
            .fillna("GREEN")
        )

        df = df.dropna(
            subset=[
                "season",
                "circuit_name",
                "pit_loss_seconds",
            ]
        )

        print()
        print(
            "PIT LOSS CIRCUIT SUMMARY"
        )

        print(
            df.groupby(
                "circuit_name"
            )["pit_loss_seconds"]
            .agg(
                [
                    "count",
                    "mean",
                    "std",
                ]
            )
            .sort_values(
                "count",
                ascending=False,
            )
        )

        features = [

            "season",

            "circuit_name",

            "track_temp",

            "air_temp",

            "rainfall",

            "track_condition",
        ]

        target = (
            "pit_loss_seconds"
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

            iterations=1000,

            depth=5,

            learning_rate=0.05,

            l2_leaf_reg=5,

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
                "track_condition",
            ]
        )

        predictions = (
            model.predict(
                X_test
            )
        )

        mae = (
            mean_absolute_error(
                y_test,
                predictions,
            )
        )

        rmse = (
            mean_squared_error(
                y_test,
                predictions,
            )
            ** 0.5
        )

        r2 = (
            r2_score(
                y_test,
                predictions,
            )
        )

        print()
        print(
            f"PIT LOSS MAE: {mae:.4f}"
        )

        print(
            f"PIT LOSS RMSE: {rmse:.4f}"
        )

        print(
            f"PIT LOSS R²: {r2:.4f}"
        )

        print()
        print(
            "FEATURE IMPORTANCE"
        )
        print()

        importance_df = pd.DataFrame(
            {
                "feature": features,
                "importance":
                model.get_feature_importance(),
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
            importance_df
            .head(10)
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
            "WORST CIRCUITS"
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