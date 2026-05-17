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
  homeScore: number | null;
  awayScore: number | null;
  leagueName: string;
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
  home_score: number | null;
  away_score: number | null;
  video_filename: string | null;
  kickoff_offset: number | null;
};

export const NARRATOR_VOICES = [
  "Puck", "Achernar", "Alnilam", "Autonoe", "Enceladus", "Rasalgethi",
  "Sadachbia", "Schedar", "Umbriel", "Zubenelgenubi",
  "Achird", "Algenib", "Callirrhoe", "Despina", "Pulcherrima",
  "Sulafat", "Vindemiatrix", "Zephyr",
] as const;

export type NarratorVoice = typeof NARRATOR_VOICES[number];

export const NARRATOR_VIBES = [
  { label: "Electrifying", value: "electrifying" },
  { label: "Analytical", value: "calm and analytical" },
  { label: "Comedic", value: "comedic and lighthearted" },
  { label: "Poetic", value: "poetic and lyrical" },
  { label: "Pundit", value: "opinionated pundit who isn't afraid to make bold calls" },
] as const;

export type NarratorVibe = typeof NARRATOR_VIBES[number]["value"];

export type NarratorStyle = {
  voice: NarratorVoice;
  persona: NarratorVibe;
  custom_instruction: string;
  temperature?: number;
  target_duration_seconds?: number;
};

export type EventsResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: BsdEvent[];
};

export type NarratorStyle = {
  temperature?: number;
  persona?: string;
  target_duration_seconds?: number;
  voice?: string;
};
