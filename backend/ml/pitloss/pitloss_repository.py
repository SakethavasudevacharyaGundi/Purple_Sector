# ml/pitloss/pitloss_repository.py

from pathlib import Path
import pandas as pd


class PitLossRepository:

    def __init__(self):

        self.path = Path(
            "data/ml/v1/pitloss.parquet"
        )

    def save(
        self,
        df: pd.DataFrame,
    ):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_parquet(
            self.path,
            index=False,
        )

    def load(self):

        return pd.read_parquet(
            self.path
        )