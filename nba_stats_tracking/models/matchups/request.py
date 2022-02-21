from pydantic import BaseModel, Field


class MatchupsRequestParameters(BaseModel):
    # Required Fields
    game_id: str = Field(alias="GameID")
    start_period: int = Field(default=0, alias="startPeriod")
    end_period: int = Field(default=10, alias="endPeriod")
    range_type: int = Field(default=0, alias="rangeType")
    start_range: int = Field(default=0, alias="startRange")
    end_range: int = Field(default=55800, alias="endRange")
