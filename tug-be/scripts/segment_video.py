"""
CLI: python scripts/segment_video.py <video_id> <source> [--filtered]

<source> can be a local file path or a remote URL.
--filtered  apply commentary removal filter while segmenting

Examples:
    python scripts/segment_video.py arg_fr videos/arg_fr.mp4
    python scripts/segment_video.py arg_fr https://example.com/arg_fr.mp4 --filtered
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.stt.segmenter import segment_video
from ai.stt.voice_filter import segment_and_filter

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/segment_video.py <video_id> <source> [--filtered]")
        sys.exit(1)

    video_id, source = sys.argv[1], sys.argv[2]
    filtered = "--filtered" in sys.argv

    output_dir = segment_and_filter(video_id, source) if filtered else segment_video(video_id, source)
    print(f"Segments written to: {output_dir}")
