from domain.race_state import (
    RaceState,
)

from domain.driver_state import (
    DriverState,
)

from state_builder.track_status_parser import (
    TrackCondition,
)

from ml.simulator.strategy import (
    Strategy,
)

from ml.simulator.strategy_simulator import (
    StrategySimulator,
)


race_state = RaceState(

    race_id="1",

    season=2024,

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

    pit_lap=22,

    next_compound="HARD",
)

simulator = (
    StrategySimulator()
)

result = simulator.simulate(

    race_state,

    driver,

    strategy,
)

print()
print(result)