import { useQuery } from "@tanstack/react-query";
import { useApi } from "./context";
import type { ImportantMomentsResponse, MatchesResponse } from "./types";

export function useMatches() {
  const api = useApi();
  return useQuery<MatchesResponse>({
    queryKey: ["matches"],
    queryFn: () => api.getMatches(),
  });
}

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
