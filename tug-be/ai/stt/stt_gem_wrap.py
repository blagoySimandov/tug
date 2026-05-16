from pydantic import BaseModel

from ai.client import AiClient
from ai.stt.models import TranscriptSegment
from ai.stt.stt_client import STTClient
from models import ImportantMoment


def _build_prompt(video_id: str, segments: list[TranscriptSegment]) -> str:
    transcript_text = "\n".join(
        f"[{s.start:.1f}s -> {s.end:.1f}s] {s.text.strip()}"
        for s in segments
    )
    return f"""You are a sports broadcast analyst. Below is a timestamped transcript of commentary from a football (soccer) match video with id "{video_id}".

Identify all important moments: goals and red cards. For each moment return:
- type: either "goal" or "red_card"
- videoId: "{video_id}"
- videoTimestamp: the start time in seconds of the moment from the transcript
- importanceScore: a float between 0.0 and 1.0 reflecting how significant this moment is
- priorityDuration: how many seconds this moment should stay highlighted (e.g. 8 for a goal, 6 for a red card)

Only include moments you are confident about based on the commentary. If no moments are found, return an empty list.

Transcript:
{transcript_text}"""


class _ImportantMomentResponse(BaseModel):
    moments: list[ImportantMoment]


async def transcribe_and_analyze(video_id: str, url: str) -> list[ImportantMoment]:
    stt = STTClient()
    ai = AiClient()

    segments = await stt.transcribe_video_url(url)
    prompt = _build_prompt(video_id, segments)
    result = ai.generate_structured_content(prompt, _ImportantMomentResponse)
    return result.moments
