from fastapi import APIRouter
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

_HARDCODED_EVENTS: list[BsdEvent] = [
    BsdEvent(
        id=1,
        league_id=7,
        league_name="UEFA Champions League",
        home_team="Bayern Munich",
        away_team="Real Madrid",
        event_date="2026-04-15",
        status="finished",
        home_score=None,
        away_score=None,
        video_filename="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Bayern_Vs_Real_Madrid_-_15042026-1_edit.mp4?alt=media&token=43bc1090-5431-431a-bbaa-bea89f08c34f",
        kickoff_time=None,  # TODO: set kickoff time e.g. "20:45"
    ),
    BsdEvent(
        id=2,
        league_id=7,
        league_name="UEFA Champions League",
        home_team="Paris Saint-Germain",
        away_team="Chelsea",
        event_date="2026-03-11",
        status="finished",
        home_score=None,
        away_score=None,
        video_filename="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Paris_Saint-Germain_Vs_Chelsea_-_11032026-1.mp4?alt=media&token=1b91a829-1ded-4599-95d9-925d0611003f",
        kickoff_time=None,  # TODO: set kickoff time e.g. "20:45"
    ),
    BsdEvent(
        id=3,
        league_id=7,
        league_name="UEFA Champions League",
        home_team="Atalanta",
        away_team="Bayern Munich",
        event_date="2026-03-10",
        status="finished",
        home_score=None,
        away_score=None,
        video_filename="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Atalanta_Vs_Bayern_Munich_-_10032026-1_edit.mp4?alt=media&token=8aa301de-5a22-445b-861c-9d130f4be1a9",
        kickoff_time=None,  # TODO: set kickoff time e.g. "20:45"
    ),
    BsdEvent(
        id=4,
        league_id=7,
        league_name="UEFA Champions League",
        home_team="Galatasaray",
        away_team="Liverpool",
        event_date="2026-03-10",
        status="finished",
        home_score=None,
        away_score=None,
        video_filename="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Galatasaray_Vs_Liverpool_-_10032026-1.mp4?alt=media&token=a2852566-7ff8-4adb-a933-ec81831bb6eb",
        kickoff_time=None,  # TODO: set kickoff time e.g. "20:45"
    ),
    BsdEvent(
        id=5,
        league_id=7,
        league_name="UEFA Champions League",
        home_team="Juventus",
        away_team="Galatasaray",
        event_date="2026-02-25",
        status="finished",
        home_score=None,
        away_score=None,
        video_filename="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Juventus_Vs_Galatasaray_-_25022026-1_edit_-_1.mp4?alt=media&token=054df9f1-d8c0-4e38-97ce-22c442db6996",
        kickoff_time=None,  # TODO: set kickoff time e.g. "20:45"
    ),
]


@router.get("/", response_model=EventsListResponse)
async def list_events():
    return EventsListResponse(count=len(_HARDCODED_EVENTS), results=_HARDCODED_EVENTS)


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
