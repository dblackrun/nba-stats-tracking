from datetime import date

from pydantic import BaseModel, Field

from nba_stats_tracking.models.request import LeagueID


class ScoreboardRequestParameters(BaseModel):
    # Required Fields
    game_date: date = Field(alias="GameDate")
    league_id: LeagueID = Field(default=LeagueID.nba, alias="LeagueID")
