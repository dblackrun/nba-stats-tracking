from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class SpeedDistanceItem(BaseModel):
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
    dist_feet: Optional[float] = Field(default=0, alias="DIST_FEET")
    dist_miles: Optional[float] = Field(default=0, alias="DIST_MILES")
    dist_miles_off: Optional[float] = Field(default=0, alias="DIST_MILES_OFF")
    dist_miles_def: Optional[float] = Field(default=0, alias="DIST_MILES_DEF")

    avg_speed: Optional[float] = Field(default=0, alias="AVG_SPEED")
    avg_speed_off: Optional[float] = Field(default=0, alias="AVG_SPEED_OFF")
    avg_speed_def: Optional[float] = Field(default=0, alias="AVG_SPEED_DEF")

    # if value from request is None, set it to 0
    @validator("dist_feet")
    def set_dist_feet(cls, v):
        return v or 0

    @validator("dist_miles")
    def set_dist_miles(cls, v):
        return v or 0

    @validator("dist_miles_off")
    def set_dist_miles_off(cls, v):
        return v or 0

    @validator("dist_miles_def")
    def set_dist_miles_def(cls, v):
        return v or 0

    def __add__(self, other):
        self.games_played += other.games_played
        self.wins += other.wins
        self.losses += other.losses
        self.minutes += other.minutes
        self.dist_feet += other.dist_feet
        self.dist_miles += other.dist_miles
        self.dist_miles_off += other.dist_miles_off
        self.dist_miles_def += other.dist_miles_def
        # when summed, these values are meaningless, set to 0
        self.avg_speed = 0
        self.avg_speed_off = 0
        self.avg_speed_def = 0

        return self

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class SpeedDistanceResults:
    results: List[SpeedDistanceItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [SpeedDistanceItem(**dict(zip(headers, row))) for row in rows]
