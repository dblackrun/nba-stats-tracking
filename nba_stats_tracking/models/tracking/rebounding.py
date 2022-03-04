from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class ReboundingItem(BaseModel):
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
    oreb: float = Field(default=0, alias="OREB")
    oreb_contest: float = Field(default=0, alias="OREB_CONTEST")
    oreb_uncontest: float = Field(default=0, alias="OREB_UNCONTEST")
    oreb_chances: float = Field(default=0, alias="OREB_CHANCES")
    oreb_chance_defer: float = Field(default=0, alias="OREB_CHANCE_DEFER")
    dreb: float = Field(default=0, alias="DREB")
    dreb_contest: float = Field(default=0, alias="DREB_CONTEST")
    dreb_uncontest: float = Field(default=0, alias="DREB_UNCONTEST")
    dreb_chances: float = Field(default=0, alias="DREB_CHANCES")
    dreb_chance_defer: float = Field(default=0, alias="DREB_CHANCE_DEFER")

    @property
    def contested_oreb_pct(self):
        if self.oreb == 0:
            return 0
        return self.oreb_contest / self.oreb

    @property
    def contested_dreb_pct(self):
        if self.dreb == 0:
            return 0
        return self.dreb_contest / self.dreb

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.oreb += other.oreb
        self.oreb_contest += other.oreb_contest
        self.oreb_uncontest += other.oreb_uncontest
        self.oreb_chances += other.oreb_chances
        self.oreb_chance_defer + other.oreb_chance_defer
        self.dreb + other.dreb
        self.dreb_contest + other.dreb_contest
        self.dreb_uncontest + other.dreb_uncontest
        self.dreb_chances + other.dreb_chances
        self.dreb_chance_defer + other.dreb_chance_defer
        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ReboundingResults:
    results: List[ReboundingItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [ReboundingItem(**dict(zip(headers, row))) for row in rows]
