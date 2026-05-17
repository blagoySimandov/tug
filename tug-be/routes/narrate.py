from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

from ai.narrator import NarratorStyle, generate_narration, generate_narration_audio

router = APIRouter()


class NarrateRequest(BaseModel):
    url: str
    style: NarratorStyle = NarratorStyle()
    window_start: float = 0
    window_end: float = 300


class NarrateResponse(BaseModel):
    narration: str


@router.post("/narrate/{event_id}", response_model=NarrateResponse)
async def narrate(event_id: int, body: NarrateRequest):
    narration = await generate_narration(
        event_id=event_id,
        url=body.url,
        style=body.style,
        window_start=body.window_start,
        window_end=body.window_end,
    )
    return NarrateResponse(narration=narration)


@router.post("/narrate/{event_id}/audio")
async def narrate_audio(event_id: int, body: NarrateRequest):
    audio = await generate_narration_audio(
        event_id=event_id,
        url=body.url,
        style=body.style,
        window_start=body.window_start,
        window_end=body.window_end,
    )
    return Response(content=audio, media_type="audio/mpeg")
