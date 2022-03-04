from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from nba_stats_tracking.models.request import PerMode, SeasonType


class TrackingMeasureType(str, Enum):
    catch_and_shoot = "CatchShoot"
    defense = "Defense"
    drives = "Drives"
    passing = "Passing"
    pull_up = "PullUpShot"
    rebounding = "Rebounding"
    shooting = "Efficiency"
    speed_distance = "SpeedDistance"
    elbow_touches = "ElbowTouch"
    paint_touches = "PaintTouch"
    post_touches = "PostTouch"
    possessions = "Possessions"


class PlayerOrTeam(str, Enum):
    player = "Player"
    team = "Team"


class TrackingRequestParameters(BaseModel):
    # Required Fields
    measure_type: TrackingMeasureType = Field(alias="PtMeasureType")
    per_mode: PerMode = Field(default=PerMode.totals, alias="PerMode")
    player_or_team: PlayerOrTeam = Field(alias="PlayerOrTeam")
    league_id: str = Field(default="00", alias="LeagueID")
    season: str = Field(alias="Season")
    season_type: SeasonType = Field(alias="SeasonType")

    # Optional Fields that need to be in the request
    # These will use the default value in the request if unset
    outcome: Optional[str] = Field(default="", alias="Outcome")
    location: Optional[str] = Field(default="", alias="Location")
    month: Optional[int] = Field(default=0, alias="Month")
    season_segment: Optional[str] = Field(default="", alias="SeasonSegment")
    date_from: Optional[str] = Field(default="", alias="DateFrom")  # MM/DD/YYYY
    date_to: Optional[str] = Field(default="", alias="DateTo")  # MM/DD/YYYY
    opponent_team_id: Optional[int] = Field(default=0, alias="OpponentTeamID")
    vs_conference: Optional[str] = Field(default="", alias="VsConference")
    vs_division: Optional[str] = Field(default="", alias="VsDivision")
    last_n_games: Optional[int] = Field(default=0, alias="LastNGames")
    game_scope: Optional[str] = Field(default="", alias="GameScope")
    player_experience: Optional[str] = Field(default="", alias="PlayerExperience")
    player_position: Optional[str] = Field(default="", alias="PlayerPosition")
    starter_bench: Optional[str] = Field(default="", alias="StarterBench")

    # Optional Fields
    playoff_round: Optional[str] = Field(alias="PORound")
    team_id: Optional[str] = Field(alias="TeamID")
    conference: Optional[str] = Field(alias="Conference")
    division: Optional[str] = Field(alias="Division")
    draft_year: Optional[str] = Field(alias="DraftYear")
    draft_pick: Optional[str] = Field(alias="DraftPick")
    college: Optional[str] = Field(alias="College")
    country: Optional[str] = Field(alias="Country")
    height: Optional[str] = Field(alias="Height")
    weight: Optional[str] = Field(alias="Weight")
