from pathlib import Path

from pydantic import BaseModel

from ai.client import AiClient
from ai.stt.models import TranscriptSegment
from ai.stt.stt_client import STTClient
from config import CHUNK_DURATION_SECONDS
from models import ImportantMoment


def _build_prompt(video_id: str, segments: list[TranscriptSegment]) -> str:
    transcript_text = "\n".join(
        f"[{s.start:.1f}s -> {s.end:.1f}s] {s.text.strip()}" for s in segments
    )
    return f"""You are a sports broadcast analyst. Below is a timestamped transcript of commentary from a football (soccer) match video with id "{video_id}".

Identify all important moments: goal, red_card, yellow_card, var_decision, substitution (in this order of importance). For each moment return:
- type: either "goal", "red_card", "yellow_card", "var_decision", "substitution"
- videoId: "{video_id}"
- videoTimestamp: the start time in seconds of the moment from the transcript
- importanceScore: a float between 0.0 and 1.0 reflecting how significant this moment is
- priorityDuration: how many seconds this moment should stay highlighted (e.g. 8 for a goal, 6 for a red card)

Only include moments you are confident about based on the commentary. If no moments are found, return an empty list.

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
    result = ai.generate_structured_content(prompt, _ImportantMomentResponse)
    return result.moments


async def transcribe_and_analyze_segment(
    video_id: str, segment_path: Path, chunk_index: int
) -> list[ImportantMoment]:
    stt = STTClient()
    ai = AiClient()

    segments = await stt.transcribe_local_file(segment_path)

    # Whisper timestamps are relative to the segment; shift them to absolute video time
    offset = chunk_index * CHUNK_DURATION_SECONDS
    for s in segments:
        s.start += offset
        s.end += offset

    prompt = _build_prompt(video_id, segments)
    result = ai.generate_structured_content(prompt, _ImportantMomentResponse)
    return result.moments
