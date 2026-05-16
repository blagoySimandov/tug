from typing import Literal
from pydantic import BaseModel

MomentType = Literal["goal", "red_card"]


class ImportantMoment(BaseModel):
    type: MomentType
    videoId: str
    videoTimestamp: float
    importanceScore: float
    priorityDuration: float


class BatchQuery(BaseModel):
    videoId: str
    start: float = 0
    end: float = float("inf")


class BatchMomentsRequest(BaseModel):
    queries: list[BatchQuery]
