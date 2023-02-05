from datetime import date
from typing import List

from pydantic import BaseModel, Field


class TeamItem(BaseModel):
    team_id: int = Field(alias="teamId")


class GameItem(BaseModel):
    game_id: str = Field(alias="gameId")
    game_stats_id: int = Field(alias="gameStatus")
    home_team: TeamItem = Field(alias="homeTeam")
    visitor_team: TeamItem = Field(alias="awayTeam")

    def __getitem__(self, item):
        return getattr(self, item)


class ScoreboardResults(BaseModel):
    game_date: date = Field(alias="gameDate")
    games: List[GameItem] = Field(alias="games")
