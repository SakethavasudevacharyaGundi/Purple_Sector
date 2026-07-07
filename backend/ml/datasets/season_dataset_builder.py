import pandas as pd

from ingestion.fastf1_client import (
    FastF1Client,
)

from replay.replay_generator import (
    ReplayGenerator,
)

from ml.datasets.dataset_builder import (
    DatasetBuilder,
)


class SeasonDatasetBuilder:

    def __init__(self):

        self.client = FastF1Client()

        self.replay_generator = (
            ReplayGenerator()
        )

        self.dataset_builder = (
            DatasetBuilder()
        )

    def build(
        self,
        season: int,
    ) -> pd.DataFrame:

        race_datasets = []

        schedule = (
            self.client.get_schedule(
                season
            )
        )

        races = schedule[
            schedule["EventFormat"]
            == "conventional"
        ]

        for _, race in races.iterrows():

            event_name = race[
                "EventName"
            ]

            print(
                f"\n[{season}] "
                f"{event_name}"
            )

            try:

                session = (
                    self.client.get_session(
                        season=season,
                        grand_prix=event_name,
                        session_type="R",
                    )
                )

                replay = (
                    self.replay_generator.generate(
                        session
                    )
                )

                df = (
                    self.dataset_builder
                    .build_from_replay(
                        replay
                    )
                )

                race_datasets.append(
                    df
                )

            except Exception as e:

                print(
                    f"FAILED: "
                    f"{event_name}"
                )

                print(e)

        if not race_datasets:

            return pd.DataFrame()

        return pd.concat(
            race_datasets,
            ignore_index=True,
        )