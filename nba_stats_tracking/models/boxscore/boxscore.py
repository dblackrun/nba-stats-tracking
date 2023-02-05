from typing import List, Optional

from pydantic import BaseModel, Field


class BoxScorePlayer(BaseModel):
    player_id: Optional[int] = Field(alias="personId")
    first_name: Optional[str] = Field(alias="firstName")
    family_name: Optional[str] = Field(alias="familyName")
    name_initial: Optional[str] = Field(alias="nameI")
    player_slug: Optional[str] = Field(alias="playerSlug")
    position: Optional[str] = Field(alias="position")
    comment: Optional[str] = Field(alias="comment")
    jersey_num: Optional[str] = Field(alias="jerseyNum")


class BoxscoreTeam(BaseModel):
    team_id: Optional[int] = Field(alias="teamId")
    team_city: Optional[str] = Field(alias="teamCity")
    team_name: Optional[str] = Field(alias="teamName")
    team_tricode: Optional[str] = Field(alias="teamTricode")
    team_slug: Optional[str] = Field(alias="teamSlug")
    players: List[BoxScorePlayer] = Field(alias="players")


class BoxscoreResults(BaseModel):
    game_id: str = Field(alias="gameId")
    away_team_id: int = Field(alias="awayTeamId")
    home_team_id: int = Field(alias="homeTeamId")
    home_team: BoxscoreTeam = Field(alias="homeTeam")
    away_team: BoxscoreTeam = Field(alias="awayTeam")
