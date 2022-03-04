from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class BoxscoreItem(BaseModel):
    game_id: str = Field(alias="GAME_ID")
    team_id: int = Field(alias="TEAM_ID")
    team_abbreviation: str = Field(alias="TEAM_ABBREVIATION")
    team_city: str = Field(alias="TEAM_CITY")
    player_id: int = Field(alias="PLAYER_ID")
    player_name: str = Field(alias="PLAYER_NAME")
    start_position: str = Field(alias="START_POSITION")
    comment: str = Field(alias="COMMENT")
    minutes: Optional[str] = Field(alias="MIN")
    fgm: Optional[int] = Field(alias="FGM")
    fga: Optional[int] = Field(alias="FGA")
    fg_pct: Optional[float] = Field(alias="FG_PCT")
    fg3m: Optional[int] = Field(alias="FG3M")
    fg3a: Optional[int] = Field(alias="FG3A")
    fg3_pct: Optional[int] = Field(alias="FG3_PCT")
    ftm: Optional[int] = Field(alias="FTM")
    fta: Optional[int] = Field(alias="FTA")
    ft_pct: Optional[float] = Field(alias="FT_PCT")
    oreb: Optional[int] = Field(alias="OREB")
    dreb: Optional[int] = Field(alias="DREB")
    reb: Optional[int] = Field(alias="REB")
    stl: Optional[int] = Field(alias="STL")
    blk: Optional[int] = Field(alias="BLK")
    turnovers: Optional[int] = Field(alias="TO")
    fouls: Optional[int] = Field(alias="PF")
    points: Optional[int] = Field(alias="PTS")
    plus_minutes: Optional[float] = Field(alias="PLUS_MINUS")

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class BoxscoreResults:
    results: List[BoxscoreItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [BoxscoreItem(**dict(zip(headers, row))) for row in rows]

    def __iter__(self):
        return iter(self.results)
