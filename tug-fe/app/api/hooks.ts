import { useQuery } from "@tanstack/react-query";
import { useApi } from "./context";
import type { ImportantMomentsResponse } from "./types";

export function useLiveImportantMoments(
  videoId: string,
  timestampStart: number,
  timestampEnd: number,
) {
  const api = useApi();
  return useQuery<ImportantMomentsResponse>({
    queryKey: ["importantMoments", videoId, timestampStart, timestampEnd],
    queryFn: () => api.getLiveImportantMoments(videoId, timestampStart, timestampEnd),
  });
}
