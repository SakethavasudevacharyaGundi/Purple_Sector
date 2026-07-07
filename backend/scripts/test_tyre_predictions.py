import pandas as pd

from catboost import (
    CatBoostRegressor,
)


def main():

    model = CatBoostRegressor()

    model.load_model(
        "data/ml/models/tyre_model.cbm"
    )

    rows = []

    for age in range(4, 31):

        rows.append(
            {
                # "circuit_name":
                #     "Monaco Grand Prix",

                "current_compound":
                    "SOFT",

                "current_tyre_age":
                    age,

                # "track_temp":
                #     40.0,

                # "air_temp":
                #     25.0,
            }
        )

    df = pd.DataFrame(rows)

    df["predicted_deg"] = (
        model.predict(df)
    )

    print(
        df[
            [
                "current_tyre_age",
                "predicted_deg",
            ]
        ]
    )


if __name__ == "__main__":
    main()