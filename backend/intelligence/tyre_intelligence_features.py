from intelligence.base_feature import BaseFeature
from recommendation.tyre_profiles import TYRE_PROFILES
class TyreIntelligenceFeatures(BaseFeature):
    def extract(self,race_state, driver_state) -> dict:
        if(driver_state.current_compound is None or driver_state.current_tyre_age is None):
            return {}
        profile=TYRE_PROFILES.get(driver_state.current_compound)
        age=driver_state.current_tyre_age
        remaining_life=max(0, profile.max_stint- age)
        completion_ratio=age/profile.max_stint
        return{
            "remaining_tyre_life":remaining_life,
            "tyre_completion_ratio":completion_ratio,
            "tyre_life_used_pct":age/profile.max_stint*100,
        }