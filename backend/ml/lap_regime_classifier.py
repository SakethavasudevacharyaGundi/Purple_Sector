# ml/lap_regime_classifier.py

from domain.lap_regime import LapRegime
from domain.track_condition import TrackCondition


class LapRegimeClassifier:

    def classify(
        self,
        race_state,
        driver_state,
    ) -> LapRegime:

        if driver_state.pit_in_this_lap:
            return LapRegime.PIT_IN

        if driver_state.pit_out_this_lap:
            return LapRegime.PIT_OUT

        if (
            race_state.track_condition
            == TrackCondition.SAFETY_CAR
        ):
            return LapRegime.SAFETY_CAR

        if (
            race_state.track_condition
            == TrackCondition.RED_FLAG
        ):
            return LapRegime.RED_FLAG

        return LapRegime.GREEN