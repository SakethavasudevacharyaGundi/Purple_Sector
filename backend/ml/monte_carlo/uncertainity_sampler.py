import random

from ml.monte_carlo.model_uncertainity import (
    ModelUncertainty,
)


class UncertaintySampler:

    def __init__(self):

        self.config = (
            ModelUncertainty()
        )

    def sample_pit_loss(
        self,
        prediction: float,
    ) -> float:

        return max(
            0.0,
            random.gauss(
                prediction,
                self.config.pit_loss_mae,
            ),
        )

    def sample_rejoin(
        self,
        prediction: float,
    ) -> float:

        return max(
            1.0,
            random.gauss(
                prediction,
                self.config.rejoin_mae,
            ),
        )

    def sample_traffic(
        self,
        prediction: float,
    ) -> float:

        return max(
            0.0,
            random.gauss(
                prediction,
                self.config.traffic_mae,
            ),
        )