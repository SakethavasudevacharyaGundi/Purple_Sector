from ml.datasets.training_row import TrainingRow


class FeatureExtractor:

    def extract(
            self,
            race_state,
            driver_state,
            season:int,
            future_lap_time:float|None=None,
            lap_time_delta:float|None=None,
    )->TrainingRow:
        return TrainingRow(
            season=season,
            event_name=race_state.event_name,
            circuit_name=race_state.event_name,
            driver_number=driver_state.driver_number,
            lap_number=race_state.lap_number,
            total_laps=race_state.total_laps,
            position=driver_state.position,
            current_compound=driver_state.current_compound,
            current_tyre_age=driver_state.current_tyre_age,
            stint=driver_state.stint,
            gap_ahead=driver_state.gap_ahead,
            gap_behind=driver_state.gap_behind,
            gap_to_leader=driver_state.gap_to_leader,
            air_temp=race_state.air_temp,
            track_temp=race_state.track_temp,
            rainfall=race_state.rainfall,
            track_condition=race_state.track_condition.value,
            laps_remaining=(
                race_state.total_laps
                - race_state.lap_number
            ),
            future_lap_time=future_lap_time,
            current_lap_time=driver_state.last_lap_time,
            lap_time_delta=lap_time_delta, 
                pit_in_time_seconds=
            driver_state.pit_in_time_seconds,

            pit_out_time_seconds=
            driver_state.pit_out_time_seconds,
        )