import type { ImportantMomentsResponse, MatchesResponse, EventsFilter, EventsResponse, BsdEvent } from "./types";

export class Api {
  baseUrl: string;
  constructor() {
    this.baseUrl = "http://localhost:8000";
  }

  /**
   * Builds a URL for the API.
   * @param base The base URL for the API.
   * @param path The path to append to the base URL.
   * @param params The query parameters to append to the URL.
   * @returns The built URL.
   */
  private buildUrl(base: string, path: string = "", params?: Record<string, any>): string {
    let url = base.replace(/\/+$/, "") + "/" + path.replace(/^\/+/, "");
    if (params && Object.keys(params).length > 0) {
      const query = Object.entries(params)
        .filter(([_, v]) => v !== undefined && v !== null)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
        .join("&");
      url += `?${query}`;
    }
    return url;
  }

  private eventToMatch(event: BsdEvent): MatchesResponse[number] {
    return {
      id: String(event.id),
      homeTeam: { name: event.home_team, flag: "" },
      awayTeam: { name: event.away_team, flag: "" },
      url: event.video_filename ?? "",
    };
  }

  public async getMatches(): Promise<MatchesResponse> {
    const events = await this.getEvents();
    return events.results.map((e) => this.eventToMatch(e));
  }

  public async getEvents(filter: EventsFilter = {}): Promise<EventsResponse> {
    const url = this.buildUrl(this.baseUrl, "/events/", filter);
    const res = await fetch(url);
    return res.json() as Promise<EventsResponse>;
  }

  public async getLiveImportantMoments(
    videoId: string,
    timestampStart: number,
    timestampEnd: number,
  ): Promise<ImportantMomentsResponse> {
    const url = this.buildUrl(this.baseUrl, `/${videoId}/important-moments`, {
      start: timestampStart,
      end: timestampEnd,
    });
    const res = await fetch(url);
    return res.json() as Promise<ImportantMomentsResponse>;
  }
}

export const api = new Api();
