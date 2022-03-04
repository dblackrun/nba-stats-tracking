from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from nba_stats_tracking.models.request import LeagueID, PerMode, SeasonType


class Location(str, Enum):
    any = ""
    home = "Home"
    road = "Road"


class CloseDefDist(str, Enum):
    all = ""
    range_0_2_ft = "0-2 Feet - Very Tight"
    range_2_4_ft = "2-4 Feet - Tight"
    range_4_6_ft = "4-6 Feet - Open"
    range_6_plus_ft = "6+ Feet - Wide Open"


class ShotClock(str, Enum):
    all = ""
    range_24_22 = "24-22"
    range_22_18 = "22-18 Very Early"
    range_18_15 = "18-15 Early"
    range_17_7 = "15-7 Average"
    range_7_4 = "7-4 Late"
    range_4_0 = "4-0 Very Late"
    off = "ShotClock Off"  # I think this is no longer used


class ShotDist(str, Enum):
    all = ""
    ten_or_more_ft = ">=10.0"


class TouchTime(str, Enum):
    all = ""
    under_2_seconds = "Touch < 2 Seconds"
    two_to_six_seconds = "Touch 2-6 Seconds"
    six_plus_seconds = "Touch 6+ Seconds"


class Dribbles(str, Enum):
    all = ""
    zero = "0 Dribbles"
    one = "1 Dribble"
    two = "2 Dribbles"
    three_to_six = "3-6 Dribbles"
    seven_plus = "7+ Dribbles"


class GeneralRange(str, Enum):
    overall = "Overall"
    catch_and_shoot = "Catch and Shoot"
    pullups = "Pullups"
    under_10_ft = "Less Than 10 ft"


class TrackingRequestParameters(BaseModel):
    # Required Fields
    season: str = Field(alias="Season")
    season_type: SeasonType = Field(alias="SeasonType")
    per_mode: PerMode = Field(default=PerMode.totals, alias="PerMode")
    league_id: LeagueID = Field(LeagueID.nba, alias="LeagueID")
    close_def_dist: CloseDefDist = Field(CloseDefDist.all, alias="CloseDefDistRange")
    shot_clock: ShotClock = Field(ShotClock.all, alias="ShotClockRange")
    shot_dist: ShotDist = Field(ShotDist.all, alias="ShotDistRange")
    touch_time: TouchTime = Field(TouchTime.all, alias="TouchTimeRange")
    dribble_range: Dribbles = Field(Dribbles.all, alias="DribbleRange")
    general_range: GeneralRange = Field(GeneralRange.overall, alias="GeneralRange")
    date_from: Optional[str] = Field(default="", alias="DateFrom")  # MM/DD/YYYY
    date_to: Optional[str] = Field(default="", alias="DateTo")  # MM/DD/YYYY
    period: Optional[str] = Field(default="", alias="Period")
    location: Optional[Location] = Field(Location.any, alias="Location")
