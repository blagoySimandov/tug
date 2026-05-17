from pathlib import Path

import ffmpeg

from config import CHUNK_DURATION_SECONDS

# Segments live next to the project root, outside the package
HLS_OUTPUT_DIR = Path(__file__).parent.parent.parent / "hls_output"


def segment_video(video_id: str, source: str | Path) -> Path:
    """
    Segments a video into HLS .ts chunks and writes a .m3u8 playlist.
    Returns the output folder path.
    """
    output_dir = HLS_OUTPUT_DIR / video_id
    output_dir.mkdir(parents=True, exist_ok=True)

    playlist = output_dir / "playlist.m3u8"
    segment_pattern = str(output_dir / "segment_%03d.ts")

    (
        ffmpeg
        .input(str(source))
        .output(
            str(playlist),
            format="hls",
            hls_time=CHUNK_DURATION_SECONDS,
            hls_segment_filename=segment_pattern,
            hls_playlist_type="vod",   # writes all segments upfront, no live streaming
            vcodec="copy",             # no re-encode — just remux, fast and lossless
            acodec="copy",
        )
        .overwrite_output()            # safe to re-run; overwrites existing segments
        .run(quiet=True)
    )

    return output_dir


def create_single_segment(video_id: str, url: str, chunk_index: int) -> Path:
    output_dir = HLS_OUTPUT_DIR / video_id
    output_dir.mkdir(parents=True, exist_ok=True)
    segment_path = output_dir / f"segment_{chunk_index:03d}.ts"
    chunk_start = chunk_index * CHUNK_DURATION_SECONDS
    (
        ffmpeg
        .input(url, ss=chunk_start, t=CHUNK_DURATION_SECONDS)
        .output(str(segment_path), format="mpegts", vcodec="copy", acodec="copy")
        .overwrite_output()
        .run(quiet=True)
    )
    return segment_path
