from pathlib import Path

import pandas as pd

from ml.elo.elo_calculator import EloCalculator


def main():

    results_path = Path(
        "data/ml/features/race_results.parquet"
    )

    results_df = pd.read_parquet(
        results_path
    )

    print()
    print("=" * 80)
    print("RESULT DATASET")
    print("=" * 80)
    print()

    print(results_df.columns.tolist())

    calculator = EloCalculator()

    driver_elos = (
        calculator.build_driver_elos(
            results_df
        )
    )

    team_elos = (
        calculator.build_team_elos(
            results_df
        )
    )

    driver_output = Path(
        "data/ml/features/driver_elo.parquet"
    )

    team_output = Path(
        "data/ml/features/team_elo.parquet"
    )

    driver_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    driver_elos.to_parquet(
        driver_output,
        index=False,
    )

    team_elos.to_parquet(
        team_output,
        index=False,
    )

    print()
    print("=" * 80)
    print("DRIVER ELO")
    print("=" * 80)
    print()

    print(driver_elos.head())

    print()

    print("=" * 80)
    print("TEAM ELO")
    print("=" * 80)
    print()

    print(team_elos.head())

    print()

    print(
        f"Saved {driver_output}"
    )

    print(
        f"Saved {team_output}"
    )


if __name__ == "__main__":
    main()