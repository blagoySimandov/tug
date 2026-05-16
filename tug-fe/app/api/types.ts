export type MomentType = "goal" | "red_card";

export interface Team {
  name: string;
  flag: string;
}

export interface Match {
  id: string;
  homeTeam: Team;
  awayTeam: Team;
  url: string;
}

export type MatchesResponse = Match[];

export interface ImportantMoment {
  type: MomentType;
  videoId: string;
  videoTimestamp: number; // seconds into the video
  importanceScore: number; // how important is this moment 0 -1
  priorityDuration: number; // seconds this moment holds priority
}

export type ImportantMomentsResponse = ImportantMoment[];
