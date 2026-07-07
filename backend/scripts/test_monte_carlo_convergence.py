from domain.race_state import RaceState
from domain.driver_state import DriverState

from state_builder.track_status_parser import (
    TrackCondition,
)

from ml.simulator.strategy import (
    Strategy,
)

from ml.monte_carlo.monte_carlo_simulator import (
    MonteCarloSimulator,
)


race_state = RaceState(

    race_id="1",

    event_name=
    "Bahrain Grand Prix",

    lap_number=20,

    total_laps=57,

    track_condition=
    TrackCondition.ALL_CLEAR,

    air_temp=28,

    track_temp=36,

    rainfall=False,

    drivers=[],
)

driver = DriverState(

    driver_number="4",

    driver_name="Norris",

    team="McLaren",

    position=5,

    current_compound="MEDIUM",

    current_tyre_age=18,

    stint=1,

    gap_ahead=1.5,

    gap_behind=2.0,

    gap_to_leader=14.5,
)

strategy = Strategy(

    pit_lap=28,

    next_compound="HARD",
)

simulator = (
    MonteCarloSimulator()
)

for runs in [

    100,

    500,

    1000,

    5000,

]:

    result = simulator.simulate(

        race_state,

        driver,

        strategy,

        runs=runs,
    )

    print()

    print(
        f"RUNS = {runs}"
    )

    print(
        f"Expected Finish: "
        f"{result.expected_finish_position}"
    )

    print(
        f"Points Probability: "
        f"{result.points_probability}"
    )

    print(
        f"Podium Probability: "
        f"{result.podium_probability}"
    )