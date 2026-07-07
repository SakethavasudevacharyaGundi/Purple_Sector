from intelligence.base_feature import BaseFeature
class TyreFeatures(BaseFeature):
    def extract(self,race_state, driver_state) -> dict:
        return {
            "compound":driver_state.current_compound,
            "tyre_age":driver_state.current_tyre_age,
            "stint":driver_state.stint,
        }