import logging
from pathlib import Path
from io import BytesIO
from os import environ

import av
import ffmpeg
from fastapi import HTTPException
from openai import OpenAI

from .models import TranscriptSegment

log = logging.getLogger(__name__)

_AUDIO_FILTERS = "highpass=f=200,afftdn=nf=-25,equalizer=f=1000:width_type=o:width=2:g=4,dynaudnorm"


def _fetch_audio_from_url(url: str, start: float = 0, duration: float | None = None) -> BytesIO:
    input_kwargs: dict = {"ss": start} if start > 0 else {}
    output_kwargs: dict = {"format": "mp3", "af": _AUDIO_FILTERS, "ac": 1, "ar": "22050"}
    if duration is not None:
        output_kwargs["t"] = duration
    stream = ffmpeg.input(url, **input_kwargs).output("pipe:", **output_kwargs)  # type: ignore[attr-defined]
    raw, _ = stream.run(capture_output=True, quiet=True)
    buf = BytesIO(raw)
    buf.name = "audio.mp3"
    return buf


def _build_filter_graph(audio):
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
    return graph


def _drain_graph(graph, out_stream, out_container):
    while True:
        try:
            filtered = graph.pull()
        except av.error.BlockingIOError:  # type: ignore
            break
        for packet in out_stream.encode(filtered):
            out_container.mux(packet)


def _flush_graph(graph, out_stream, out_container):
    graph.push(None)
    while True:
        try:
            filtered = graph.pull()
        except (av.error.BlockingIOError, av.error.EOFError):  # type: ignore
            break
        for packet in out_stream.encode(filtered):
            out_container.mux(packet)
    for packet in out_stream.encode(None):
        out_container.mux(packet)


def _process_frames(in_container, audio, graph, out_stream, out_container, end: float):
    for packet in in_container.demux(audio):  # type: ignore
        for frame in packet.decode():
            if frame.pts is not None and float(frame.pts * frame.time_base) >= end:
                return
            graph.push(frame)
            _drain_graph(graph, out_stream, out_container)


def _convert_to_filtered_mp3(source: BytesIO, start: float = 0, end: float = float("inf")) -> BytesIO:
    out = BytesIO()
    with av.open(source) as inc:  # type: ignore
        audio = inc.streams.audio[0]
        if start > 0:
            inc.seek(int(start * 1_000_000), stream=audio)  # type: ignore
        graph = _build_filter_graph(audio)
        with av.open(out, "w", format="mp3") as outc:  # type: ignore
            out_stream = outc.add_stream("mp3")
            _process_frames(inc, audio, graph, out_stream, outc, end)
            _flush_graph(graph, out_stream, outc)
    out.seek(0)
    return out


class STTClient:
    def __init__(self):
        self.client = OpenAI(api_key=environ["OPENAI_API_KEY"])

    def _run_whisper(self, audio: BytesIO) -> list[TranscriptSegment]:
        audio.name = "audio.mp3"
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", file=audio, response_format="verbose_json"
        )
        if transcript.segments is None:
            raise HTTPException(status_code=502, detail="Failed to transcribe")
        return [TranscriptSegment(start=s.start, end=s.end, text=s.text) for s in transcript.segments]

    async def transcribe_local_file(self, path: Path) -> list[TranscriptSegment]:
        src = BytesIO(path.read_bytes())
        src.name = path.name
        return self._run_whisper(_convert_to_filtered_mp3(src))

    async def transcribe_video_url(self, url: str) -> list[TranscriptSegment]:
        log.info("extracting full audio from url via ffmpeg")
        return self._run_whisper(_fetch_audio_from_url(url))

    async def transcribe_video_url_window(self, url: str, start: float, end: float) -> list[TranscriptSegment]:
        log.info("extracting audio [%.0fs-%.0fs] from url via ffmpeg", start, end)
        audio = _fetch_audio_from_url(url, start, end - start)
        log.info("audio extracted, sending to Whisper")
        segments = self._run_whisper(audio)
        log.info("Whisper done: %d segments", len(segments))
        for s in segments:
            s.start += start
            s.end += start
        return segments
