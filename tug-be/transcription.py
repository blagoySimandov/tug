import os
import tempfile

import av
import httpx
from fastapi import HTTPException
from openai import OpenAI


class TranscriptSegment:
    def __init__(self, start: float, end: float, text: str):
        self.start = start
        self.end = end
        self.text = text


def _convert_to_filtered_mp3(input_path: str, output_path: str) -> None:
    with av.open(input_path) as in_container:
        audio = in_container.streams.audio[0]

        graph = av.filter.Graph()
        abuffer = graph.add_abuffer(template=audio)
        highpass = graph.add("highpass", "f=200")
        afftdn = graph.add("afftdn", "nf=-25")
        equalizer = graph.add("equalizer", "f=1000:width_type=o:width=2:g=4")
        dynaudnorm = graph.add("dynaudnorm")
        abuffersink = graph.add("abuffersink")

        abuffer.link_to(highpass)
        highpass.link_to(afftdn)
        afftdn.link_to(equalizer)
        equalizer.link_to(dynaudnorm)
        dynaudnorm.link_to(abuffersink)
        graph.configure()

        with av.open(output_path, "w", format="mp3") as out_container:
            out_stream = out_container.add_stream("mp3")

            for packet in in_container.demux(audio):
                for frame in packet.decode():
                    graph.push(frame)
                    while True:
                        try:
                            filtered = graph.pull()
                        except av.error.BlockingIOError:
                            break
                        for out_packet in out_stream.encode(filtered):
                            out_container.mux(out_packet)

            graph.push(None)
            while True:
                try:
                    filtered = graph.pull()
                except (av.error.BlockingIOError, av.error.EOFError):
                    break
                for out_packet in out_stream.encode(filtered):
                    out_container.mux(out_packet)

            for out_packet in out_stream.encode(None):
                out_container.mux(out_packet)


_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


async def transcribe_video_url(url: str) -> list[TranscriptSegment]:

    async with httpx.AsyncClient(timeout=120) as http:
        response = await http.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to download video")

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    mp3_path = tmp_path.replace(".mp4", ".mp3")
    try:
        _convert_to_filtered_mp3(tmp_path, mp3_path)
        with open(mp3_path, "rb") as audio_file:
            transcript = _get_client().audio.transcriptions.create(
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
