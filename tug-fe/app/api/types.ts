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
