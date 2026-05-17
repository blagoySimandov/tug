import { useQuery } from "@tanstack/react-query";
import { useApi } from "./context";
import type { ImportantMomentsResponse, MatchesResponse, EventsFilter, EventsResponse } from "./types";

export function useEvents(filter: EventsFilter = {}) {
  const api = useApi();
  return useQuery<EventsResponse>({
    queryKey: ["events", filter],
    queryFn: () => api.getEvents(filter),
  });
}

export function useMatches() {
  const api = useApi();
  return useQuery<MatchesResponse>({
    queryKey: ["matches"],
    queryFn: () => api.getMatches(),
  });
}

export function useLiveImportantMoments(videoId: string, timestampStart: number, timestampEnd: number) {
  const api = useApi();
  return useQuery<ImportantMomentsResponse>({
    queryKey: ["importantMoments", videoId, timestampStart, timestampEnd],
    queryFn: ({ signal }) => api.getLiveImportantMoments(videoId, timestampStart, timestampEnd, signal).then((data) => { console.log("important moments", data); return data; }),
    enabled: !!videoId,
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  });
}
