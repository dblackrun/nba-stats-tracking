from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PullUpItem(BaseModel):
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
    fgm: Optional[float] = Field(default=0, alias="PULL_UP_FGM")
    fga: Optional[float] = Field(default=0, alias="PULL_UP_FGA")
    points: Optional[float] = Field(default=0, alias="PULL_UP_PTS")
    fg3m: Optional[float] = Field(default=0, alias="PULL_UP_FG3M")
    fg3a: Optional[float] = Field(default=0, alias="PULL_UP_FG3A")
    fg3pct: float = Field(default=0, alias="PULL_UP_FG3_PCT")
    efg: float = Field(default=0, alias="PULL_UP_EFG_PCT")

    # if value from request is None, set it to 0
    @validator("fgm")
    def set_fgm(cls, v):
        return v or 0

    @validator("fga")
    def set_fga(cls, v):
        return v or 0

    @validator("points")
    def set_points(cls, v):
        return v or 0

    @validator("fg3m")
    def set_fg3m(cls, v):
        return v or 0

    @validator("fg3a")
    def set_fg3a(cls, v):
        return v or 0

    @property
    def fg3pct(self):
        if self.fg3a == 0:
            return 0
        return self.fg3m / self.fg3a

    @property
    def efg(self):
        if self.fga == 0:
            return 0
        return (self.fgm + 0.5 * self.fg3m) / self.fga

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.fgm += other.fgm
        self.fga += other.fga
        self.points += other.points
        self.fg3m += other.fg3m
        self.fg3a += other.fg3a

        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class PullUpResults:
    results: List[PullUpItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [PullUpItem(**dict(zip(headers, row))) for row in rows]
