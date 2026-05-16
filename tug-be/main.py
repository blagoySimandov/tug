import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from models import ImportantMoment
from routes.events import router as events_router
import bsd_past
import moment_mapper

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


@app.get("/{event_id}/important-moments", response_model=list[ImportantMoment])
async def get_important_moments(
    event_id: int,
    start: float = Query(0),
    end: float = Query(float("inf")),
):
    incidents = await bsd_past.get_incidents(event_id)
    moments = moment_mapper.incidents_to_moments(event_id, incidents)
    return [m for m in moments if start <= m.videoTimestamp <= end]
