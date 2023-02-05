from pydantic import BaseModel, Field


class BoxscoreRequestParameters(BaseModel):
    # Required Fields
    game_id: str = Field(alias="GameID")
    start_period: int = Field(default=0, alias="StartPeriod")
    end_period: int = Field(default=10, alias="EndPeriod")
    range_type: int = Field(default=2, alias="RangeType")
    start_range: int = Field(default=0, alias="StartRange")
    end_range: int = Field(default=55800, alias="EndRange")
    league_id: str = Field(default="00", alias="LeagueID")
