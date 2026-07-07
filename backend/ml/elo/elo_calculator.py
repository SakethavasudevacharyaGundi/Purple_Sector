from collections import defaultdict

import pandas as pd

from ml.elo.driver_lookup import (
    get_driver_info,
)


class EloCalculator:

    BASE_RATING = 1500.0

    K_FACTOR = 20

    def expected_score(

        self,

        rating_a: float,

        rating_b: float,

    ) -> float:

        return 1 / (

            1 +

            10 ** (

                (rating_b - rating_a)

                / 400

            )

        )

    def update_ratings(
        self,
        ratings: dict,
        ordered_entities: list[str],
    ) -> None:
        n = len(ordered_entities)
        if n <= 1:
            return
            
        # Divide the K_FACTOR by the number of opponents to prevent inflation in multiplayer mode
        effective_k = self.K_FACTOR / (n - 1)

        for i in range(n):
            entity_a = ordered_entities[i]
            for j in range(i + 1, n):
                entity_b = ordered_entities[j]
                
                rating_a = ratings[entity_a]
                rating_b = ratings[entity_b]
                
                expected_a = self.expected_score(rating_a, rating_b)
                expected_b = self.expected_score(rating_b, rating_a)
                
                ratings[entity_a] += effective_k * (1 - expected_a)
                ratings[entity_b] += effective_k * (0 - expected_b)

    def build_driver_elos(

        self,

        results_df: pd.DataFrame,

    ) -> pd.DataFrame:

        ratings = defaultdict(

            lambda:
            self.BASE_RATING

        )

        elo_rows = []

        grouped = results_df.groupby(

            [

                "season",

                "round_number",

                "event_name",

            ],

            sort=True,

        )

        for (

            season,

            round_number,

            event_name,

        ), race_df in grouped:

            race_df = (

                race_df
                .sort_values(
                    "Position"
                )

            )

            ordered_drivers = []

            driver_infos = []

            for driver_number in (

                race_df[
                    "DriverNumber"
                ]
                .astype(str)
            ):

                driver_info = (

                    get_driver_info(

                        season,

                        driver_number,

                    )

                )

                ordered_drivers.append(

                    driver_info
                    .canonical_driver_number

                )

                driver_infos.append(

                    driver_info

                )

            for driver_info in driver_infos:

                elo_rows.append(

                    {

                        "season":
                        season,

                        "round_number":
                        round_number,

                        "event_name":
                        event_name,

                        "driver_name":
                        driver_info.driver_name,

                        "display_number":
                        driver_info.display_number,

                        "canonical_driver_number":
                        driver_info.canonical_driver_number,

                        "driver_elo":
                        round(

                            ratings[
                                driver_info
                                .canonical_driver_number
                            ],

                            2,

                        ),

                    }

                )

            self.update_ratings(

                ratings,

                ordered_drivers,

            )

        return pd.DataFrame(

            elo_rows

        )

    def build_team_elos(

        self,

        results_df: pd.DataFrame,

    ) -> pd.DataFrame:

        ratings = defaultdict(

            lambda:
            self.BASE_RATING

        )

        elo_rows = []

        grouped = results_df.groupby(

            [

                "season",

                "round_number",

                "event_name",

            ],

            sort=True,

        )

        for (

            season,

            round_number,

            event_name,

        ), race_df in grouped:

            team_results = (

                race_df
                .groupby(
                    "Team"
                )

                [
                    "Position"
                ]

                .mean()

                .sort_values()

            )

            ordered_teams = list(

                team_results.index

            )

            for team in ordered_teams:

                elo_rows.append(

                    {

                        "season":
                        season,

                        "event_name":
                        event_name,

                        "team":
                        team,

                        "team_elo":
                        round(

                            ratings[
                                team
                            ],

                            2,

                        ),

                    }

                )

            self.update_ratings(

                ratings,

                ordered_teams,

            )

        return pd.DataFrame(

            elo_rows

        )