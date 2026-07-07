import pandas as pd

from catboost import (
    CatBoostClassifier,
)

from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
)


class OvertakeTrainer:

    def train(
        self,
        dataset_path: str,
    ):

        df = pd.read_parquet(
            dataset_path
        )

        numeric_cols = [
            "gap_ahead",
            "gap_behind",
            "gap_to_leader",
            "current_tyre_age",
            "current_lap_time",
            "lap_time_delta",
            "laps_remaining",
            "stint",
            "driver_elo",
        ]

        for col in numeric_cols:

            if col in df.columns:

                df[col] = (
                    df[col]
                    .fillna(
                        df[col].median()
                    )
                )

        features = [

            "season",

            "event_name",

            "driver_number",

            "lap_number",

            "position",

            "gap_ahead",

            "gap_behind",

            "gap_to_leader",

            "current_compound",

            "current_tyre_age",

            "stint",

            "track_condition",

            "current_lap_time",

            "lap_time_delta",

            "laps_remaining",

            "drs_zone",

            "attack_zone",

            "compound_age",

            "driver_elo",
        ]

        target = (
            "overtake_happened"
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

        model = CatBoostClassifier(

            iterations=1200,

            depth=7,

            learning_rate=0.04,

            loss_function="Logloss",

            eval_metric="AUC",

            random_seed=42,

            verbose=100,
        )

        model.fit(

            X_train,

            y_train,

            cat_features=[

                "event_name",

                "driver_number",

                "current_compound",

                "track_condition",

                "compound_age",
            ]
        )

        probabilities = (
            model.predict_proba(
                X_test
            )[:, 1]
        )

        predictions = (
            probabilities >= 0.5
        ).astype(int)

        auc = (
            roc_auc_score(
                y_test,
                probabilities,
            )
        )

        precision = (
            precision_score(
                y_test,
                predictions,
            )
        )

        recall = (
            recall_score(
                y_test,
                predictions,
            )
        )

        print()
        print(
            f"AUC: {auc:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall: {recall:.4f}"
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

        return (
            model,
            auc,
        )