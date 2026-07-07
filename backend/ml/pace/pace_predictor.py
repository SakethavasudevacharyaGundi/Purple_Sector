from catboost import (
    CatBoostRegressor,
)


class PacePredictor:

    def __init__(
        self,
        model_path: str,
    ):

        self.model = (
            CatBoostRegressor()
        )

        self.model.load_model(
            model_path
        )

    def predict(
        self,
        features,
    ):

        return self.model.predict(
            features
        )