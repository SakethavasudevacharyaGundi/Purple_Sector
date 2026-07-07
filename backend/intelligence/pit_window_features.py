from intelligence.base_feature import BaseFeature
class PitWindowFeatures(BaseFeature):
    DEFAULT_PIT_LOSS=22.0
    def extract(self,race_state, driver_state) -> dict:
        gap_ahead = (driver_state.gap_ahead or 0)
        gap_behind = (driver_state.gap_behind or 0)
        return{
            "pit_loss_estimate": self.DEFAULT_PIT_LOSS,
            "pit_window_open_ahead": gap_ahead > self.DEFAULT_PIT_LOSS,
            "pit_window_open_behind": gap_behind > self.DEFAULT_PIT_LOSS
        }