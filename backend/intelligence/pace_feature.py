from intelligence.base_feature import BaseFeature
class PaceFeatures(BaseFeature):
    def extract(self,race_state, driver_state) -> dict:
        return {
            "last_lap_time": driver_state.last_lap_time,
        }