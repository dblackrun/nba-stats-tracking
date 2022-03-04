from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class EfficiencyItem(BaseModel):
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
    drive_pts: float = Field(default=0, alias="DRIVE_PTS")
    catch_shoot_pts: float = Field(default=0, alias="CATCH_SHOOT_PTS")
    pull_up_pts: float = Field(default=0, alias="PULL_UP_PTS")
    paint_touch_pts: float = Field(default=0, alias="PAINT_TOUCH_PTS")
    post_touch_pts: float = Field(default=0, alias="POST_TOUCH_PTS")
    elbow_touch_pts: float = Field(default=0, alias="ELBOW_TOUCH_PTS")

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.points += other.points
        self.drive_pts += other.drive_pts
        self.catch_shoot_pts += other.catch_shoot_pts
        self.pull_up_pts += other.pull_up_pts
        self.paint_touch_pts += other.paint_touch_pts
        self.post_touch_pts += other.post_touch_pts
        self.elbow_touch_pts += other.elbow_touch_pts
        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class EfficiencyResults:
    results: List[EfficiencyItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [EfficiencyItem(**dict(zip(headers, row))) for row in rows]
