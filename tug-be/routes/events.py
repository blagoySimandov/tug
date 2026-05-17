import asyncio
import logging
from dataclasses import dataclass
from enum import IntEnum

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse

log = logging.getLogger(__name__)

import bsd_past
import narrated_segmenter  # type: ignore[import-untyped]
from models import (
    BsdEvent,
    EventLineups,
    EventMetadata,
    EventStats,
    EventsListResponse,
    Incident,
    MatchSnapshot,
    PlayerStat,
)

router = APIRouter(prefix="/events", tags=["events"])


class Match(IntEnum):
    BAYERN_VS_REAL_MADRID = 7716
    PSG_VS_CHELSEA = 7586
    ATALANTA_VS_BAYERN = 7583
    GALATASARAY_VS_LIVERPOOL = 7580
    JUVENTUS_VS_GALATASARAY = 7387


_LOGO = "/team-logo/{}.png"

@dataclass
class MatchConfig:
    home_team: str
    away_team: str
    event_date: str
    video_url: str
    kickoff_offset: float  # seconds into video when kickoff occurs
    home_team_logo: str = ""
    away_team_logo: str = ""


# ── Configure matches here ───────────────────────────────────────────────────
MATCHES: dict[Match, MatchConfig] = {
    Match.BAYERN_VS_REAL_MADRID: MatchConfig(
        home_team="Bayern Munich",
        away_team="Real Madrid",
        event_date="2026-04-15",
        video_url="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Bayern_Vs_Real_Madrid_-_15042026-1_edit.mp4?alt=media&token=43bc1090-5431-431a-bbaa-bea89f08c34f",
        kickoff_offset=0,
        home_team_logo=_LOGO.format("BAY"),
        away_team_logo=_LOGO.format("RMA"),
    ),
    Match.PSG_VS_CHELSEA: MatchConfig(
        home_team="Paris Saint-Germain",
        away_team="Chelsea",
        event_date="2026-03-11",
        video_url="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Paris_Saint-Germain_Vs_Chelsea_-_11032026-1.mp4?alt=media&token=1b91a829-1ded-4599-95d9-925d0611003f",
        kickoff_offset=0,
        home_team_logo=_LOGO.format("PSG"),
        away_team_logo=_LOGO.format("CHE"),
    ),
    Match.ATALANTA_VS_BAYERN: MatchConfig(
        home_team="Atalanta",
        away_team="Bayern Munich",
        event_date="2026-03-10",
        video_url="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Atalanta_Vs_Bayern_Munich_-_10032026-1_edit.mp4?alt=media&token=8aa301de-5a22-445b-861c-9d130f4be1a9",
        kickoff_offset=0,
        home_team_logo=_LOGO.format("ATA"),
        away_team_logo=_LOGO.format("BAY"),
    ),
    Match.GALATASARAY_VS_LIVERPOOL: MatchConfig(
        home_team="Galatasaray",
        away_team="Liverpool",
        event_date="2026-03-10",
        video_url="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Galatasaray_Vs_Liverpool_-_10032026-1.mp4?alt=media&token=a2852566-7ff8-4adb-a933-ec81831bb6eb",
        kickoff_offset=0,
        home_team_logo=_LOGO.format("GAL"),
        away_team_logo=_LOGO.format("LIV"),
    ),
    Match.JUVENTUS_VS_GALATASARAY: MatchConfig(
        home_team="Juventus",
        away_team="Galatasaray",
        event_date="2026-02-25",
        video_url="https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/2025-26_Juventus_Vs_Galatasaray_-_25022026-1_edit_-_1.mp4?alt=media&token=054df9f1-d8c0-4e38-97ce-22c442db6996",
        kickoff_offset=0,
        home_team_logo=_LOGO.format("JUV"),
        away_team_logo=_LOGO.format("GAL"),
    ),
}
# ─────────────────────────────────────────────────────────────────────────────


def get_kickoff_offset(bsd_event_id: int) -> float:
    try:
        return MATCHES[Match(bsd_event_id)].kickoff_offset
    except ValueError:
        return 0


def _to_bsd_event(match: Match, cfg: MatchConfig) -> BsdEvent:
    return BsdEvent(
        id=int(match),
        league_id=7,
        league_name="UEFA Champions League",
        home_team=cfg.home_team,
        away_team=cfg.away_team,
        event_date=cfg.event_date,
        status="finished",
        video_filename=cfg.video_url,
        kickoff_offset=cfg.kickoff_offset,
        home_team_logo=cfg.home_team_logo or None,
        away_team_logo=cfg.away_team_logo or None,
    )


_EVENTS = [_to_bsd_event(m, cfg) for m, cfg in MATCHES.items()]


@router.get("/", response_model=EventsListResponse)
async def list_events():
    return EventsListResponse(count=len(_EVENTS), results=_EVENTS)


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


def _get_match_config(event_id: int) -> MatchConfig:
    try:
        cfg = MATCHES.get(Match(event_id))
    except ValueError:
        cfg = None
    if cfg is None:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return cfg


@router.get("/{event_id}/narrated-stream.m3u8")
async def get_narrated_playlist(event_id: int):
    cfg = _get_match_config(event_id)
    log.info("narrated playlist requested for event %d", event_id)
    num_segments = await asyncio.to_thread(narrated_segmenter.get_num_segments, cfg.video_url)
    manifest = narrated_segmenter.build_hls_manifest(num_segments)
    log.info("narrated playlist: %d segments", num_segments)
    return PlainTextResponse(manifest, media_type="application/vnd.apple.mpegurl")


@router.get("/{event_id}/narrated-stream/{chunk_index}")
async def get_narrated_segment(event_id: int, chunk_index: int):
    cfg = _get_match_config(event_id)
    log.info("narrated segment %d requested for event %d", chunk_index, event_id)
    segment_path = await narrated_segmenter.generate_narrated_segment(event_id, cfg.video_url, chunk_index)
    return FileResponse(str(segment_path), media_type="video/mp2t")
