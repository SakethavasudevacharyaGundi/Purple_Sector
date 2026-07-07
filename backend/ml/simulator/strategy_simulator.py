import pandas as pd

from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy import Strategy

from ml.simulator.simulation_result import (
    SimulationResult,
)

from ml.simulator.simulation_components import (
    SimulationComponents,
)

from ml.simulator.model_loader import (
    ModelLoader,
)

from ml.simulator.tyre_projection_engine import (
    TyreProjectionEngine,
)

from ml.simulator.overtake_simulator import (
    OvertakeSimulator,
)


class StrategySimulator:

    def __init__(self):

        self.models = (
            ModelLoader()
        )

        self.tyre_projection = (
            TyreProjectionEngine()
        )

        self.overtake_simulator = (
            OvertakeSimulator()
        )
    def simulate_components(

        self,

        race_state: RaceState,

        driver: DriverState,

        strategy: Strategy,

    ) -> SimulationComponents:

        pit_loss_features = pd.DataFrame(
            [
                {
                    "season": race_state.season,

                    "circuit_name":
                    race_state.event_name,

                    "track_temp":
                    race_state.track_temp,

                    "air_temp":
                    race_state.air_temp,

                    "rainfall":
                    int(
                        race_state.rainfall
                    ),

                    "track_condition":
                    race_state.track_condition.value,
                }
            ]
        )

        pit_loss = float(

            self.models
            .pit_loss_model
            .predict(
                pit_loss_features
            )[0]

        )

        rejoin_features = pd.DataFrame(
            [
                {
                    "season": 2024,

                    "event_name":
                    race_state.event_name,

                    "driver_number":
                    driver.driver_number,

                    "lap_number":
                    strategy.pit_lap,

                    "position_before_pit":
                    driver.position,

                    "gap_to_leader":
                    driver.gap_to_leader,

                    "pit_loss_seconds":
                    pit_loss,
                }
            ]
        )

        rejoin_position = float(

            self.models
            .rejoin_model
            .predict(
                rejoin_features
            )[0]

        )

        traffic_features = pd.DataFrame(
            [
                {
                    "season": 2024,

                    "event_name":
                    race_state.event_name,

                    "driver_number":
                    driver.driver_number,

                    "lap_number":
                    strategy.pit_lap,

                    "rejoin_position":
                    rejoin_position,

                    "gap_ahead":
                    driver.gap_ahead,

                    "gap_behind":
                    driver.gap_behind,

                    "current_compound":
                    strategy.next_compound,

                    "current_tyre_age":
                    1,
                }
            ]
        )

        traffic_loss = float(

            self.models
            .traffic_loss_model
            .predict(
                traffic_features
            )[0]

        )

        degradation_seconds = (

            self.tyre_projection
            .project(
                race_state,
                driver,
                strategy,
            )

        )

        expected_overtakes = (

            self.overtake_simulator
            .simulate(

                race_state,

                driver,

                strategy,

            )

        )

        # print()
        # print("COMPONENTS")
        # print()
        # print(
        #     f"Pit Loss: {pit_loss:.2f}"
        # )
        # print(
        #     f"Rejoin Position: {rejoin_position:.2f}"
        # )
        # print(
        #     f"Traffic Loss: {traffic_loss:.2f}"
        # )
        # print(
        #     f"Degradation Seconds: {degradation_seconds:.2f}"
        # )
        # print(
        #     f"Expected Overtakes: {expected_overtakes:.2f}"
        # )
        # print()

        return SimulationComponents(

            pit_loss=round(
                pit_loss,
                2,
            ),

            rejoin_position=round(
                rejoin_position,
                2,
            ),

            traffic_loss=round(
                traffic_loss,
                2,
            ),

            average_pace=0.0,

            degradation_seconds=
            round(
                degradation_seconds,
                2,
            ),

            expected_overtakes=
            round(
                expected_overtakes,
                2,
            ),
        )

    def simulate(

        self,

        race_state: RaceState,

        driver: DriverState,

        strategy: Strategy,

    ) -> SimulationResult:

        components = (
            self.simulate_components(
                race_state,
                driver,
                strategy,
            )
        )

        finish_position = (

            components.rejoin_position

            +

            components.traffic_loss

            -

            components.expected_overtakes

        )

        return SimulationResult(

            expected_pit_loss=
            components.pit_loss,

            expected_rejoin_position=
            components.rejoin_position,

            expected_traffic_loss=
            components.traffic_loss,

            expected_finish_position=
            round(
                finish_position,
                2,
            ),

            expected_average_pace=
            components.average_pace,

            expected_degradation_seconds=
            components.degradation_seconds,

            expected_overtakes=
            components.expected_overtakes,
        )