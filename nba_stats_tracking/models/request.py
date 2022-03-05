from enum import Enum


class PerMode(str, Enum):
    per_game = "PerGame"
    totals = "Totals"


class SeasonType(str, Enum):
    regular_season = "Regular Season"
    playoffs = "Playoffs"
    play_in = "PlayIn"


class LeagueID(str, Enum):
    nba = "00"
    wnba = "10"  # unused for tracking stats but including it in case they ever are
    gleague = "20"  # unused for tracking stats but including it in case they ever are
