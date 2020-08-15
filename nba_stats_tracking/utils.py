from nba_stats_tracking import (
    HEADERS,
    REQUEST_TIMEOUT,
    PLAYOFFS_STRING,
    REGULAR_SEASON_STRING,
    PLAY_IN_STRING,
)

import requests


def make_array_of_dicts_from_response_json(response_json, index):
    """
    Makes array of dicts from stats.nba.com response json

    :param dict response_json: dict with response from request
    :param int index: index that holds results in resultSets array
    :return: list of dicts with data for each row
    :rtype: list[dict]
    """
    headers = response_json["resultSets"][index]["headers"]
    rows = response_json["resultSets"][index]["rowSet"]
    return [dict(zip(headers, row)) for row in rows]


def get_json_response(url, params):
    """
    Helper function to get json response for request

    :param str url: base url for api endpoint
    :param dict params: params for request
    :return: response json
    :rtype: dict
    """
    response = requests.get(
        url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT
    )
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_scoreboard_response_json_for_date(date):
    """
    Gets response from scoreboard endpoint

    :param str date: Format - MM/DD/YYYY
    :return: response json
    :rtype: dict
    """
    parameters = {"DayOffset": 0, "LeagueID": "00", "gameDate": date}
    url = "https://stats.nba.com/stats/scoreboardV2"

    return get_json_response(url, parameters)


def get_game_ids_for_date(date):
    """
    Gets game ids for all games played on a given date

    :param str date: Format - MM/DD/YYYY
    :return: list of game ids
    :rtype: list
    """
    response_json = get_scoreboard_response_json_for_date(date)
    games = make_array_of_dicts_from_response_json(response_json, 0)
    return [game["GAME_ID"] for game in games]


def get_season_from_game_id(game_id):
    """
    Gets season from nba.com game id
    4th and 5th digits of game id represent year season started
    ex 0021900001 is for the 2019-20 season

    :param str game_id: nba.com game id
    :return: season - Format YYYY-YY ex 2019-20
    :rtype: string
    """
    if game_id[4] == "9":
        return "20" + game_id[3] + game_id[4] + "-" + str(int(game_id[3]) + 1) + "0"
    else:
        return (
            "20" + game_id[3] + game_id[4] + "-" + game_id[3] + str(int(game_id[4]) + 1)
        )


def get_season_type_from_game_id(game_id):
    """
    Gets season type from nba.com game id
    Season type is represented in 3rd digit of game id
    2 is Regular Season, 4 is Playoffs

    :param str game_id: nba.com game id
    :return: season type - Regular Season or Playoffs
    :rtype: string
    """
    if game_id[2] == "4":
        return PLAYOFFS_STRING
    elif game_id[2] == "2":
        return REGULAR_SEASON_STRING
    elif game_id[2] == "5":
        return PLAY_IN_STRING
    return None


def get_boxscore_response_for_game(game_id):
    """
    Gets response from boxscore endpoint

    :param str game_id: nba.com game id
    :return: response json
    :rtype: dict
    """
    url = "https://stats.nba.com/stats/boxscoretraditionalv2"
    parameters = {
        "GameId": game_id,
        "StartPeriod": 0,
        "EndPeriod": 10,
        "RangeType": 2,
        "StartRange": 0,
        "EndRange": 55800,
    }

    return get_json_response(url, parameters)


def get_team_id_maps_for_date(date):
    """
    Creates dicts mapping team id to game id and team id
    to opponent team id for games on a given date

    :param str date: Format - MM/DD/YYYY
    :return: team id game id dict, team id opponent id dict
    :rtype: tuple(dict, dict)
    """
    response_json = get_scoreboard_response_json_for_date(date)
    games = make_array_of_dicts_from_response_json(response_json, 0)
    team_id_game_id_map = {}
    team_id_opponent_id_map = {}
    for game in games:
        team_id_game_id_map[game["HOME_TEAM_ID"]] = game["GAME_ID"]
        team_id_game_id_map[game["VISITOR_TEAM_ID"]] = game["GAME_ID"]
        team_id_opponent_id_map[game["HOME_TEAM_ID"]] = game["VISITOR_TEAM_ID"]
        team_id_opponent_id_map[game["VISITOR_TEAM_ID"]] = game["HOME_TEAM_ID"]
    return team_id_game_id_map, team_id_opponent_id_map


def make_player_team_map_for_game(boxscore_data):
    """
    Creates a dict mapping player id to team id for a game

    :param dict boxscore_data: list of dicts with boxscore data for a game
    :return: player id team id dict
    :rtype: dict
    """
    player_game_team_map = {
        player["PLAYER_ID"]: player["TEAM_ID"] for player in boxscore_data
    }

    return player_game_team_map


def get_player_team_map_for_date(date):
    """
    Creates a dict mapping player id to team id for all games on a given date

    :param str date: Format - MM/DD/YYYY
    :return: player id team id dict
    :rtype: dict
    """
    player_game_team_map = {}
    game_ids = get_game_ids_for_date(date)
    for game_id in game_ids:
        boxscores_response = get_boxscore_response_for_game(game_id)
        boxscore_data = make_array_of_dicts_from_response_json(boxscores_response, 0)
        player_game_team_map_for_game = make_player_team_map_for_game(boxscore_data)
        player_game_team_map = {**player_game_team_map, **player_game_team_map_for_game}
    return player_game_team_map
