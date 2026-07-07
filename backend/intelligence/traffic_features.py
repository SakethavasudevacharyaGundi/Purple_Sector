from intelligence.base_feature import BaseFeature
class TrafficFeatures(BaseFeature):
    def extract(self,race_state, driver_state) -> dict:
        return {
            "position":driver_state.position,
            "gap_ahead":driver_state.gap_ahead,
            "gap_behind":driver_state.gap_behind,
            "gap_to_leader":driver_state.gap_to_leader,
        }