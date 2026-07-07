import pandas as pd

df = pd.read_parquet(
    "data/ml/features/driver_elo.parquet"
)

latest_race = (

    df[
        [
            "season",
            "event_name",
        ]
    ]

    .drop_duplicates()

    .sort_values(
        [
            "season",
            "event_name",
        ]
    )

    .iloc[-1]
)

season = latest_race["season"]

event_name = latest_race["event_name"]

latest_df = df[

    (df["season"] == season)

    &

    (
        df["event_name"]
        ==
        event_name
    )

].copy()

latest_df = latest_df.sort_values(

    "driver_elo",

    ascending=False,

)

print()
print("=" * 80)
print("TOP 20 DRIVER ELO")
print("=" * 80)
print()

print(

    latest_df[
        [
            "driver_number",
            "driver_elo",
        ]
    ]
    .head(20)

)

print()
print("=" * 80)
print("BOTTOM 20 DRIVER ELO")
print("=" * 80)
print()

print(

    latest_df[
        [
            "driver_number",
            "driver_elo",
        ]
    ]
    .tail(20)

)

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

print(
    f"Drivers: {len(latest_df)}"
)

print(
    f"Max ELO: {latest_df['driver_elo'].max():.2f}"
)

print(
    f"Min ELO: {latest_df['driver_elo'].min():.2f}"
)

print(
    f"Mean ELO: {latest_df['driver_elo'].mean():.2f}"
)

print(
    f"Std ELO: {latest_df['driver_elo'].std():.2f}"
)

print()