# scripts/test_lap_regime_classifier.py

from ingestion.fastf1_client import FastF1Client

from replay.replay_generator import ReplayGenerator

from backend.ml.datasets.dataset_builder import DatasetBuilder


def main():

    client = FastF1Client()

    session = client.get_session(
        season=2024,
        grand_prix="Monaco Grand Prix",
        session_type="R",
    )

    replay = ReplayGenerator().generate(
        session
    )

    df = DatasetBuilder().build_from_replay(
        replay
    )

    print("\n" + "=" * 80)
    print("LAP REGIME COUNTS")
    print("=" * 80)

    print(
        df["lap_regime"]
        .value_counts(dropna=False)
    )

    print("\n" + "=" * 80)
    print("LAP 1 SAMPLE")
    print("=" * 80)

    print(
        df[
            df["lap_number"] == 1
        ][
            [
                "driver_number",
                "lap_number",
                "lap_regime",
                "current_lap_time",
                "track_condition",
            ]
        ]
        .head(20)
    )

    print("\n" + "=" * 80)
    print("PIT EVENT SAMPLE")
    print("=" * 80)

    pit_rows = df[
        df["lap_regime"].isin(
            [
                "PIT_IN",
                "PIT_OUT",
            ]
        )
    ]

    print(
        pit_rows[
            [
                "driver_number",
                "lap_number",
                "lap_regime",
                "current_lap_time",
            ]
        ]
        .head(20)
    )

    print("\n" + "=" * 80)
    print("RED FLAG / SAFETY CAR SAMPLE")
    print("=" * 80)

    special_rows = df[
        df["lap_regime"].isin(
            [
                "RED_FLAG",
                "SAFETY_CAR",
            ]
        )
    ]

    print(
        special_rows[
            [
                "driver_number",
                "lap_number",
                "lap_regime",
                "current_lap_time",
            ]
        ]
        .head(20)
    )


if __name__ == "__main__":
    main()