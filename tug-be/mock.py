from models import ImportantMoment

MOCK_MOMENTS: dict[str, list[ImportantMoment]] = {
    "cr_bra": [
        ImportantMoment(
            type="goal",
            videoId="cr_bra",
            videoTimestamp=15,
            importanceScore=0.85,
            priorityDuration=8,
        ),
        ImportantMoment(
            type="red_card",
            videoId="cr_bra",
            videoTimestamp=45,
            importanceScore=0.70,
            priorityDuration=6,
        ),
        ImportantMoment(
            type="goal",
            videoId="cr_bra",
            videoTimestamp=90,
            importanceScore=0.92,
            priorityDuration=10,
        ),
    ],
    "arg_fr": [
        ImportantMoment(
            type="goal",
            videoId="arg_fr",
            videoTimestamp=10,
            importanceScore=0.90,
            priorityDuration=8,
        ),
        ImportantMoment(
            type="red_card",
            videoId="arg_fr",
            videoTimestamp=30,
            importanceScore=0.75,
            priorityDuration=6,
        ),
        ImportantMoment(
            type="goal",
            videoId="arg_fr",
            videoTimestamp=60,
            importanceScore=0.95,
            priorityDuration=10,
        ),
    ],
}
