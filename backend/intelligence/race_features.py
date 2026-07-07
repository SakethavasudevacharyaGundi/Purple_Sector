from intelligence.base_feature import BaseFeature
class RaceFeatures(BaseFeature):
    def extract(self, race_state, driver_state) -> dict:
        return {
            "lap_number":race_state.lap_number,
            "total_laps":race_state.total_laps,
            "laps_remaining":(race_state.total_laps-race_state.lap_number),
            "track_condition":race_state.track_condition.value,
            "air_temp":race_state.air_temp,
            "track_temp":race_state.track_temp,
            "rainfall":race_state.rainfall,
        }
    