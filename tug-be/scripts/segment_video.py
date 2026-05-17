"""
CLI: python scripts/segment_video.py <video_id> <source>

<source> can be a local file path or a remote URL.

Example:
    python scripts/segment_video.py arg_fr videos/arg_fr.mp4
    python scripts/segment_video.py arg_fr https://example.com/arg_fr.mp4
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.stt.segmenter import segment_video

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/segment_video.py <video_id> <source>")
        sys.exit(1)

    video_id, source = sys.argv[1], sys.argv[2]
    output_dir = segment_video(video_id, source)
    print(f"Segments written to: {output_dir}")
