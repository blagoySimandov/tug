from fastapi import HTTPException
from openai import OpenAI
from os import environ
from .models import TranscriptSegment
import av
from httpx import get
from io import BytesIO


class STTClient:
    """Client for OpenAI's Speech-to-Text API."""

    def __init__(self):
        self.client = OpenAI(api_key=environ["OPENAI_API_KEY"])

    async def transcribe_video_url(self, url: str) -> list[TranscriptSegment]:
        response = get(url)
        bytes_io = BytesIO(response.content)
        bytes_io.name = "video.mp4"
        converted = _convert_to_filtered_mp3(bytes_io)
        converted.name = "audio.mp3"
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=converted,
            response_format="verbose_json",
        )
        if transcript.segments is None:
            raise HTTPException(status_code=502, detail="Failed to transcribe video")
        return [
            TranscriptSegment(start=s.start, end=s.end, text=s.text)
            for s in transcript.segments
        ]


def _convert_to_filtered_mp3(input: BytesIO) -> BytesIO:
    output_buffer = BytesIO()
    with av.open(input) as in_container:
        audio = in_container.streams.audio[0]
        graph = av.filter.Graph()  # type: ignore
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
        with av.open(output_buffer, "w", format="mp3") as out_container:
            out_stream = out_container.add_stream("mp3")
            for packet in in_container.demux(audio):  # type: ignore
                for frame in packet.decode():
                    graph.push(frame)
                    while True:
                        try:
                            filtered = graph.pull()
                        except av.error.BlockingIOError:  # type: ignore
                            break
                        for out_packet in out_stream.encode(filtered):
                            out_container.mux(out_packet)
            graph.push(None)
            while True:
                try:
                    filtered = graph.pull()
                except (av.error.BlockingIOError, av.error.EOFError):  # type: ignore
                    break
                for out_packet in out_stream.encode(filtered):
                    out_container.mux(out_packet)
            for out_packet in out_stream.encode(None):
                out_container.mux(out_packet)

    output_buffer.seek(0)
    return output_buffer
