import asyncio
import logging
import math
import struct
from pathlib import Path

import ffmpeg

from ai.client import AiClient
from ai.narrator import NarratorStyle, generate_narration
from ai.stt.segmenter import HLS_OUTPUT_DIR
from config import CHUNK_DURATION_SECONDS

log = logging.getLogger(__name__)

_SAMPLE_RATE = 24000
_CHANNELS = 1
_BIT_DEPTH = 16


def _narrated_dir(event_id: int) -> Path:
    return HLS_OUTPUT_DIR / f"{event_id}_narrated"


def _segment_path(event_id: int, chunk_index: int) -> Path:
    return _narrated_dir(event_id) / f"segment_{chunk_index:03d}.ts"


def _wav_path(event_id: int, chunk_index: int) -> Path:
    return _narrated_dir(event_id) / f"segment_{chunk_index:03d}.wav"


def _pcm_to_wav(pcm: bytes) -> bytes:
    data_size = len(pcm)
    byte_rate = _SAMPLE_RATE * _CHANNELS * _BIT_DEPTH // 8
    block_align = _CHANNELS * _BIT_DEPTH // 8
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", data_size + 36, b"WAVE",
        b"fmt ", 16, 1, _CHANNELS, _SAMPLE_RATE,
        byte_rate, block_align, _BIT_DEPTH,
        b"data", data_size,
    )
    return header + pcm


def get_video_duration(url: str) -> float:
    log.info("probing video duration: %s", url[:60])
    probe = ffmpeg.probe(url, v="quiet", show_entries="format=duration", timeout=30000000)  # type: ignore
    duration = float(probe["format"]["duration"])
    log.info("video duration: %.1fs", duration)
    return duration


def get_num_segments(url: str) -> int:
    return math.ceil(get_video_duration(url) / CHUNK_DURATION_SECONDS)


def build_hls_manifest(num_segments: int) -> str:
    lines = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        f"#EXT-X-TARGETDURATION:{CHUNK_DURATION_SECONDS}",
        "#EXT-X-PLAYLIST-TYPE:VOD",
    ]
    for i in range(num_segments):
        lines += [f"#EXTINF:{CHUNK_DURATION_SECONDS}.0,", f"narrated-stream/{i}"]
    lines.append("#EXT-X-ENDLIST")
    return "\n".join(lines)


def _mux_segment(url: str, chunk_index: int, narration_wav: Path, output: Path) -> None:
    chunk_start = chunk_index * CHUNK_DURATION_SECONDS
    video_in = ffmpeg.input(url, ss=chunk_start, t=CHUNK_DURATION_SECONDS)  # type: ignore[attr-defined]
    audio_in = ffmpeg.input(str(narration_wav))  # type: ignore[attr-defined]
    out = ffmpeg.output(video_in["v"], audio_in["a"], str(output), format="mpegts", vcodec="copy", acodec="aac")  # type: ignore[attr-defined]
    out.overwrite_output().run(quiet=True)


async def generate_narrated_segment(event_id: int, url: str, chunk_index: int) -> Path:
    output = _segment_path(event_id, chunk_index)
    if output.exists():
        log.info("[segment %d] cache hit", chunk_index)
        return output

    _narrated_dir(event_id).mkdir(parents=True, exist_ok=True)
    chunk_start = chunk_index * CHUNK_DURATION_SECONDS
    chunk_end = chunk_start + CHUNK_DURATION_SECONDS
    style = NarratorStyle()

    log.info("[segment %d] transcribing + narrating [%ds-%ds]", chunk_index, chunk_start, chunk_end)
    narration_text = await generate_narration(event_id, url, style, chunk_start, chunk_end)
    log.info("[segment %d] narration text (%d chars): %s", chunk_index, len(narration_text), narration_text[:120])

    log.info("[segment %d] TTS...", chunk_index)
    pcm = AiClient().generate_speech(narration_text, voice_name=style.voice)
    if not pcm:
        raise ValueError(f"TTS returned no audio for segment {chunk_index}")
    log.info("[segment %d] TTS done (%d bytes PCM)", chunk_index, len(pcm))

    wav = _wav_path(event_id, chunk_index)
    wav.write_bytes(_pcm_to_wav(pcm))

    log.info("[segment %d] muxing video + narration audio...", chunk_index)
    await asyncio.to_thread(_mux_segment, url, chunk_index, wav, output)
    wav.unlink(missing_ok=True)
    log.info("[segment %d] done → %s", chunk_index, output)

    return output
