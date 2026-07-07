from recommendation.constraints.base_constraint import BaseConstraint
from recommendation.constraints.tyre_stint_constraint import TyreStintConstraint
from recommendation.constraints.race_end_constraint import RaceEndConstraint
from recommendation.constraints.constraint_result import ConstraintResult
from recommendation.constraints.current_tyre_constraint import CurrentTyreConstraint

class ConstraintEngine:

    def __init__(self):

        self.constraints = [

            CurrentTyreConstraint(),
            
            RaceEndConstraint(),

            TyreStintConstraint(),

        ]

    def validate(
        self,
        race_state,
        driver_state,
        candidate,
    ):

        for constraint in self.constraints:

            result = constraint.validate(
                race_state,
                driver_state,
                candidate,
            )

            if not result.is_valid:

                return result

        return ConstraintResult(
            True
        )