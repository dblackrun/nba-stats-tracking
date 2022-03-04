from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field


class PassingItem(BaseModel):
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
    passes_made: Optional[float] = Field(default=0, alias="PASSES_MADE")
    passes_received: Optional[float] = Field(default=0, alias="PASSES_RECEIVED")
    assists: Optional[float] = Field(default=0, alias="AST")
    ft_assists: Optional[float] = Field(default=0, alias="FT_AST")
    secondary_assists: Optional[float] = Field(default=0, alias="SECONDARY_AST")
    potential_assists: Optional[float] = Field(default=0, alias="POTENTIAL_AST")
    adj_assists: Optional[float] = Field(default=0, alias="AST_ADJ")
    assist_pts: Optional[float] = Field(default=0, alias="AST_POINTS_CREATED")

    @property
    def pts_per_assist(self):
        if self.assists == 0:
            return 0
        return self.assist_pts / self.assists

    @property
    def assists_per_pass(self):
        if self.passes_made == 0:
            return 0
        return self.assists / self.passes_made

    @property
    def potential_assists_per_pass(self):
        if self.passes_made == 0:
            return 0
        return self.potential_assists / self.passes_made

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.passes_made += other.passes_made
        self.passes_received += other.passes_received
        self.assists += other.assists
        self.ft_assists += other.ft_assists
        self.secondary_assists + other.secondary_assists
        self.potential_assists + other.potential_assists
        self.adj_assists + other.adj_assists
        self.assist_pts + other.assist_pts

        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class PassingResults:
    results: List[PassingItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [PassingItem(**dict(zip(headers, row))) for row in rows]
