import type { ImportantMomentsResponse } from "./types";

// Edit this freely. Empty array = no moments for that video.
export const MOCK_MOMENTS: Record<string, ImportantMomentsResponse> = {
  "video-1": [
    { type: "goal", videoId: "video-1", videoTimestamp: 312, importanceScore: 0.9 },
    { type: "red_card", videoId: "video-1", videoTimestamp: 2748, importanceScore: 0.75 },
    { type: "goal", videoId: "video-1", videoTimestamp: 3510, importanceScore: 0.95 },
  ],
  "video-2": [
    { type: "goal", videoId: "video-2", videoTimestamp: 900, importanceScore: 0.8 },
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
