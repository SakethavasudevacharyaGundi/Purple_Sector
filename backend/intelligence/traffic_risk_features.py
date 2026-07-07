from intelligence.base_feature import BaseFeature
class TrafficRiskFeatures(BaseFeature):
    def extract(self,race_state, driver_state) -> dict:
        return{}