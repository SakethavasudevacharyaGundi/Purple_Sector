import pandas as pd


class TyreTargetBuilder:

    FUEL_BURN_PER_LAP = 1.8
    FUEL_TIME_PER_KG = 0.035

    def build(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        working_df = df.copy()

        working_df = working_df.dropna(
            subset=[
                "current_lap_time",
                "current_compound",
                "current_tyre_age",
                "stint",
            ]
        )

        # Green flag only
        working_df = working_df[
            working_df["track_condition"]
            == "ALL_CLEAR"
        ]

        # Dry compounds only
        working_df = working_df[
            working_df["current_compound"].isin(
                [
                    "SOFT",
                    "MEDIUM",
                    "HARD",
                ]
            )
        ]

        # Ignore warmup laps
        working_df = working_df[
            working_df["current_tyre_age"] >= 4
        ]

        # Remove very long stints
        working_df = working_df[
            working_df["current_tyre_age"] <= 40
        ]

        # Remove pit-in laps
        working_df = working_df[
            working_df[
                "pit_in_time_seconds"
            ].isna()
        ]

        # Remove pit-out laps
        working_df = working_df[
            working_df[
                "pit_out_time_seconds"
            ].isna()
        ]

        stint_keys = [
            "season",
            "event_name",
            "driver_number",
            "stint",
        ]

        baseline_rows = []

        for _, stint_df in (
            working_df.groupby(stint_keys)
        ):

            stint_df = (
                stint_df
                .sort_values(
                    "current_tyre_age"
                )
                .copy()
            )

            stint_df[
                "lap_in_stint"
            ] = (
                stint_df[
                    "current_tyre_age"
                ]
                - 4
            )
            stint_df["race_progress"] = (
                stint_df["lap_number"]
                /
                stint_df["total_laps"]
            )

            stint_df["tyre_life_ratio"] = (
                stint_df["current_tyre_age"]
                /
                (
                    stint_df["current_tyre_age"]
                    +
                    stint_df["laps_remaining"]
                )
            )

            # Fuel correction
            stint_df[
                "fuel_correction"
            ] = (
                stint_df[
                    "lap_in_stint"
                ]
                * self.FUEL_BURN_PER_LAP
                * self.FUEL_TIME_PER_KG
            )

            stint_df[
                "fuel_corrected_lap_time"
            ] = (
                stint_df[
                    "current_lap_time"
                ]
                + stint_df[
                    "fuel_correction"
                ]
            )

            # IMPORTANT:
            # create baseline window AFTER fuel_corrected_lap_time exists
            baseline_window = stint_df[
                (
                    stint_df[
                        "current_tyre_age"
                    ] >= 4
                )
                &
                (
                    stint_df[
                        "current_tyre_age"
                    ] <= 8
                )
            ]

            if len(
                baseline_window
            ) < 3:
                continue

            baseline = (
                baseline_window[
                    "fuel_corrected_lap_time"
                ]
                .quantile(0.20)
            )

            stint_df[
                "baseline_pace"
            ] = baseline

            stint_df[
                "degradation_seconds"
            ] = (
                stint_df[
                    "fuel_corrected_lap_time"
                ]
                - baseline
            )

            # Keep realistic degradation values
            stint_df = stint_df[
                stint_df[
                    "degradation_seconds"
                ].between(
                    -0.5,
                    2.5,
                )
            ]
    
            if len(
                stint_df
            ) < 5:
                continue

            baseline_rows.append(
                stint_df
            )

        if not baseline_rows:
            return pd.DataFrame()

        result = pd.concat(
            baseline_rows,
            ignore_index=True,
        )
        result["rainfall"] = (
            result["rainfall"]
            .fillna(0)
        )

        result["race_progress"] = (
            result["race_progress"]
            .fillna(0)
        )

        result["tyre_life_ratio"] = (
            result["tyre_life_ratio"]
            .fillna(0)
        )

        print()
        print("SHAPE")
        print(result.shape)

        print()
        print("TARGET")
        print(
            result[
                "degradation_seconds"
            ].describe()
        )
        print()
        print("TARGET QUANTILES")

        print(
            result[
                "degradation_seconds"
            ]
            .quantile(
                [
                    0.90,
                    0.95,
                    0.97,
                    0.98,
                    0.99,
                ]
            )
        )
        print()
        print("CORRELATION")
        print(
            result[
                "current_tyre_age"
            ].corr(
                result[
                    "degradation_seconds"
                ]
            )
        )

        print()
        print("MEAN BY TYRE AGE")
        print(
            result.groupby(
                "current_tyre_age"
            )[
                "degradation_seconds"
            ]
            .mean()
            .head(40)
        )

        print()
        print("COMPOUND CORRELATIONS")

        for compound in [
            "SOFT",
            "MEDIUM",
            "HARD",
        ]:

            compound_df = result[
                result[
                    "current_compound"
                ]
                == compound
            ]

            if len(compound_df) == 0:
                continue

            corr = (
                compound_df[
                    "current_tyre_age"
                ]
                .corr(
                    compound_df[
                        "degradation_seconds"
                    ]
                )
            )

            print(
                f"{compound}: {corr:.4f}"
            )

        return result