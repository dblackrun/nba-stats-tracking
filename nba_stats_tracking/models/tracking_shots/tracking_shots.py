from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class TrackingShotItem(BaseModel):
    # Only for player stats
    player_id: Optional[int] = Field(alias="PLAYER_ID")
    player_name: Optional[str] = Field(alias="PLAYER_NAME")
    player_last_team_id: Optional[int] = Field(alias="PLAYER_LAST_TEAM_ID")
    player_last_team_abbreviation: Optional[str] = Field(
        alias="PLAYER_LAST_TEAM_ABBREVIATION"
    )
    age: Optional[int] = Field(alias="AGE")

    # Only for team stats
    team_name: Optional[str] = Field(alias="TEAM_NAME")
    team_id: Optional[int] = Field(alias="TEAM_ID")
    team_abbreviation: Optional[str] = Field(alias="TEAM_ABBREVIATION")

    # Only for season stats
    season: Optional[str] = Field(alias="SEASON")

    # Only for game logs
    game_id: Optional[str] = Field(alias="GAME_ID")
    opponent_team_id: Optional[int] = Field(alias="OPPONENT_TEAM_ID")

    games_played: Optional[int] = Field(default=0, alias="GP")
    fgm: Optional[int] = Field(default=0, alias="FGM")
    fga: Optional[int] = Field(default=0, alias="FGA")
    fg2m: Optional[int] = Field(default=0, alias="FG2M")
    fg2a: Optional[int] = Field(default=0, alias="FG2A")
    fg3m: Optional[int] = Field(default=0, alias="FG3M")
    fg3a: Optional[int] = Field(default=0, alias="FG3A")

    # For computing frequencies. Not in response.

    overall_fga: Optional[int] = Field(default=0)
    overall_fg2a: Optional[int] = Field(default=0)
    overall_fg3a: Optional[int] = Field(default=0)

    # if value from request is None, set it to 0
    @validator("games_played")
    def set_games_played(cls, v):
        return v or 0

    @validator("fgm")
    def set_fgm(cls, v):
        return v or 0

    @validator("fga")
    def set_fga(cls, v):
        return v or 0

    @validator("fg2m")
    def set_fg2m(cls, v):
        return v or 0

    @validator("fg2a")
    def set_fg2a(cls, v):
        return v or 0

    @validator("fg3m")
    def set_fg3m(cls, v):
        return v or 0

    @validator("fg3a")
    def set_fg3a(cls, v):
        return v or 0

    @property
    def fg2pct(self):
        if self.fg2a == 0:
            return 0
        return self.fg2m / self.fg2a

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

    @property
    def fga_frequency(self):
        if self.overall_fga == 0:
            return 0
        return self.fga / self.overall_fga

    @property
    def fg2a_frequency(self):
        if self.overall_fga == 0:
            return 0
        return self.fg2a / self.overall_fga

    @property
    def fg3a_frequency(self):
        if self.overall_fga == 0:
            return 0
        return self.fg3a / self.overall_fga

    @property
    def frequency_of_fg2a(self):
        if self.overall_fg2a == 0:
            return 0
        return self.fg2a / self.overall_fg2a

    @property
    def frequency_of_fg3a(self):
        if self.overall_fg3a == 0:
            return 0
        return self.fg3a / self.overall_fg3a

    def __add__(self, other):
        self.games_played += other.games_played
        self.fgm += other.fgm
        self.fga += other.fga
        self.fg2m += other.fg2m
        self.fg2a += other.fg2a
        self.fg3m += other.fg3m
        self.fg3a += other.fg3a
        self.overall_fga += other.overall_fga
        self.overall_fg2a += other.overall_fg2a
        self.overall_fg3a += other.overall_fg3a

        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class TrackingShotResults:
    results: List[TrackingShotItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [TrackingShotItem(**dict(zip(headers, row))) for row in rows]
