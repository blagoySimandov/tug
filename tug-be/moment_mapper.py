from models import ImportantMoment, MomentType

# (importanceScore, priorityDuration in seconds)
_SCORING: dict[str, tuple[float, float]] = {
    "goal": (0.95, 30),
    "red_card": (0.85, 30),
    "var_decision": (0.70, 20),
    "yellow_card": (0.50, 10),
    "period": (0.40, 4),
    "substitution": (0.20, 10),
    "penalty": (0.85, 60),
    "near_miss": (0.65, 10),
    "free_kick": (0.50, 20),
    "corner": (0.50, 20),
}

# - "goal": goal scored
# - "red_card": player sent off
# - "yellow_card": booking
# - "var_decision": VAR review or decision
# - "substitution": player substitution
# - "penalty": penalty awarded or saved (0.85, 60)
# - "near_miss": close chance, shot on target, great save (0.65, 10)
# - "free_kick": dangerous free kick (0.50, 20)
# - "corner": corner kick leading to danger (0.50, 20)
# - "highlight": any other notable moment worth flagging


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
