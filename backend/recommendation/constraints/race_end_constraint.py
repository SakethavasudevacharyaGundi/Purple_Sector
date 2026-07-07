from recommendation.constraints.base_constraint import (
    BaseConstraint
)

from recommendation.constraints.constraint_result import (
    ConstraintResult
)


class RaceEndConstraint(
    BaseConstraint
):

    def validate(
        self,
        race_state,
        driver_state,
        candidate,
    ) -> ConstraintResult:

        for stop in candidate.pit_stops:

            if stop.lap <= race_state.lap_number:

                return ConstraintResult(
                    False,
                    (
                        f"Pit stop lap "
                        f"{stop.lap} "
                        f"is not in the future"
                    )
                )

            if stop.lap >= race_state.total_laps:

                return ConstraintResult(
                    False,
                    (
                        f"Pit stop lap "
                        f"{stop.lap} "
                        f"occurs after race end"
                    )
                )

        return ConstraintResult(
            True
        )