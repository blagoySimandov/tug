export type MomentType = "goal" | "red_card";

export interface ImportantMoment {
  type: MomentType;
  videoId: string;
  videoTimestamp: number; // seconds into the video
  matchTimestamp: number; // match minute
  description?: string;
}

export type ImportantMomentsResponse = ImportantMoment[];
