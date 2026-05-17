import asyncio
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path

from pydantic import BaseModel

from ai.client import AiClient
from ai.stt.models import TranscriptSegment
from ai.stt.stt_client import STTClient
from config import CHUNK_DURATION_SECONDS
from models import ImportantMoment

log = logging.getLogger(__name__)

DisconnectCheck = Callable[[], Awaitable[bool]] | None


def _build_prompt(video_id: str, segments: list[TranscriptSegment]) -> str:
    transcript_text = "\n".join(
        f"[{s.start:.1f}s -> {s.end:.1f}s] {s.text.strip()}" for s in segments
    )
    return f"""You are a sports broadcast analyst. Below is a timestamped transcript of commentary from a football (soccer) match video with id "{video_id}".

Identify ALL notable moments. Include anything that sounds exciting or significant. Types ranked by importance:
- "goal": goal scored
- "red_card": player sent off
- "yellow_card": booking
- "var_decision": VAR review or decision
- "substitution": player substitution
- "penalty": penalty awarded or saved
- "near_miss": close chance, shot on target, great save
- "free_kick": dangerous free kick
- "corner": corner kick leading to danger
- "highlight": any other notable moment worth flagging
- "attack": "really good attack that is worth highlighting"

For each moment return:
- type: one of the types listed above
- videoId: "{video_id}"
- videoTimestamp: the start time in seconds of the moment from the transcript
- importanceScore: a float between 0.0 and 1.0 reflecting significance
- priorityDuration: seconds to stay highlighted (goal=10, red_card=8, penalty=8, near_miss=5, yellow_card=5, var_decision=6, substitution=4, free_kick=4, corner=3, highlight=5)

Return an empty list only if the transcript contains no match action at all.

Transcript:
{transcript_text}"""


# Gemini requires an object schema, not a bare list — this wrapper satisfies that
class _ImportantMomentResponse(BaseModel):
    moments: list[ImportantMoment]


async def transcribe_and_analyze(video_id: str, url: str) -> list[ImportantMoment]:
    stt = STTClient()
    ai = AiClient()

    segments = await stt.transcribe_video_url(url)
    prompt = _build_prompt(video_id, segments)
    result = await asyncio.to_thread(ai.generate_structured_content, prompt, _ImportantMomentResponse)
    return result.moments


async def transcribe_and_analyze_segment(
    video_id: str,
    segment_path: Path,
    chunk_index: int,
    is_disconnected: DisconnectCheck = None,
) -> list[ImportantMoment]:
    stt = STTClient()

    segments = await stt.transcribe_local_file(segment_path)

    offset = chunk_index * CHUNK_DURATION_SECONDS
    for s in segments:
        s.start += offset
        s.end += offset

    log.info("[chunk %d] transcript:\n%s", chunk_index, "\n".join(f"  [{s.start:.1f}s] {s.text.strip()}" for s in segments))

    if is_disconnected and await is_disconnected():
        log.info("[chunk %d] client disconnected after transcription, skipping Gemini", chunk_index)
        return []

    ai = AiClient()
    prompt = _build_prompt(video_id, segments)
    result = await asyncio.to_thread(ai.generate_structured_content, prompt, _ImportantMomentResponse)
    log.info("[chunk %d] moments: %s", chunk_index, result.moments)
    return result.moments
