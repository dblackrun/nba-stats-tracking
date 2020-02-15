from nba_stats_tracking import HEADERS, REQUEST_TIMEOUT, PLAYOFFS_STRING, REGULAR_SEASON_STRING

import requests


def make_array_of_dicts_from_response_json(response_json, index):
    """
    makes array of dicts from stats.nba.com response json

    response_json - dict
    index - int, index that holds results in resultSets array, should be either 0 or 1
    """
    headers = response_json['resultSets'][index]['headers']
    rows = response_json['resultSets'][index]['rowSet']
    return [dict(zip(headers, row)) for row in rows]


def get_json_response(url, params):
    """
    helper method to get json response

    args:
    url - string, api endpoint
    params - dict, query params
    """
    response = requests.get(url, params=params, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_scoreboard_response_json_for_date(date):
    """
    date - string, format - MM/DD/YYYY
    """
    parameters = {
        'DayOffset': 0,
        'LeagueID': '00',
        'gameDate': date
    }
    url = 'https://stats.nba.com/stats/scoreboardV2'

    return get_json_response(url, parameters)


def get_game_ids_for_date(date):
    """
    date - string, format - MM/DD/YYYY
    """
    response_json = get_scoreboard_response_json_for_date(date)
    games = make_array_of_dicts_from_response_json(response_json, 0)
    return [game['GAME_ID'] for game in games]


def get_season_from_game_id(game_id):
    """
    season is 4th and 5th digits of game id
    ex 0021900001 is for the 2019-20 season
    """
    if game_id[4] == '9':
        return '20' + game_id[3] + game_id[4] + '-' + str(int(game_id[3]) + 1) + '0'
    else:
        return '20' + game_id[3] + game_id[4] + '-' + game_id[3] + str(int(game_id[4]) + 1)


def get_season_type_from_game_id(game_id):
    """
    season type is 3rd digit of game id, 2 is regular season, 4 is playoffs
    """
    if game_id[2] == '4':
        return PLAYOFFS_STRING
    elif game_id[2] == '2':
        return REGULAR_SEASON_STRING
    return None


def get_boxscore_response_for_game(game_id):
    """
    game_id - string
    """
    url = 'https://stats.nba.com/stats/boxscoretraditionalv2'
    parameters = {
        'GameId': game_id,
        'StartPeriod': 0,
        'EndPeriod': 10,
        'RangeType': 2,
        'StartRange': 0,
        'EndRange': 55800
    }

    return get_json_response(url, parameters)


def get_team_id_maps_for_date(date):
    """
    date - string, format - MM/DD/YYYY
    returns dict mapping team id to game id and dict mapping team id to opponent team id
    """
    response_json = get_scoreboard_response_json_for_date(date)
    games = make_array_of_dicts_from_response_json(response_json, 0)
    team_id_game_id_map = {}
    team_id_opponent_id_map = {}
    for game in games:
        team_id_game_id_map[game['HOME_TEAM_ID']] = game['GAME_ID']
        team_id_game_id_map[game['VISITOR_TEAM_ID']] = game['GAME_ID']
        team_id_opponent_id_map[game['HOME_TEAM_ID']] = game['VISITOR_TEAM_ID']
        team_id_opponent_id_map[game['VISITOR_TEAM_ID']] = game['HOME_TEAM_ID']
    return team_id_game_id_map, team_id_opponent_id_map


def make_player_team_map_for_game(boxscore_data):
    """
    Makes a dict mapping player id to team id for game

    boxscore_data - list of dicts of boxscore data for a game
    """
    player_game_team_map = {player['PLAYER_ID']: player['TEAM_ID'] for player in boxscore_data}

    return player_game_team_map


def get_player_team_map_for_date(date):
    """
    date - string, format - MM/DD/YYYY
    returns dict mapping player id to team id
    """
    player_game_team_map = {}
    game_ids = get_game_ids_for_date(date)
    for game_id in game_ids:
        boxscores_response = get_boxscore_response_for_game(game_id)
        boxscore_data = make_array_of_dicts_from_response_json(boxscores_response, 0)
        player_game_team_map_for_game = make_player_team_map_for_game(boxscore_data)
        player_game_team_map = {**player_game_team_map, **player_game_team_map_for_game}
    return player_game_team_map
