import type { SetupRequest, RaceState, DriverState, Strategy } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const fetchSetup = async (request: SetupRequest): Promise<RaceState> => {
  const response = await fetch(`${API_BASE_URL}/setup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch setup data');
  }

  const data = await response.json();
  if (data.error) {
    throw new Error(data.error);
  }
  return data as RaceState;
};

export const runSimulation = async (
  raceState: RaceState,
  driver: DriverState,
  strategy: Strategy
) => {
  const response = await fetch(`${API_BASE_URL}/simulate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      race_state: raceState,
      driver,
      strategy,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to run simulation');
  }

  return response.json();
};

export const runMonteCarlo = async (
  raceState: RaceState,
  driver: DriverState,
  strategy: Strategy,
  runs: number = 1000
) => {
  const response = await fetch(`${API_BASE_URL}/monte-carlo`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      race_state: raceState,
      driver,
      strategy,
      runs,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to run Monte Carlo simulation');
  }

  return response.json();
};

export async function fetchElo() {
  const response = await fetch(`${API_BASE_URL}/elo`);
  if (!response.ok) {
    throw new Error('Failed to fetch ELO rankings');
  }
  return response.json();
}

export async function fetchSeasons() {
  const response = await fetch(`${API_BASE_URL}/metadata/seasons`);
  if (!response.ok) {
    throw new Error('Failed to fetch seasons');
  }
  return response.json();
}

export async function fetchSeasonMetadata(season: number | string) {
  const response = await fetch(`${API_BASE_URL}/metadata/${season}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch metadata for season ${season}`);
  }
  return response.json();
}

export const fetchRecommendations = async (raceState: RaceState, driver: DriverState) => {
  const response = await fetch(`${API_BASE_URL}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ race_state: raceState, driver })
  });
  if (!response.ok) {
    throw new Error('Failed to fetch recommendations');
  }
  const data = await response.json();
  if (data.error) throw new Error(data.error);
  return data;
};

export const fetchCustomSimulation = async (raceState: any, driver: any, pitLap: number, nextCompound: string) => {
  const response = await fetch(`${API_BASE_URL}/simulate/custom`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ race_state: raceState, driver, pit_lap: pitLap, next_compound: nextCompound })
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to run custom simulation');
  }
  return response.json();
};
