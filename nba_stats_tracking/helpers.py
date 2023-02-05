from datetime import date
from typing import Dict, List, Tuple

import requests

from nba_stats_tracking import HEADERS, REQUEST_TIMEOUT
from nba_stats_tracking.models import SeasonType
from nba_stats_tracking.models.boxscore import (
    BoxscoreRequestParameters,
    BoxscoreResults,
)
from nba_stats_tracking.models.scoreboard import (
    ScoreboardRequestParameters,
    ScoreboardResults,
)


def get_json_response(url: str, params: Dict) -> Dict:
    """
    Helper function to get json response for request
    """
    response = requests.get(
        url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT
    )
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_scoreboard_response_json_for_date(game_date: date) -> Dict:
    """
    Gets response data for scoreboard endpoint
    """
    parameters = ScoreboardRequestParameters(GameDate=game_date)

    response_json = get_json_response(
        "https://stats.nba.com/stats/scoreboardV3", parameters.dict(by_alias=True)
    )

    return response_json["scoreboard"]


def get_game_ids_for_date(game_date: date) -> List[str]:
    """
    Gets game ids for all games played on a given date
    """
    results = get_scoreboard_response_json_for_date(game_date)
    scoreboard_result = ScoreboardResults(**results)
    return [game.game_id for game in scoreboard_result.games]


def get_season_from_game_id(game_id: str) -> str:
    """
    Gets season from nba.com game id
    4th and 5th digits of game id represent year season started
    ex 0021900001 is for the 2019-20 season
    """
    if game_id[4] == "9":
        return "20" + game_id[3] + game_id[4] + "-" + str(int(game_id[3]) + 1) + "0"
    else:
        return (
            "20" + game_id[3] + game_id[4] + "-" + game_id[3] + str(int(game_id[4]) + 1)
        )


def get_season_type_from_game_id(game_id: str) -> SeasonType:
    """
    Gets season type from nba.com game id
    Season type is represented in 3rd digit of game id
    2 is Regular Season, 4 is Playoffs
    """
    if game_id[2] == "4":
        return SeasonType.playoffs
    elif game_id[2] == "2":
        return SeasonType.regular_season
    elif game_id[2] == "5":
        return SeasonType.play_in
    return None


def get_boxscore_response_for_game(game_id: str) -> Dict:
    """
    Gets response data from boxscore endpoint for nba.com game id
    """
    parameters = BoxscoreRequestParameters(GameID=game_id)

    response_json = get_json_response(
        "https://stats.nba.com/stats/boxscoretraditionalv3",
        parameters.dict(by_alias=True),
    )

    return response_json["boxScoreTraditional"]


def get_team_id_maps_for_date(game_date: date) -> Tuple[Dict, Dict]:
    """
    Creates dicts mapping team id to game id and team id
    to opponent team id for games on a given date
    """
    results = get_scoreboard_response_json_for_date(game_date)
    scoreboard_result = ScoreboardResults(**results)
    team_id_game_id_map = {}
    team_id_opponent_id_map = {}
    for game in scoreboard_result.games:
        team_id_game_id_map[game.home_team.team_id] = game.game_id
        team_id_game_id_map[game.visitor_team.team_id] = game.game_id
        team_id_opponent_id_map[game.home_team.team_id] = game.visitor_team.team_id
        team_id_opponent_id_map[game.visitor_team.team_id] = game.home_team.team_id
    return team_id_game_id_map, team_id_opponent_id_map


def make_player_team_map_for_game(boxscore_data: BoxscoreResults) -> Dict:
    """
    Creates a dict mapping player id to team id for a game
    """
    player_game_team_map = {
        player.player_id: boxscore_data.away_team.team_id
        for player in boxscore_data.away_team.players
    }
    for player in boxscore_data.home_team.players:
        player_game_team_map[player.player_id] = boxscore_data.home_team.team_id

    return player_game_team_map


def get_player_team_map_for_date(game_date: date) -> Dict:
    """
    Creates a dict mapping player id to team id for all games on a given date
    """
    player_game_team_map = {}
    game_ids = get_game_ids_for_date(game_date)
    for game_id in game_ids:
        results = get_boxscore_response_for_game(game_id)
        boxscore_data = BoxscoreResults(**results)
        player_game_team_map_for_game = make_player_team_map_for_game(boxscore_data)
        player_game_team_map = {**player_game_team_map, **player_game_team_map_for_game}
    return player_game_team_map
