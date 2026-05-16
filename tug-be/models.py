from typing import Literal
from pydantic import BaseModel, ConfigDict

MomentType = Literal["goal", "red_card", "yellow_card", "var_decision"]

_extra = ConfigDict(extra="allow")


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


class BsdEvent(BaseModel):
    model_config = _extra
    id: int
    league_id: int
    league_name: str | None = None
    home_team: str
    away_team: str
    event_date: str
    status: str
    home_score: int | None = None
    away_score: int | None = None


class EventsListResponse(BaseModel):
    count: int
    next: str | None = None
    previous: str | None = None
    results: list[BsdEvent]


class Incident(BaseModel):
    model_config = _extra
    incidentType: str
    time: int
    addedTime: int | None = None
    isHome: bool | None = None


class StatItem(BaseModel):
    model_config = _extra
    name: str
    home: str | None = None
    away: str | None = None


class StatGroup(BaseModel):
    model_config = _extra
    groupName: str | None = None
    statisticsItems: list[StatItem] | None = None


class StatPeriod(BaseModel):
    model_config = _extra
    period: str | None = None
    groups: list[StatGroup] | None = None


class EventStats(BaseModel):
    model_config = _extra
    statistics: list[StatPeriod] | None = None


class EventMetadata(BaseModel):
    model_config = _extra


class LineupPlayer(BaseModel):
    model_config = _extra
    shirtNumber: int | None = None
    position: str | None = None
    substitute: bool | None = None


class TeamLineup(BaseModel):
    model_config = _extra
    players: list[LineupPlayer] | None = None
    formation: str | None = None


class EventLineups(BaseModel):
    model_config = _extra
    home: TeamLineup | None = None
    away: TeamLineup | None = None


class PlayerStat(BaseModel):
    model_config = _extra


class MatchSnapshot(BaseModel):
    event_id: int
    event: BsdEvent | None = None
    metadata: EventMetadata | None = None
    stats: EventStats | None = None
    incidents: list[Incident] | None = None
    lineups: EventLineups | None = None
    player_stats: list[PlayerStat] | None = None
