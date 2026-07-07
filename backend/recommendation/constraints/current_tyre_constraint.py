from recommendation.constraints.base_constraint import BaseConstraint
from recommendation.constraints.constraint_result import ConstraintResult
from recommendation.tyre_profiles import TYRE_PROFILES

class CurrentTyreConstraint(
    BaseConstraint
):

    def validate(
        self,
        race_state,
        driver_state,
        candidate,
    )->ConstraintResult:
        if not candidate.pit_stops:
            return ConstraintResult(is_valid=True)
        first_stop=candidate.pit_stops[0]
        profile=TYRE_PROFILES[driver_state.current_compound]
        projected_stint_length=(driver_state.current_tyre_age)+(first_stop.lap-race_state.lap_number)
        if projected_stint_length<profile.min_stint:
            return ConstraintResult(
                is_valid=False,
                reason=(
                    f"Current"
                    f"{driver_state.current_compound}"
                    f"Stint only reaches"
                    f"{projected_stint_length}laps"
                    f"(minimum: {profile.min_stint})"
                ),
            )
        return ConstraintResult(is_valid=True)
    