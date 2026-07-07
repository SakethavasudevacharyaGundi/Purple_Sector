from domain.race_state import RaceState
from domain.driver_state import DriverState
from domain.track_condition import TrackCondition

from ml.simulator.strategy import Strategy
from ml.simulator.strategy_simulator import (
    StrategySimulator,
)

from ml.monte_carlo.monte_carlo_simulator import (
    MonteCarloSimulator,
)


def create_race_state():

    driver = create_driver(
        position=8,
    )

    return RaceState(

        race_id="TEST_RACE",

        event_name="Monza",

        lap_number=25,

        total_laps=53,

        track_condition=
        TrackCondition.ALL_CLEAR,

        air_temp=27.0,

        track_temp=38.0,

        rainfall=False,

        drivers=[driver],
    )


def create_driver(
    position: int,
    gap_ahead: float = 2.0,
    gap_behind: float = 2.0,
):

    return DriverState(

        driver_number="44",

        driver_name="Lewis Hamilton",

        team="Mercedes",

        position=position,

        current_compound="MEDIUM",

        current_tyre_age=15,

        stint=1,

        gap_ahead=gap_ahead,

        gap_behind=gap_behind,

        gap_to_leader=float(position * 4),

        last_lap_time=91.5,
    )


def print_header(title: str):

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    print()


def run_strategy(

    simulator,

    race_state,

    driver,

    strategy,

):

    result = simulator.simulate(

        race_state=race_state,

        driver=driver,

        strategy=strategy,

    )

    print(result)

    return result


def run_monte_carlo(

    simulator,

    race_state,

    driver,

    strategy,

):

    result = simulator.simulate(

        race_state=race_state,

        driver=driver,

        strategy=strategy,

        runs=1000,

    )

    print(result)

    return result


def position_sensitivity_test():

    print_header(
        "POSITION SENSITIVITY TEST"
    )

    race_state = create_race_state()

    strategy = Strategy(

        pit_lap=30,

        next_compound="HARD",
    )

    strategy_simulator = (
        StrategySimulator()
    )

    monte_carlo = (
        MonteCarloSimulator()
    )

    for position in [

        2,
        10,
        18,

    ]:

        print()
        print(
            f"POSITION = {position}"
        )
        print()

        driver = create_driver(
            position=position,
        )

        run_strategy(

            strategy_simulator,

            race_state,

            driver,

            strategy,
        )

        run_monte_carlo(

            monte_carlo,

            race_state,

            driver,

            strategy,
        )


def pit_lap_sensitivity_test():

    print_header(
        "PIT LAP SENSITIVITY TEST"
    )

    race_state = create_race_state()

    driver = create_driver(
        position=8,
    )

    monte_carlo = (
        MonteCarloSimulator()
    )

    for pit_lap in [

        15,
        20,
        25,
        30,
        35,

    ]:

        print()
        print(
            f"PIT LAP = {pit_lap}"
        )
        print()

        strategy = Strategy(

            pit_lap=pit_lap,

            next_compound="HARD",
        )

        result = run_monte_carlo(

            monte_carlo,

            race_state,

            driver,

            strategy,
        )

        print()

        print(
            f"Expected Finish: "
            f"{result.expected_finish_position}"
        )


def compound_test():

    print_header(
        "COMPOUND TEST"
    )

    race_state = create_race_state()

    driver = create_driver(
        position=8,
    )

    strategy_simulator = (
        StrategySimulator()
    )

    for compound in [

        "SOFT",

        "MEDIUM",

        "HARD",

    ]:

        print()
        print(
            f"COMPOUND = {compound}"
        )
        print()

        strategy = Strategy(

            pit_lap=30,

            next_compound=compound,
        )

        result = (
            strategy_simulator
            .simulate(
                race_state,
                driver,
                strategy,
            )
        )

        print(result)
        print()
def strategy_ranking_test():

    print_header(
        "STRATEGY RANKING TEST"
    )

    race_state = create_race_state()

    driver = create_driver(
        position=8,
    )

    monte_carlo = (
        MonteCarloSimulator()
    )

    results = []

    for pit_lap in range(

        15,
        36,

    ):

        strategy = Strategy(

            pit_lap=pit_lap,

            next_compound="HARD",
        )

        result = monte_carlo.simulate(

            race_state=race_state,

            driver=driver,

            strategy=strategy,

            runs=500,
        )

        results.append(

            (
                pit_lap,

                result.expected_finish_position,

                result.points_probability,
            )

        )

    results.sort(
        key=lambda x: x[1]
    )

    print()

    print(
        "TOP 10 STRATEGIES"
    )

    print()

    for row in results[:10]:

        print(

            f"Pit Lap: {row[0]} | "

            f"Finish: {row[1]} | "

            f"Points: {row[2]}"
        )

    print()

    print(
        "BOTTOM 10 STRATEGIES"
    )

    print()

    for row in results[-10:]:

        print(

            f"Pit Lap: {row[0]} | "

            f"Finish: {row[1]} | "

            f"Points: {row[2]}"
        )


if __name__ == "__main__":


    compound_test()

