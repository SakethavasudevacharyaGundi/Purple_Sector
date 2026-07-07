from intelligence.feature_registry import (
    FeatureRegistry,
)

from intelligence.race_features import (
    RaceFeatures,
)

from intelligence.tyre_features import (
    TyreFeatures,
)

from intelligence.traffic_features import (
    TrafficFeatures,
)

from intelligence.pace_feature import (
    PaceFeatures,
)

from intelligence.tyre_intelligence_features import (
    TyreIntelligenceFeatures,
)

from intelligence.pit_window_features import (
    PitWindowFeatures,
)

from intelligence.traffic_risk_features import (
    TrafficRiskFeatures,
)

from intelligence.undercut_features import (
    UndercutFeatures,
)

from intelligence.pace_trend_feature import (
    PaceTrendFeatures,
)


class FeatureEngine:

    def __init__(self):

        self.registry = FeatureRegistry()

        self.registry.register(
            RaceFeatures()
        )

        self.registry.register(
            TyreFeatures()
        )

        self.registry.register(
            TrafficFeatures()
        )

        self.registry.register(
            PaceFeatures()
        )

        self.registry.register(
            TyreIntelligenceFeatures()
        )

        self.registry.register(
            PitWindowFeatures()
        )

        self.registry.register(
            TrafficRiskFeatures()
        )

        self.registry.register(
            UndercutFeatures()
        )

        self.registry.register(
            PaceTrendFeatures()
        )

    def extract(
        self,
        race_state,
        driver_state,
    ):

        features = {}

        for extractor in (
            self.registry.get_all()
        ):

            features.update(

                extractor.extract(
                    race_state,
                    driver_state,
                )
            )

        return features