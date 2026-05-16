import asyncio
from dotenv import load_dotenv
from transcription import transcribe_video_url

load_dotenv()

VIDEOS = [
    {"id": 1, "label": "arg_fr", "url": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342"},
    {"id": 2, "label": "cr_bra", "url": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8"},
]


async def main():
    for video in VIDEOS:
        print(f"\nTranscribing {video['label']}...")
        transcript = await transcribe_video_url(video["url"])
        print(f"\n--- Transcript: {video['label']} ---")
        print(transcript.encode("utf-8", errors="replace").decode("utf-8"))


if __name__ == "__main__":
    asyncio.run(main())
