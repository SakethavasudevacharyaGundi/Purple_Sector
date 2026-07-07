from ingestion.fastf1_client import FastF1Client

from state_builder.state_builder import StateBuilder

from recommendation.constraints.current_tyre_constraint import (
    CurrentTyreConstraint,
)

from recommendation.strategy_candidate import (
    StrategyCandidate,
)

from recommendation.strategy_type import (
    StrategyType,
)

from recommendation.pit_stop import (
    Pitstop,
)


def main():

    client = FastF1Client()

    session = client.get_session(
        season=2024,
        grand_prix="Monaco Grand Prix",
        session_type="R",
    )

    state = StateBuilder().build_state(
        session=session,
        lap_number=20,
    )

    driver = next(
        d
        for d in state.drivers
        if d.driver_number == "16"
    )

    print("\nORIGINAL DRIVER\n")
    print(driver)

    #
    # Simulate fresh tyres
    #

    driver.current_tyre_age = 1

    candidate = StrategyCandidate(
        strategy_type=StrategyType.ONE_STOP,
        pit_stops=[
            Pitstop(
                lap=21,
                compound="HARD",
            )
        ],
    )

    constraint = CurrentTyreConstraint()

    result = constraint.validate(
        race_state=state,
        driver_state=driver,
        candidate=candidate,
    )

    print("\nRESULT\n")

    print(
        f"Valid={result.is_valid}"
    )

    print(
        f"Reason={result.reason}"
    )


if __name__ == "__main__":
    main()