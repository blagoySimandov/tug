from io import BytesIO
from pathlib import Path

import av
import ffmpeg

from ai.stt.segmenter import HLS_OUTPUT_DIR
from config import CHUNK_DURATION_SECONDS


def remove_commentary(input: BytesIO) -> BytesIO:
    """
    Attenuates center-panned commentary using a side-channel pan trick,
    then applies a low-pass to suppress the voice frequency range.
    Works best on stereo broadcasts where commentary is center-panned.
    """
    output_buffer = BytesIO()
    with av.open(input) as in_container:
        audio = in_container.streams.audio[0]
        graph = av.filter.Graph()  # type: ignore

        abuffer = graph.add_abuffer(template=audio)
        # Subtract right from left (and vice versa) to cancel center-panned audio
        pan = graph.add("pan", "stereo|c0=c0-c1|c1=c1-c0")
        # Cut voice frequency range (1kHz–4kHz)
        equalizer = graph.add("equalizer", "f=2500:width_type=o:width=3:g=-12")
        # Boost volume to compensate for the level drop from pan subtraction
        volume = graph.add("volume", "volume=6dB")
        abuffersink = graph.add("abuffersink")

        abuffer.link_to(pan)
        pan.link_to(equalizer)
        equalizer.link_to(volume)
        volume.link_to(abuffersink)
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


def segment_and_filter(video_id: str, source: str | Path) -> Path:
    """
    Segments a video into HLS .ts chunks with commentary removed.
    Applies the same pan subtraction + EQ + volume boost as remove_commentary(),
    but in a single ffmpeg pass alongside the segmentation.
    Returns the output folder path.
    """
    # Filtered segments go to a separate folder so unfiltered segments
    # (used by Whisper) are not overwritten
    output_dir = HLS_OUTPUT_DIR / f"{video_id}_filtered"
    output_dir.mkdir(parents=True, exist_ok=True)

    playlist = output_dir / "playlist.m3u8"
    segment_pattern = str(output_dir / "segment_%03d.ts")

    # Pass the full audio filter chain as a single -af string to avoid
    # ffmpeg-python escaping the = signs inside the pan filter expression
    audio_filters = (
        "pan=stereo|c0=c0-c1|c1=c1-c0,"        # cancel center-panned commentary
        "equalizer=f=2500:width_type=o:width=3:g=-12,"  # cut residual voice freq
        "volume=6dB"                             # restore level lost from pan subtraction
    )

    (
        ffmpeg
        .input(str(source))
        .output(
            str(playlist),
            format="hls",
            hls_time=CHUNK_DURATION_SECONDS,
            hls_segment_filename=segment_pattern,
            hls_playlist_type="vod",  # write all segments upfront, no live streaming
            vcodec="copy",            # no re-encode on video
            acodec="aac",             # re-encode audio to apply the filter
            af=audio_filters,
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return output_dir
