export type DriverStatus = "UNKNOWN" | "ACTIVE";

export type TrackCondition = "UNKNOWN" | "ALL_CLEAR" | "YELLOW" | "SAFETY_CAR" | "RED_FLAG";

export interface DriverState {
  driver_number: string;
  driver_name: string;
  team: string;
  status: DriverStatus;
  position: number | null;
  current_compound: string | null;
  current_tyre_age: number | null;
  stint: number | null;
  gap_ahead: number | null;
  gap_behind: number | null;
  gap_to_leader: number;
  last_lap_time: number | null;
  pit_in_this_lap: boolean;
  pit_out_this_lap: boolean;
  is_retired: boolean;
  pit_in_time_seconds: number | null;
  pit_out_time_seconds: number | null;
}

export interface RaceState {
  race_id: string;
  season?: number;
  event_name: string;
  lap_number: number;
  total_laps: number;
  track_condition: TrackCondition;
  air_temp: number | null;
  track_temp: number | null;
  rainfall: boolean;
  drivers: DriverState[];
}

export interface Strategy {
  pit_lap: number;
  next_compound: string;
}

export interface SetupRequest {
  season: number;
  gp: string;
  lap: number;
  driver: string;
}
