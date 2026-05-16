export type MomentType = "goal" | "red_card";

export interface ImportantMoment {
  type: MomentType;
  videoId: string;
  videoTimestamp: number; // seconds into the video
  importanceScore: number; // how important is this moment 0 -1
}

export type ImportantMomentsResponse = ImportantMoment[];
