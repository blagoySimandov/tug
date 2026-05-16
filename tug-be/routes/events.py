from fastapi import APIRouter, Query
import bsd_past
from models import (
    BsdEvent,
    EventsListResponse,
    EventLineups,
    EventMetadata,
    EventStats,
    Incident,
    MatchSnapshot,
    PlayerStat,
)

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=EventsListResponse)
async def list_events(
    year: int | None = Query(None),
    league_id: int | None = Query(None),
    team_name: str | None = Query(None),
    team_id: int | None = Query(None),
    status: str | None = Query(None),
    limit: int = Query(20, le=20),
    offset: int = Query(0),
):
    return await bsd_past.get_events(year, league_id, team_name, team_id, status, limit, offset)


@router.get("/{event_id}", response_model=BsdEvent)
async def get_event(event_id: int):
    return await bsd_past.get_event(event_id)


@router.get("/{event_id}/incidents", response_model=list[Incident])
async def get_incidents(event_id: int):
    return await bsd_past.get_incidents(event_id)


@router.get("/{event_id}/stats", response_model=EventStats)
async def get_stats(event_id: int):
    return await bsd_past.get_stats(event_id)


@router.get("/{event_id}/metadata", response_model=EventMetadata)
async def get_metadata(event_id: int):
    return await bsd_past.get_metadata(event_id)


@router.get("/{event_id}/lineups", response_model=EventLineups)
async def get_lineups(event_id: int):
    return await bsd_past.get_lineups(event_id)


@router.get("/{event_id}/player-stats", response_model=list[PlayerStat])
async def get_player_stats(event_id: int):
    return await bsd_past.get_player_stats(event_id)


@router.get("/{event_id}/snapshot", response_model=MatchSnapshot)
async def get_match_snapshot(event_id: int):
    return await bsd_past.get_match_snapshot(event_id)
