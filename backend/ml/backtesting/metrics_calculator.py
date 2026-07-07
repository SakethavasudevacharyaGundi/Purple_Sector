import pandas as pd


class MetricsCalculator:

    def calculate(

        self,

        results_df: pd.DataFrame,

    ) -> dict:

        mae = float(

            results_df[
                "error"
            ].mean()

        )

        rmse = float(

            (
                results_df[
                    "error"
                ] ** 2
            )
            .mean()
            ** 0.5

        )

        median_error = float(

            results_df[
                "error"
            ].median()

        )

        p90_error = float(

            results_df[
                "error"
            ].quantile(
                0.90
            )

        )

        return {

            "mae":
            round(mae, 3),

            "rmse":
            round(rmse, 3),

            "median_error":
            round(
                median_error,
                3,
            ),

            "p90_error":
            round(
                p90_error,
                3,
            ),
        }