// Run `bun run gen:types` (with backend running) to regenerate from the OpenAPI spec.
// Source of truth: tug-be/models.py
import type { components } from "./generated";

export type { components };
export type ImportantMoment = components["schemas"]["ImportantMoment"];
export type MomentType = ImportantMoment["type"];
export type ImportantMomentsResponse = ImportantMoment[];

export type Match = {
  id: string;
  homeTeam: { name: string; flag: string };
  awayTeam: { name: string; flag: string };
  url: string;
};
export type MatchesResponse = Match[];

export type EventsFilter = {
  year?: number;
  league_id?: number;
  team_name?: string;
  team_id?: number;
  status?: string;
  offset?: number;
};

export type BsdEvent = {
  id: number;
  league_id: number;
  league_name: string;
  home_team: string;
  away_team: string;
  event_date: string;
  status: string;
  home_score: number;
  away_score: number;
};

export type EventsResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: BsdEvent[];
};
