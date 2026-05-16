from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from models import ImportantMoment
from routes.events import router as events_router, get_kickoff_offset
import bsd_past
import moment_mapper

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


@app.get("/")
def read_root():
    return {"message": "tug backend is running"}


@app.get("/{event_id}/important-moments", response_model=list[ImportantMoment])
async def get_important_moments(
    event_id: int,
    start: float = Query(0),
    end: float = Query(float("inf")),
):
    incidents = await bsd_past.get_incidents(event_id)
    kickoff_offset = get_kickoff_offset(event_id)
    moments = moment_mapper.incidents_to_moments(event_id, incidents, kickoff_offset)
    return [m for m in moments if start <= m.videoTimestamp <= end]
