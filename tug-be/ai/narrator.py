import asyncio
import logging
from typing import Any

from pydantic import BaseModel

import bsd_past
from ai.client import AiClient
from ai.stt.models import TranscriptSegment
from ai.stt.stt_client import STTClient

log = logging.getLogger(__name__)


class NarratorStyle(BaseModel):
    temperature: float = 1.2
    persona: str = "electrifying"
    target_duration_seconds: int = 60
    voice: AiClient.AvaillableTTSVoices = "Puck"


def _filter_snapshot(snapshot: dict[str, Any], window_start: float, window_end: float) -> dict[str, Any]:
    incidents = snapshot.get("incidents") or []
    filtered_incidents = [
        inc for inc in incidents
        if isinstance(inc, dict) and window_start <= (inc.get("minute", 0) + (inc.get("added_time") or 0)) * 60 <= window_end
    ]
    return {**snapshot, "incidents": filtered_incidents}


def _build_narrator_prompt(
    segments: list[TranscriptSegment],
    snapshot: dict[str, Any],
    style: NarratorStyle,
    window_start: float,
    window_end: float,
) -> str:
    event = snapshot.get("event") or {}
    home = event.get("home_team", "Home")
    away = event.get("away_team", "Away")
    league = event.get("league_name", "Unknown League")
    home_score = event.get("home_score", "?")
    away_score = event.get("away_score", "?")

    incidents = snapshot.get("incidents") or []
    incident_lines = []
    for inc in incidents:
        if not isinstance(inc, dict):
            continue
        t = inc.get("type", "")
        minute = inc.get("minute", "?")
        added = inc.get("added_time")
        time_str = f"{minute}+{added}'" if added else f"{minute}'"
        team = home if inc.get("is_home") else away
        player = inc.get("player_name") or inc.get("player", "")
        detail = f"{t} — {team}"
        if player:
            detail += f" ({player})"
        incident_lines.append(f"  {time_str}: {detail}")

    incidents_block = "\n".join(incident_lines) if incident_lines else "  (no key incidents in this window)"

    transcript_lines = "\n".join(
        f"[{s.start:.1f}s -> {s.end:.1f}s] {s.text.strip()}" for s in segments
    )

    return f"""You are a {style.persona} football (soccer) broadcast narrator preparing a script for text-to-speech playback.

Match: {home} vs {away} | {league}
Score at time of cut: {home_score} - {away_score}
Video window: {window_start:.0f}s to {window_end:.0f}s

Key incidents in this window:
{incidents_block}

Raw commentary transcript:
{transcript_lines}

Your task:
Write ONE continuous, uninterrupted narration script based on the transcript and match context above.

Rules:
- Output ONLY the narration text — no timestamps, no bullet points, no markdown, no headers
- Never leave dead air — bridge every silence with vivid commentary or atmosphere
- Treat the transcript as raw input; elevate and dramatize it into proper broadcast commentary
- Incorporate the match context and key incidents naturally
- Target approximately {style.target_duration_seconds} seconds when read aloud at broadcast pace
- Style: {style.persona} — match the energy level throughout
- End on a strong note, not mid-sentence

Begin the narration now:"""


async def generate_narration(
    event_id: int,
    url: str,
    style: NarratorStyle,
    window_start: float = 0,
    window_end: float = 300,
) -> str:
    stt = STTClient()
    ai = AiClient()

    log.info("transcribing [%.0fs-%.0fs]", window_start, window_end)
    segments, snapshot = await asyncio.gather(
        stt.transcribe_video_url_window(url, window_start, window_end),
        bsd_past.get_match_snapshot(event_id),
    )
    log.info("transcription done: %d segments", len(segments))

    filtered = _filter_snapshot(snapshot, window_start, window_end)
    prompt = _build_narrator_prompt(segments, filtered, style, window_start, window_end)
    log.info("calling Gemini for narration")
    result = await asyncio.to_thread(ai.generate_content, prompt, AiClient.DEFAULT_MODEL, style.temperature)
    log.info("Gemini narration done (%d chars)", len(result or ""))
    return result or ""


async def generate_narration_audio(
    event_id: int,
    url: str,
    style: NarratorStyle,
    window_start: float = 0,
    window_end: float = 300,
) -> bytes:
    narration = await generate_narration(event_id, url, style, window_start, window_end)
    ai = AiClient()
    audio = await asyncio.to_thread(ai.generate_speech, narration, style.voice)
    if not audio:
        raise ValueError("TTS returned no audio")
    return audio
