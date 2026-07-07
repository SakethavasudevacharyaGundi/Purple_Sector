from ml.training.training_regime import TrainingRegime

class DatasetFilter:
    def filter(
        self,
        dataset,
        regime: TrainingRegime,
    ):
        if(regime ==TrainingRegime.GREEN_ONLY):
            return dataset[
                dataset['track_condition'] == 'ALL_CLEAR'
            ]