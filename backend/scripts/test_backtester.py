import pandas as pd

from ml.backtesting.backtest_runner import (
    BacktestRunner,
)


TEST_RACES = [

    (2024, "Bahrain Grand Prix", 20),

    (2024, "Saudi Arabian Grand Prix", 20),

    (2024, "Australian Grand Prix", 20),

    (2024, "Japanese Grand Prix", 20),

    (2024, "Chinese Grand Prix", 20),

]


runner = BacktestRunner()

all_results = []

print()
print("=" * 100)
print("MULTI RACE BACKTEST")
print("=" * 100)

for season, event_name, lap in TEST_RACES:

    print()
    print(
        f"Running {season} "
        f"{event_name} "
        f"(Lap {lap})"
    )

    try:

        results_df, metrics = (

            runner.run_race(

                season=season,

                event_name=event_name,

                state_lap=lap,

                monte_carlo_runs=500,

            )

        )

        print(
            f"MAE={metrics['mae']:.2f} "
            f"RMSE={metrics['rmse']:.2f}"
        )

        all_results.append(
            results_df
        )

    except Exception as exc:

        print(
            f"FAILED: "
            f"{event_name}"
        )

        print(exc)

if not all_results:

    raise RuntimeError(
        "No races completed"
    )

combined_df = pd.concat(

    all_results,

    ignore_index=True,

)

overall_mae = float(
    combined_df["error"].mean()
)

overall_rmse = float(
    (
        combined_df["error"] ** 2
    ).mean() ** 0.5
)

overall_median = float(
    combined_df["error"].median()
)

overall_p90 = float(
    combined_df["error"]
    .quantile(0.90)
)

print()
print("=" * 100)
print("OVERALL RESULTS")
print("=" * 100)

print()

print(
    f"Drivers Tested : "
    f"{len(combined_df)}"
)

print(
    f"Overall MAE    : "
    f"{overall_mae:.3f}"
)

print(
    f"Overall RMSE   : "
    f"{overall_rmse:.3f}"
)

print(
    f"Median Error   : "
    f"{overall_median:.3f}"
)

print(
    f"P90 Error      : "
    f"{overall_p90:.3f}"
)

print()

print("=" * 100)
print("WORST 20 PREDICTIONS")
print("=" * 100)

print()

print(

    combined_df

    .sort_values(
        "error",
        ascending=False,
    )

    .head(20)

    [[
        "season",
        "event_name",
        "driver_number",
        "predicted_finish",
        "actual_finish",
        "error",
    ]]

)