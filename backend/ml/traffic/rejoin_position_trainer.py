import pandas as pd

from catboost import CatBoostRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


class RejoinPositionTrainer:

    def train(
        self,
        dataset_path: str,
    ):

        df = pd.read_parquet(
            dataset_path
        )

        df = df.dropna()

        features = [

            "season",

            "event_name",

            "driver_number",

            "lap_number",

            "position_before_pit",

            "gap_to_leader",

            "pit_loss_seconds",
        ]

        target = (
            "actual_rejoin_position"
        )

        train_df = (
            df[df["season"] <= 2022]
        )

        test_df = (
            df[df["season"] >= 2023]
        )

        print()
        print(
            f"Train rows: {len(train_df)}"
        )

        print(
            f"Test rows: {len(test_df)}"
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

            depth=6,

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
                "event_name",
                "driver_number",
            ],
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
            f"REJOIN MAE: {mae:.4f}"
        )

        print(
            f"REJOIN RMSE: {rmse:.4f}"
        )

        print(
            f"REJOIN R²: {r2:.4f}"
        )

        importance_df = pd.DataFrame(
            {
                "feature": features,
                "importance":
                model.get_feature_importance(),
            }
        )

        print()
        print(
            importance_df.sort_values(
                "importance",
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