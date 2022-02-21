from pydantic import BaseModel, Field


class BoxscoreRequestParameters(BaseModel):
    # Required Fields
    game_id: str = Field(alias="GameId")
    start_period: int = Field(default=0, alias="StartPeriod")
    end_period: int = Field(default=10, alias="EndPeriod")
    range_type: int = Field(default=2, alias="RangeType")
    start_range: int = Field(default=0, alias="StartRange")
    end_range: int = Field(default=55800, alias="EndRange")
