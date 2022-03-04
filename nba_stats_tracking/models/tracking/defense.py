from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class DefenseItem(BaseModel):
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
    steals: float = Field(default=0, alias="STL")
    blocks: float = Field(default=0, alias="BLK")
    dreb: float = Field(default=0, alias="DREB")
    def_rim_fga: float = Field(default=0, alias="DEF_RIM_FGA")
    def_rim_fgm: float = Field(default=0, alias="DEF_RIM_FGM")

    @property
    def def_rim_fgpct(self):
        if self.def_rim_fga == 0:
            return 0
        return self.def_rim_fgm / self.def_rim_fga

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.steals += other.steals
        self.blocks += other.blocks
        self.dreb += other.dreb
        self.def_rim_fga += other.def_rim_fga
        self.def_rim_fgm += other.def_rim_fgm
        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class DefenseResults:
    results: List[DefenseItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [DefenseItem(**dict(zip(headers, row))) for row in rows]
