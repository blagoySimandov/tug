from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import ImportantMoment, BatchQuery, BatchMomentsRequest

app = FastAPI()


MOCK_MOMENTS: dict[str, list[ImportantMoment]] = {
    "cr_bra": [
        ImportantMoment(type="goal",     videoId="cr_bra", videoTimestamp=15,  importanceScore=0.85, priorityDuration=8),
        ImportantMoment(type="red_card", videoId="cr_bra", videoTimestamp=45,  importanceScore=0.70, priorityDuration=6),
        ImportantMoment(type="goal",     videoId="cr_bra", videoTimestamp=90,  importanceScore=0.92, priorityDuration=10),
    ],
    "arg_fr": [
        ImportantMoment(type="goal",     videoId="arg_fr", videoTimestamp=10,  importanceScore=0.90, priorityDuration=8),
        ImportantMoment(type="red_card", videoId="arg_fr", videoTimestamp=30,  importanceScore=0.75, priorityDuration=6),
        ImportantMoment(type="goal",     videoId="arg_fr", videoTimestamp=60,  importanceScore=0.95, priorityDuration=10),
    ],
}


def get_moments_for_video(video_id: str, start: float, end: float) -> list[ImportantMoment]:
    moments = MOCK_MOMENTS.get(video_id, [])
    return [m for m in moments if start <= m.videoTimestamp <= end]


@app.get("/")
def read_root():
    return {"message": "tug backend is running"}


@app.get("/videos")
def get_videos():
    return [
        {"id": 1, "label": "Primary", "url": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342"},
        {"id": 2, "label": "Secondary", "url": "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8"},
    ]


@app.get("/{video_id}/important-moments", response_model=list[ImportantMoment])
def get_important_moments(
    video_id: str,
    start: float = Query(0),
    end: float = Query(float("inf")),
):
    if video_id not in MOCK_MOMENTS:
        raise HTTPException(status_code=404, detail=f"Video '{video_id}' not found")
    return get_moments_for_video(video_id, start, end)



@app.post("/important-moments/batch", response_model=dict[str, list[ImportantMoment]])
def get_important_moments_batch(body: BatchMomentsRequest):
    result: dict[str, list[ImportantMoment]] = {}
    for q in body.queries:
        result[q.videoId] = get_moments_for_video(q.videoId, q.start, q.end)
    return result
