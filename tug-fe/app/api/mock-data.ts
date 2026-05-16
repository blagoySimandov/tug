import type { ImportantMomentsResponse } from "./types";

// Edit this freely. Empty array = no moments for that video.
export const MOCK_MOMENTS: Record<string, ImportantMomentsResponse> = {
  "video-1": [
    {
      type: "goal",
      videoId: "video-1",
      videoTimestamp: 312,
      matchTimestamp: 23,
      description: "Header from corner kick",
    },
    {
      type: "red_card",
      videoId: "video-1",
      videoTimestamp: 2748,
      matchTimestamp: 67,
      description: "Dangerous tackle",
    },
    {
      type: "goal",
      videoId: "video-1",
      videoTimestamp: 3510,
      matchTimestamp: 89,
      description: "Penalty kick",
    },
  ],
  "video-2": [
    {
      type: "goal",
      videoId: "video-2",
      videoTimestamp: 900,
      matchTimestamp: 45,
      description: "Long-range shot",
    },
  ],
  "video-3": [], // nothing happened
};

export function getMockMoments(
  videoId: string,
  timestampStart: number,
  timestampEnd: number,
): ImportantMomentsResponse {
  const moments = MOCK_MOMENTS[videoId] ?? [];
  return moments.filter(
    (m) =>
      m.videoTimestamp >= timestampStart && m.videoTimestamp <= timestampEnd,
  );
}
