from pathlib import Path
import json

from replay.replay_model import RaceReplay


class ReplayRepository:

    def __init__(self):

        self.base_path = Path(
            "data/processed/replays"
        )

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        replay: RaceReplay,
    ):

        filename = (
            f"{replay.season}_"
            f"{replay.event_name}"
            .lower()
            .replace(" ", "_")
            + ".json"
        )

        path = self.base_path / filename

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as f:

            f.write(
                replay.model_dump_json(
                    indent=2
                )
            )

    def load(
        self,
        season: int,
        event_name: str,
    ):

        filename = (
            f"{season}_"
            f"{event_name}"
            .lower()
            .replace(" ", "_")
            + ".json"
        )

        path = self.base_path / filename

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        return RaceReplay.model_validate(
            data
        )