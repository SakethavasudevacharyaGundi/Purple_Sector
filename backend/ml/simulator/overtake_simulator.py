import copy
import random

from domain.race_state import RaceState
from domain.driver_state import DriverState

from ml.simulator.strategy import Strategy

from ml.simulator.overtake_projection_engine import (
    OvertakeProjectionEngine,
)


class OvertakeSimulator:


    RANDOM_SEED = 42

    def __init__(self):

        self.projection_engine = (
            OvertakeProjectionEngine()
        )

        self.random = random.Random(
            self.RANDOM_SEED
        )

    def simulate(

    self,

    race_state: RaceState,

    driver: DriverState,

    strategy: Strategy,

) -> float:

        return float(

            self._simulate_once(

                race_state,

                driver,

                strategy,

            )

        )

    def _simulate_once(

        self,

        race_state: RaceState,

        driver: DriverState,

        strategy: Strategy,

    ) -> int:

        simulated_race = copy.deepcopy(
            race_state
        )

        simulated_driver = copy.deepcopy(
            driver
        )

        self._apply_pit_stop(

            simulated_driver,

            strategy,

        )

        overtakes = 0

        simulated_race.lap_number = (
            strategy.pit_lap
        )

        while (

            simulated_race.lap_number
            <=
            simulated_race.total_laps

        ):

            probability = (

                self.projection_engine
                .predict_probability(

                    simulated_race,

                    simulated_driver,

                )

            )

            if (

                self.random.random()
                <
                probability

            ):

                overtakes += 1

                self._apply_overtake(

                    simulated_driver,

                )

            self._advance_lap(

                simulated_race,

                simulated_driver,

            )

        return overtakes

    def _apply_pit_stop(

        self,

        driver: DriverState,

        strategy: Strategy,

    ) -> None:

        driver.current_compound = (
            strategy.next_compound
        )

        driver.current_tyre_age = 1

        if driver.stint is None:

            driver.stint = 1

        else:

            driver.stint += 1

    def _apply_overtake(

        self,

        driver: DriverState,

    ) -> None:

        if (

            driver.position
            is not None

        ):

            driver.position = max(

                1,

                driver.position
                - 1,

            )

        if (

            driver.gap_ahead
            is not None

            and

            driver.gap_behind
            is not None

        ):

            previous_gap = (
                driver.gap_ahead
            )

            driver.gap_ahead = max(

                0.5,

                previous_gap
                +
                0.75,

            )

            driver.gap_behind = (
                previous_gap
            )

            driver.gap_to_leader = max(

                0.0,

                driver.gap_to_leader
                -
                previous_gap,

            )

    def _advance_lap(

        self,

        race_state: RaceState,

        driver: DriverState,

    ) -> None:

        race_state.lap_number += 1

        if (

            driver.current_tyre_age
            is not None

        ):

            driver.current_tyre_age += 1

        if (

            driver.last_lap_time
            is not None

        ):

            driver.last_lap_time += 0.03

        if (

            driver.gap_ahead
            is not None

        ):

            driver.gap_ahead += 0.05

        if (

            driver.gap_behind
            is not None

        ):

            driver.gap_behind += 0.05

        if (

            driver.gap_to_leader
            is not None

        ):

            driver.gap_to_leader += 0.05