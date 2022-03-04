from typing import List, Optional

from pydantic import BaseModel, Field


class MatchupStatistics(BaseModel):
    minutes_str: str = Field(alias="matchupMinutes")
    seconds: float = Field(alias="matchupMinutesSort")
    partial_possessions: float = Field(alias="partialPossessions")
    percentage_defender_total_time: float = Field(alias="percentageDefenderTotalTime")
    percentage_offensive_total_time: float = Field(alias="percentageOffensiveTotalTime")
    percentage_total_time_both_on: float = Field(alias="percentageTotalTimeBothOn")
    switches_on: int = Field(alias="switchesOn")
    player_points: int = Field(alias="playerPoints")
    team_points: int = Field(alias="teamPoints")
    assists: int = Field(alias="matchupAssists")
    potential_assists: int = Field(alias="matchupPotentialAssists")
    turnovers: int = Field(alias="matchupTurnovers")
    blocks: int = Field(alias="matchupBlocks")
    fgm: int = Field(alias="matchupFieldGoalsMade")
    fga: int = Field(alias="matchupFieldGoalsAttempted")
    fg3m: int = Field(alias="matchupThreePointersMade")
    fg3a: int = Field(alias="matchupThreePointersAttempted")
    help_blocks: int = Field(alias="helpBlocks")
    help_fgm: int = Field(alias="helpFieldGoalsMade")
    help_fga: int = Field(alias="helpFieldGoalsAttempted")
    ftm: int = Field(alias="matchupFreeThrowsMade")
    fta: int = Field(alias="matchupFreeThrowsAttempted")
    shooting_fouls: int = Field(alias="shootingFouls")


class Matchup(BaseModel):
    player_id: int = Field(alias="personId")
    first_name: str = Field(alias="firstName")
    family_name: str = Field(alias="familyName")
    name_initial: str = Field(alias="nameI")
    player_slug: str = Field(alias="playerSlug")
    jersey_num: str = Field(alias="jerseyNum")
    statistics: MatchupStatistics = Field(alias="statistics")


class MatchupPlayer(BaseModel):
    player_id: Optional[int] = Field(alias="personId")
    first_name: Optional[str] = Field(alias="firstName")
    family_name: Optional[str] = Field(alias="familyName")
    name_initial: Optional[str] = Field(alias="nameI")
    player_slug: Optional[str] = Field(alias="playerSlug")
    position: Optional[str] = Field(alias="position")
    comment: Optional[str] = Field(alias="comment")
    jersey_num: Optional[str] = Field(alias="jerseyNum")
    matchups: Optional[List[Matchup]] = Field(alias="matchups")


class MatchupTeam(BaseModel):
    team_id: Optional[int] = Field(alias="teamId")
    team_city: Optional[str] = Field(alias="teamCity")
    team_name: Optional[str] = Field(alias="teamName")
    team_tricode: Optional[str] = Field(alias="teamTricode")
    team_slug: Optional[str] = Field(alias="teamSlug")
    players: List[MatchupPlayer] = Field(alias="players")


class MatchupResults(BaseModel):
    game_id: str = Field(alias="gameId")
    away_team_id: int = Field(alias="awayTeamId")
    home_team_id: int = Field(alias="homeTeamId")
    home_team: MatchupTeam = Field(alias="homeTeam")
    away_team: MatchupTeam = Field(alias="awayTeam")
