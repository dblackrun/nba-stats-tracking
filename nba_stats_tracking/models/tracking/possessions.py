from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class PossessionsItem(BaseModel):
    # Only for player stats
    player_id: Optional[int] = Field(alias="PLAYER_ID")
    player_name: Optional[str] = Field(alias="PLAYER_NAME")

    # Only for team stats
    team_name: Optional[str] = Field(alias="TEAM_NAME")

    # Only for season stats
    season: Optional[str] = Field(alias="SEASON")

    # Only for game logs
    game_id: Optional[str] = Field(alias="GAME_ID")
    opponent_team_id: Optional[int] = Field(alias="OPPONENT_TEAM_ID")

    team_id: int = Field(alias="TEAM_ID")
    team_abbreviation: str = Field(alias="TEAM_ABBREVIATION")
    games_played: int = Field(default=0, alias="GP")
    wins: int = Field(default=0, alias="W")
    losses: int = Field(default=0, alias="L")
    minutes: float = Field(default=0, alias="MIN")
    points: float = Field(default=0, alias="POINTS")
    touches: float = Field(default=0, alias="TOUCHES")
    front_court_touches: float = Field(default=0, alias="FRONT_CT_TOUCHES")
    time_of_poss: float = Field(default=0, alias="TIME_OF_POSS")
    elbow_touches: float = Field(default=0, alias="ELBOW_TOUCHES")
    post_touches: float = Field(default=0, alias="POST_TOUCHES")
    paint_touches: float = Field(default=0, alias="PAINT_TOUCHES")

    seconds_per_touch: float = Field(default=0, alias="AVG_SEC_PER_TOUCH")
    dribbles_per_touch: float = Field(default=0, alias="AVG_DRIB_PER_TOUCH")

    @property
    def pts_per_touch(self):
        if self.touches == 0:
            return 0
        return self.points / self.touches

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.points += other.points
        self.touches += other.touches
        self.front_court_touches += other.front_court_touches
        self.time_of_poss += other.time_of_poss
        self.elbow_touches + other.elbow_touches
        self.post_touches + other.post_touches
        self.post_touches + other.post_touches
        self.paint_touches + other.paint_touches

        # when summed, these values are meaningless, set to 0
        self.seconds_per_touch = 0
        self.dribbles_per_touch = 0

        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class PossessionsResults:
    results: List[PossessionsItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [PossessionsItem(**dict(zip(headers, row))) for row in rows]
