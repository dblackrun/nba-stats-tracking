from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class GameItem(BaseModel):
    game_date_est: datetime = Field(alias="GAME_DATE_EST")
    game_sequence: int = Field(alias="GAME_SEQUENCE")
    game_id: str = Field(alias="GAME_ID")
    game_stats_id: int = Field(alias="GAME_STATUS_ID")
    game_stats_text: str = Field(alias="GAME_STATUS_TEXT")
    game_code: str = Field(alias="GAMECODE")
    home_team_id: int = Field(alias="HOME_TEAM_ID")
    visitor_team_id: int = Field(alias="VISITOR_TEAM_ID")
    season: str = Field(alias="SEASON")
    live_period: int = Field(alias="LIVE_PERIOD")
    live_pc_time: str = Field(alias="LIVE_PC_TIME")
    natl_tv_broadcaster: Optional[str] = Field(alias="NATL_TV_BROADCASTER_ABBREVIATION")
    home_tv_broadcaster: Optional[str] = Field(alias="HOME_TV_BROADCASTER_ABBREVIATION")
    away_tv_broadcaster: Optional[str] = Field(alias="AWAY_TV_BROADCASTER_ABBREVIATION")
    live_period_time_bcast: str = Field(alias="LIVE_PERIOD_TIME_BCAST")
    arena_name: str = Field(alias="ARENA_NAME")
    wh_status: int = Field(alias="WH_STATUS")

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ScoreboardResults:
    results: List[GameItem]

    def __init__(self, **kwargs):
        headers = kwargs.get("headers", [])
        rows = kwargs.get("rowSet", [])
        self.results = [GameItem(**dict(zip(headers, row))) for row in rows]

    def __iter__(self):
        return iter(self.results)
