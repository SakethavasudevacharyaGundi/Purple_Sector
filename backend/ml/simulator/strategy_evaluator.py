from domain.race_state import (
    RaceState,
)

from domain.driver_state import (
    DriverState,
)

from ml.simulator.strategy import (
    Strategy,
)

from ml.simulator.strategy_simulator import (
    StrategySimulator,
)


class StrategyEvaluator:

    TOP_RECOMMENDATIONS = 5

    AVAILABLE_COMPOUNDS = [
        "SOFT",
        "MEDIUM",
        "HARD",
    ]

    def __init__(self):

        self.simulator = (
            StrategySimulator()
        )

    def evaluate(

        self,

        race_state: RaceState,

        driver: DriverState,

    ):

        strategies = []

        compounds = [

            compound

            for compound in
            self.AVAILABLE_COMPOUNDS

            if compound
            !=
            driver.current_compound
        ]

        start_lap = (

            race_state.lap_number
            + 1
        )

        end_lap = min(

            race_state.lap_number
            + 10,

            race_state.total_laps,
        )

        for pit_lap in range(

            start_lap,

            end_lap + 1,
        ):

            for compound in compounds:

                strategy = Strategy(

                    pit_lap=pit_lap,

                    next_compound=
                    compound,
                )

                result = (

                    self.simulator
                    .simulate(

                        race_state,

                        driver,

                        strategy,
                    )
                )

                strategies.append(
                    {
                        "strategy":
                        strategy,

                        "result":
                        result,
                    }
                )

        strategies.sort(

            key=lambda x: (

                x[
                    "result"
                ]
                .expected_finish_position,

                x[
                    "result"
                ]
                .expected_traffic_loss,

                x[
                    "result"
                ]
                .expected_pit_loss,
            )
        )

        return (
            strategies[
                :
                self.TOP_RECOMMENDATIONS
            ]
        )