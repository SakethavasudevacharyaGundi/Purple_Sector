from recommendation.constraints.base_constraint import (
    BaseConstraint
)

from recommendation.constraints.constraint_result import (
    ConstraintResult
)

from recommendation.constraints.segment_builder import (
    SegmentBuilder
)

from recommendation.tyre_profiles import (
    TYRE_PROFILES
)


class TyreStintConstraint(
    BaseConstraint
):

    def __init__(self):

        self.segment_builder = (
            SegmentBuilder()
        )

    def validate(
        self,
        race_state,
        driver_state,
        candidate,
    ) -> ConstraintResult:

        segments = (

            self.segment_builder.build(
                race_state,
                driver_state,
                candidate,
            )

        )

        for segment in segments:

            profile = (
                TYRE_PROFILES[
                    segment.compound
                ]
            )

            if (
                segment.length
                > profile.max_stint
            ):

                return ConstraintResult(
                    False,
                    (
                        f"{segment.compound} "
                        f"stint of "
                        f"{segment.length} laps "
                        f"exceeds max "
                        f"{profile.max_stint}"
                    )
                )

        return ConstraintResult(
            True
        )