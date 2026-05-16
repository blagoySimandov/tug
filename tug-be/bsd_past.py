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
