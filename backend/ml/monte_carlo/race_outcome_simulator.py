import random

from ml.simulator.simulation_components import (
    SimulationComponents,
)

from ml.monte_carlo.uncertainity_sampler import (
    UncertaintySampler,
)


class RaceOutcomeSimulator:

    POSITION_SECONDS = 5.0

    def __init__(self):

        self.sampler = (
            UncertaintySampler()
        )

    def simulate(

        self,

        components: SimulationComponents,

    ) -> int:

        sampled_pit_loss = (

            self.sampler
            .sample_pit_loss(
                components.pit_loss
            )

        )

        sampled_rejoin = (

            self.sampler
            .sample_rejoin(
                components.rejoin_position
            )

        )

        sampled_traffic = (

            self.sampler
            .sample_traffic(
                components.traffic_loss
            )

        )

        degradation_effect = (

            components.degradation_seconds

            /

            self.POSITION_SECONDS

        )

        degradation_effect += random.gauss(
            0,
            0.15,
        )

        overtake_gain = (

            components.expected_overtakes

        )

        overtake_gain += random.gauss(
            0,
            0.25,
        )

        finish_position = (

            sampled_rejoin

            +

            sampled_traffic

            +

            degradation_effect

            -

            overtake_gain

        )

        finish_position += random.gauss(
            0,
            0.3,
        )

        finish_position = round(
            finish_position
        )

        finish_position = max(
            1,
            min(
                20,
                finish_position,
            ),
        )

        return finish_position