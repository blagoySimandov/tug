import asyncio
import sys
from ai.stt.stt_client import STTClient


async def main(url: str):
    client = STTClient()
    segments = await client.transcribe_video_url(url)
    for seg in segments:
        print(f"[{seg.start:.2f} -> {seg.end:.2f}] {seg.text}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stt_test.py <video_url>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
