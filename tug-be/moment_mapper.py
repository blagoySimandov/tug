from models import ImportantMoment, MomentType

# (importanceScore, priorityDuration in seconds)
_SCORING: dict[str, tuple[float, float]] = {
    "goal": (0.95, 10),
    "red_card": (0.85, 8),
    "var_decision": (0.70, 6),
    "yellow_card": (0.55, 5),
    "period": (0.40, 4),
    "substitution": (0.20, 3),
}


def _classify(incident: dict) -> MomentType | None:
    t = incident.get("type")
    if t == "goal":
        return "goal"
    if t == "card":
        card_type = incident.get("card_type", "")
        if card_type in ("red", "yellowRed"):
            return "red_card"
        return "yellow_card"
    if t == "varDecision":
        return "var_decision"
    return None


def incidents_to_moments(
    event_id: int, incidents: list[dict], kickoff_offset: float = 0
) -> list[ImportantMoment]:
    moments = []
    for inc in incidents:
        minute = inc.get("minute", 0) or 0
        if minute < 0:
            continue
        kind = _classify(inc)
        if kind is None:
            continue
        score, duration = _SCORING[kind]
        added = inc.get("added_time") or 0
        video_ts = kickoff_offset + (minute + added) * 60
        moments.append(
            ImportantMoment(
                type=kind,
                videoId=str(event_id),
                videoTimestamp=video_ts,
                importanceScore=score,
                priorityDuration=duration,
            )
        )
    return moments
