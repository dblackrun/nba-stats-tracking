from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class PaintTouchesItem(BaseModel):
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
    touches: float = Field(default=0, alias="TOUCHES")
    paint_touches: float = Field(default=0, alias="PAINT_TOUCHES")
    fgm: float = Field(default=0, alias="PAINT_TOUCH_FGM")
    fga: float = Field(default=0, alias="PAINT_TOUCH_FGA")
    ftm: float = Field(default=0, alias="PAINT_TOUCH_FTM")
    fta: float = Field(default=0, alias="PAINT_TOUCH_FTA")
    points: float = Field(default=0, alias="PAINT_TOUCH_PTS")
    passes: float = Field(default=0, alias="PAINT_TOUCH_PASSES")
    assists: float = Field(default=0, alias="PAINT_TOUCH_AST")
    turnovers: float = Field(default=0, alias="PAINT_TOUCH_TOV")
    fouls: float = Field(default=0, alias="PAINT_TOUCH_FOULS")

    @property
    def pass_pct(self):
        if self.paint_touches == 0:
            return 0
        return self.passes / self.paint_touches

    @property
    def assist_pct(self):
        if self.paint_touches == 0:
            return 0
        return self.assists / self.paint_touches

    @property
    def turnover_pct(self):
        if self.paint_touches == 0:
            return 0
        return self.turnovers / self.paint_touches

    @property
    def foul_pct(self):
        if self.paint_touches == 0:
            return 0
        return self.fouls / self.paint_touches

    @property
    def pts_per_paint_touch(self):
        if self.paint_touches == 0:
            return 0
        return self.points / self.paint_touches

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.touches += other.touches
        self.paint_touches += other.paint_touches
        self.fgm += other.fgm
        self.fga += other.fga
        self.ftm + other.ftm
        self.points + other.points
        self.passes + other.passes
        self.assists + other.assists
        self.turnovers + other.turnovers
        self.fouls + other.fouls
        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class PaintTouchesResults:
    results: List[PaintTouchesItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [PaintTouchesItem(**dict(zip(headers, row))) for row in rows]
