from pathlib import Path
import pandas as pd
from ml.datasets.season_dataset_builder import SeasonDatasetBuilder
class ProductionDatasetBuilder:
    def __init__(self):
        self.builder=SeasonDatasetBuilder()
        self.output_path=Path("data/ml/v1/seasons")
        self.output_path.mkdir(parents=True, exist_ok=True)
    def build(self,start_year:int, end_year:int):
        season_files=[]
        for season in range(start_year, end_year+1):
            df=self.builder.build(season)
            season_file=self.output_path/f"season_{season}.parquet"
            df.to_parquet(season_file, index=False)
            season_files.append(season_file)
        master_df=pd.concat([pd.read_parquet(file) for file in season_files], ignore_index=True)
        Path("data/ml/v1").mkdir(parents=True, exist_ok=True)
        master_df.to_parquet("data/ml/v1/master_dataset.parquet", index=False)
        return master_df