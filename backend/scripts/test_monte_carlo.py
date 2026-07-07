from pprint import pprint

from domain.driver_state import DriverState
from domain.driver_status import DriverStatus
from domain.race_state import RaceState

from state_builder.track_status_parser import (
    TrackCondition,
)

from ml.monte_carlo.monte_carlo_simulator import (
    MonteCarloSimulator,
)

from ml.simulator.strategy import Strategy


def main():

    race_state = RaceState(

        race_id="test",

        season=2024,

        event_name="Bahrain Grand Prix",

        lap_number=20,

        total_laps=57,

        track_condition=TrackCondition.ALL_CLEAR,

        air_temp=30.0,

        track_temp=42.0,

        rainfall=False,

        drivers=[],
    )

    driver = DriverState(

        driver_number="4",

        driver_name="NOR",

        team="McLaren",

        position=5,

        status=DriverStatus.ACTIVE,

        current_compound="MEDIUM",

        current_tyre_age=18,

        stint=2,

        gap_to_leader=17.2,

        gap_ahead=2.1,

        gap_behind=1.6,

        last_lap_time=94.21,

        pit_in_this_lap=False,

        pit_out_this_lap=False,

        pit_in_time_seconds=None,

        pit_out_time_seconds=None,
    )

    strategy = Strategy(

        pit_lap=28,

        next_compound="HARD",
    )

    simulator = MonteCarloSimulator()

    result = simulator.simulate(

        race_state,

        driver,

        strategy,

        runs=1000,
    )

    print()

    print("=" * 80)
    print("MONTE CARLO RESULT")
    print("=" * 80)

    print(
        f"Expected Finish : {result.expected_finish_position}"
    )

    print(
        f"Median Finish   : {result.median_finish_position}"
    )

    print(
        f"Std Deviation   : {result.finish_position_std}"
    )

    print(
        f"P10 Finish      : {result.p10_finish_position}"
    )

    print(
        f"P90 Finish      : {result.p90_finish_position}"
    )

    print()

    print(
        f"Podium Chance   : {result.podium_probability:.2%}"
    )

    print(
        f"Points Chance   : {result.points_probability:.2%}"
    )

    print(
        f"Win Chance      : {result.win_probability:.2%}"
    )

    print()

    print("=" * 80)
    print("FINISH DISTRIBUTION")
    print("=" * 80)

    for outcome in result.distributions:

        print(

            f"P{outcome.position:<2} "

            f"{outcome.probability:.2%}"

        )

    print()

    print("=" * 80)
    print("RAW OBJECT")
    print("=" * 80)

    pprint(
        result.model_dump()
    )


if __name__ == "__main__":
    main()