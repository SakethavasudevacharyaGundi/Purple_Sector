from pathlib import Path

from catboost import (
    CatBoostRegressor,
    CatBoostClassifier,
)


class ModelLoader:

    def __init__(self):

        model_dir = Path(
            "data/ml/models"
        )

        self.pit_loss_model = (
            CatBoostRegressor()
        )

        self.pit_loss_model.load_model(
            model_dir / "pit_loss_model.cbm"
        )

        self.rejoin_model = (
            CatBoostRegressor()
        )

        self.rejoin_model.load_model(
            model_dir / "rejoin_position_model.cbm"
        )

        self.traffic_loss_model = (
            CatBoostRegressor()
        )

        self.traffic_loss_model.load_model(
            model_dir / "traffic_loss_model.cbm"
        )

        self.tyre_model = (
            CatBoostRegressor()
        )

        self.tyre_model.load_model(
            model_dir / "tyre_model.cbm"
        )

        self.overtake_model = (
            CatBoostClassifier()
        )

        self.overtake_model.load_model(
            model_dir / "overtake_model.cbm"
        )