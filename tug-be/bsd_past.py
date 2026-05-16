import asyncio
import os
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://sports.bzzoiro.com/api/v2"


def _http() -> httpx.AsyncClient:
    token = os.environ["BSD_TOKEN"].strip().strip('"')
    return httpx.AsyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Token {token}"},
        timeout=10.0,
    )


async def get_events(
    year: int | None = None,
    league_id: int | None = None,
    team_name: str | None = None,
    team_id: int | None = None,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    params: dict = {"limit": limit, "offset": offset}
    if year is not None:
        params["date_from"] = f"{year}-01-01"
        params["date_to"] = f"{year}-12-31"
    if league_id is not None:
        params["league_id"] = league_id
    if team_name is not None:
        params["team_name"] = team_name
    if team_id is not None:
        params["team_id"] = team_id
    if status is not None:
        params["status"] = status
    async with _http() as c:
        r = await c.get("/events/", params=params)
        r.raise_for_status()
        return r.json()


async def get_event(event_id: int) -> dict:
    async with _http() as c:
        r = await c.get(f"/events/{event_id}/")
        r.raise_for_status()
        return r.json()


async def get_incidents(event_id: int) -> list:
    async with _http() as c:
        r = await c.get(f"/events/{event_id}/incidents/")
        r.raise_for_status()
        data = r.json()
        return data.get("incidents", data) if isinstance(data, dict) else data


async def get_stats(event_id: int) -> dict:
    async with _http() as c:
        r = await c.get(f"/events/{event_id}/stats/")
        r.raise_for_status()
        return r.json()


async def get_metadata(event_id: int) -> dict:
    async with _http() as c:
        r = await c.get(f"/events/{event_id}/metadata/")
        r.raise_for_status()
        return r.json()


async def get_lineups(event_id: int) -> dict:
    async with _http() as c:
        r = await c.get(f"/events/{event_id}/lineups/")
        r.raise_for_status()
        return r.json()


async def get_player_stats(event_id: int) -> list:
    async with _http() as c:
        r = await c.get(f"/events/{event_id}/player-stats/")
        r.raise_for_status()
        return r.json()


async def get_match_snapshot(event_id: int) -> dict[str, Any]:
    """All match data fetched concurrently. Ready to pass to Gemini."""
    event, metadata, stats, incidents, lineups, player_stats = await asyncio.gather(
        get_event(event_id),
        get_metadata(event_id),
        get_stats(event_id),
        get_incidents(event_id),
        get_lineups(event_id),
        get_player_stats(event_id),
        return_exceptions=True,
    )
    return {
        "event_id": event_id,
        "event": event if not isinstance(event, Exception) else None,
        "metadata": metadata if not isinstance(metadata, Exception) else None,
        "stats": stats if not isinstance(stats, Exception) else None,
        "incidents": incidents if not isinstance(incidents, Exception) else None,
        "lineups": lineups if not isinstance(lineups, Exception) else None,
        "player_stats": player_stats
        if not isinstance(player_stats, Exception)
        else None,
    }
