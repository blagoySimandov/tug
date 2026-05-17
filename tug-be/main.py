import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.events import router as events_router 
from routes.narrate import router as narrate_router
from ai.stt.segmenter import HLS_OUTPUT_DIR
from config import CHUNK_DURATION_SECONDS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")


load_dotenv()

app = FastAPI(
    title="tug-be",
    description="Backend for tug",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router)
app.include_router(narrate_router)

# Serve pre-segmented HLS files so the frontend can play them directly
HLS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/hls", StaticFiles(directory=HLS_OUTPUT_DIR), name="hls")


@app.get("/")
def read_root():
    return {"message": "tug backend is running"}


@app.get("/videos")
def get_videos():
    return [
        {
            "id": 1,
            "label": "Primary",
            "url": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342",
        },
        {
            "id": 2,
            "label": "Secondary",
            "url": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8",
        },
    ]


@app.get("/{video_id}/hls")
def get_hls(video_id: str):
    if not (HLS_OUTPUT_DIR / video_id / "playlist.m3u8").exists():
        raise HTTPException(
            status_code=404,
            detail=f"No HLS segments found for '{video_id}'. Run the segmenter first.",
        )
    return {
        "playlist_url": f"/hls/{video_id}/playlist.m3u8",
        "chunk_duration_seconds": CHUNK_DURATION_SECONDS,
    }


