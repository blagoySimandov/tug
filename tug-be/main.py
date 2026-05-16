from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import ImportantMoment, BatchMomentsRequest
from mock import MOCK_MOMENTS
from ai.stt.stt_gem_wrap import transcribe_and_analyze

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


def get_moments_for_video(
    video_id: str, start: float, end: float
) -> list[ImportantMoment]:
    moments = MOCK_MOMENTS.get(video_id, [])
    return [m for m in moments if start <= m.videoTimestamp <= end]


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


VIDEO_URLS: dict[str, str] = {
    "arg_fr": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342",
    "cr_bra": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8",
}


@app.get("/{video_id}/important-moments", response_model=list[ImportantMoment])
async def get_important_moments(
    video_id: str,
    start: float = Query(0),
    end: float = Query(float("inf")),
):
    if video_id not in VIDEO_URLS:
        raise HTTPException(status_code=404, detail=f"Video '{video_id}' not found")
    all_moments = await transcribe_and_analyze(video_id, VIDEO_URLS[video_id])
    return [m for m in all_moments if start <= m.videoTimestamp <= end]


@app.post("/important-moments/batch", response_model=dict[str, list[ImportantMoment]])
def get_important_moments_batch(body: BatchMomentsRequest):
    result: dict[str, list[ImportantMoment]] = {}
    for q in body.queries:
        result[q.videoId] = get_moments_for_video(q.videoId, q.start, q.end)
    return result
