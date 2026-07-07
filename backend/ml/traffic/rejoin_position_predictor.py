from catboost import CatBoostRegressor


class RejoinPositionPredictor:

    def __init__(
        self,
        model_path:
        str = (
            "data/ml/models/"
            "rejoin_position_model.cbm"
        ),
    ):

        self.model = (
            CatBoostRegressor()
        )

        self.model.load_model(
            model_path
        )

    def predict(

        self,

        season: int,

        event_name: str,

        driver_number: str,

        lap_number: int,

        position_before_pit: int,

        gap_to_leader: float,

        pit_loss_seconds: float,
    ) -> int:

        prediction = (
            self.model.predict(
                [[

                    season,

                    event_name,

                    driver_number,

                    lap_number,

                    position_before_pit,

                    gap_to_leader,

                    pit_loss_seconds,
                ]]
            )[0]
        )

        return round(
            prediction
        )