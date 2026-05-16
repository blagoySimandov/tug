import type { ImportantMomentsResponse } from "./types";
import { getMockMoments } from "./mock-data";

// Flip to false when backend is ready
const USE_MOCK = true;

export class Api {
  baseUrl: string;
  constructor() {
    this.baseUrl = "https://tug-splitball.web.app/api"; //TODO: Change to live
  }

  /**
   * Builds a URL for the API.
   * @param base The base URL for the API.
   * @param path The path to append to the base URL.
   * @param params The query parameters to append to the URL.
   * @returns The built URL.
   */
  private buildUrl(
    base: string,
    path: string = "",
    params?: Record<string, any>,
  ): string {
    let url = base.replace(/\/+$/, "") + "/" + path.replace(/^\/+/, "");
    if (params && Object.keys(params).length > 0) {
      const query = Object.entries(params)
        .filter(([_, v]) => v !== undefined && v !== null)
        .map(
          ([k, v]) =>
            `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`,
        )
        .join("&");
      url += `?${query}`;
    }
    return url;
  }

  /**
   * Gets the "important moments" for a video.
   * @param videoId The ID of the video to get segments for.
   * @returns The segments for the video.
   */
  public async getLiveImportantMoments(
    videoId: string,
    timestampStart: number,
    timestampEnd: number,
  ): Promise<ImportantMomentsResponse> {
    if (USE_MOCK) {
      return getMockMoments(videoId, timestampStart, timestampEnd);
    }
    const url = this.buildUrl(this.baseUrl, `/${videoId}/important-moments`, {
      start: timestampStart,
      end: timestampEnd,
    });
    const res = await fetch(url);
    return res.json() as Promise<ImportantMomentsResponse>;
  }
}

export const api = new Api();
