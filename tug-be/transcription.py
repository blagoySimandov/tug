import os
import tempfile

import httpx
from fastapi import HTTPException
from openai import OpenAI


class TranscriptSegment:
    def __init__(self, start: float, end: float, text: str):
        self.start = start
        self.end = end
        self.text = text


async def transcribe_video_url(url: str) -> list[TranscriptSegment]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async with httpx.AsyncClient(timeout=120) as http:
        response = await http.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to download video")

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    mp3_path = tmp_path.replace(".mp4", ".mp3")
    try:
        os.system(f'ffmpeg -i "{tmp_path}" -vn -af "highpass=f=200,afftdn=nf=-25,equalizer=f=1000:width_type=o:width=2:g=4,dynaudnorm" -acodec mp3 -q:a 2 "{mp3_path}" -y -loglevel quiet')
        with open(mp3_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
            )
    finally:
        os.remove(tmp_path)
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

    return [
        TranscriptSegment(start=s.start, end=s.end, text=s.text)
        for s in transcript.segments
    ]
