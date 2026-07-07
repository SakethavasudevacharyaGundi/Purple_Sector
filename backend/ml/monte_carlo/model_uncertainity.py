from dataclasses import dataclass


@dataclass
class ModelUncertainty:

    pit_loss_mae: float = 0.8

    rejoin_mae: float = 0.9

    traffic_mae: float = 1.5

    tyre_mae: float = 0.15

    overtake_std: float = 0.15