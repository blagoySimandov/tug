import type { ImportantMomentsResponse } from "./types";

// Edit this freely. Empty array = no moments for that video.
export const MOCK_MOMENTS: Record<string, ImportantMomentsResponse> = {
  cr_bra: [
    { type: "goal",     videoId: "cr_bra", videoTimestamp: 15, importanceScore: 0.85, priorityDuration: 8 },
    { type: "red_card", videoId: "cr_bra", videoTimestamp: 45, importanceScore: 0.70, priorityDuration: 6 },
    { type: "goal",     videoId: "cr_bra", videoTimestamp: 90, importanceScore: 0.92, priorityDuration: 10 },
  ],
  arg_fr: [
    { type: "goal",     videoId: "arg_fr", videoTimestamp: 10, importanceScore: 0.90, priorityDuration: 8 },
    { type: "red_card", videoId: "arg_fr", videoTimestamp: 30, importanceScore: 0.75, priorityDuration: 6 },
    { type: "goal",     videoId: "arg_fr", videoTimestamp: 60, importanceScore: 0.95, priorityDuration: 10 },
  ],
  "video-1": [
    { type: "goal",     videoId: "video-1", videoTimestamp: 312,  importanceScore: 0.90, priorityDuration: 8 },
    { type: "red_card", videoId: "video-1", videoTimestamp: 2748, importanceScore: 0.75, priorityDuration: 6 },
    { type: "goal",     videoId: "video-1", videoTimestamp: 3510, importanceScore: 0.95, priorityDuration: 10 },
  ],
  "video-2": [
    { type: "goal", videoId: "video-2", videoTimestamp: 900, importanceScore: 0.80, priorityDuration: 8 },
  ],
};

export function getMockMoments(
  videoId: string,
  timestampStart: number,
  timestampEnd: number,
): ImportantMomentsResponse {
  const moments = MOCK_MOMENTS[videoId] ?? [];
  return moments.filter(
    (m) => m.videoTimestamp >= timestampStart && m.videoTimestamp <= timestampEnd,
  );
}
