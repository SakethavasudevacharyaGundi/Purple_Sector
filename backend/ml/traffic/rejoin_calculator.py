from dataclasses import dataclass


@dataclass
class RejoinResult:
    rejoin_position: int
    gap_ahead: float | None
    gap_behind: float | None


class RejoinCalculator:

    def calculate(
        self,
        race_state,
        driver_number: str,
        pit_loss_seconds: float,
    ) -> RejoinResult:

        target_driver = None

        for driver in race_state.drivers:

            if driver.driver_number == driver_number:
                target_driver = driver
                break

        if target_driver is None:
            raise ValueError(
                f"Driver {driver_number} not found"
            )

        current_gap = (
            target_driver.gap_to_leader or 0.0
        )

        projected_gap = (
            current_gap + pit_loss_seconds
        )

        projected = []

        for driver in race_state.drivers:

            gap = (
                driver.gap_to_leader or 0.0
            )

            if (
                driver.driver_number
                == driver_number
            ):
                gap = projected_gap

            projected.append(
                (
                    driver.driver_number,
                    gap,
                )
            )

        projected.sort(
            key=lambda x: x[1]
        )

        new_position = None

        for idx, (drv, _) in enumerate(
            projected,
            start=1,
        ):
            if drv == driver_number:
                new_position = idx
                break

        ahead_gap = None
        behind_gap = None

        if (
            new_position is not None
            and new_position > 1
        ):
            ahead_gap = (
                projected[new_position - 1][1]
                - projected[new_position - 2][1]
            )

        if (
            new_position is not None
            and new_position < len(projected)
        ):
            behind_gap = (
                projected[new_position][1]
                - projected[new_position - 1][1]
            )

        return RejoinResult(
            rejoin_position=new_position,
            gap_ahead=ahead_gap,
            gap_behind=behind_gap,
        )