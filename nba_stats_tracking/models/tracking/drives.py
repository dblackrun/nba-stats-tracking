from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class DrivesItem(BaseModel):
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
    drives: float = Field(default=0, alias="DRIVES")
    fgm: float = Field(default=0, alias="DRIVE_FGM")
    fga: float = Field(default=0, alias="DRIVE_FGA")
    ftm: float = Field(default=0, alias="DRIVE_FTM")
    fta: float = Field(default=0, alias="DRIVE_FTA")
    points: float = Field(default=0, alias="DRIVE_PTS")
    passes: float = Field(default=0, alias="DRIVE_PASSES")
    assists: float = Field(default=0, alias="DRIVE_AST")
    turnovers: float = Field(default=0, alias="DRIVE_TOV")
    fouls: float = Field(default=0, alias="DRIVE_PF")

    @property
    def pass_pct(self):
        if self.drives == 0:
            return 0
        return self.passes / self.drives

    @property
    def assist_pct(self):
        if self.drives == 0:
            return 0
        return self.assists / self.drives

    @property
    def turnover_pct(self):
        if self.drives == 0:
            return 0
        return self.turnovers / self.drives

    @property
    def foul_pct(self):
        if self.drives == 0:
            return 0
        return self.fouls / self.drives

    @property
    def pts_per_drive(self):
        if self.drives == 0:
            return 0
        return self.points / self.drives

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.drives += other.drives
        self.fgm += other.fgm
        self.fga += other.fga
        self.ftm += other.ftm
        self.fta += other.fta
        self.points += other.points
        self.passes += other.passes
        self.assists += other.assists
        self.turnovers += other.turnovers
        self.fouls += other.fouls
        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class DrivesResults:
    results: List[DrivesItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [DrivesItem(**dict(zip(headers, row))) for row in rows]
