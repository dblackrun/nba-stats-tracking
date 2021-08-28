import json

import responses
from furl import furl

from nba_stats_tracking import tracking


def generate_url(measure_type, season, season_type, entity_type):
    base_url = "https://stats.nba.com/stats/leaguedashptstats"
    query_params = {
        "PlayerOrTeam": entity_type.title(),
        "PtMeasureType": measure_type,
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "GameScope": "",
        "LastNGames": 0,
        "LeagueID": "00",
        "Location": "",
        "Month": 0,
        "OpponentTeamID": 0,
        "Outcome": "",
        "PerMode": "Totals",
        "PlayerExperience": "",
        "PlayerPosition": "",
        "SeasonSegment": "",
        "StarterBench": "",
        "VsConference": "",
        "VsDivision": "",
    }
    url = furl(base_url).add(query_params).url
    return url


@responses.activate
def test_get_tracking_response_json_for_stat_measure():
    with open("tests/data/team_2020_catch_and_shoot_response.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = "team"
    measure_type = "CatchShoot"
    season = "2019-20"
    season_type = "Regular Season"

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    response_json = tracking.get_tracking_response_json_for_stat_measure(
        measure_type, season, season_type, entity_type, "Totals"
    )
    assert len(response_json["resultSets"][0]["rowSet"]) == 30


@responses.activate
def test_team_aggregate_full_season_tracking_stats_for_seasons():
    with open("tests/data/team_2020_catch_and_shoot_response.json") as f:
        tracking_2020_response_json = json.loads(f.read())

    with open("tests/data/team_2019_catch_and_shoot_response.json") as f:
        tracking_2019_response_json = json.loads(f.read())

    entity_type = "team"
    measure_type = "CatchShoot"
    seasons = ["2018-19", "2019-20"]
    season_types = ["Regular Season"]

    url_2020 = generate_url(measure_type, seasons[1], season_types[0], entity_type)
    responses.add(responses.GET, url_2020, json=tracking_2020_response_json, status=200)

    url_2019 = generate_url(measure_type, seasons[0], season_types[0], entity_type)
    responses.add(responses.GET, url_2019, json=tracking_2019_response_json, status=200)

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, seasons, season_types, entity_type
    )
    assert len(stats) == 30
    for stat in stats:
        if stat["TEAM_ID"] == 1610612737:
            assert stat == {
                "TEAM_ID": 1610612737,
                "TEAM_NAME": "Atlanta Hawks",
                "TEAM_ABBREVIATION": "ATL",
                "MIN": 32170.0,
                "CATCH_SHOOT_FGM": 1243,
                "CATCH_SHOOT_FGA": 3537,
                "CATCH_SHOOT_PTS": 3658,
                "CATCH_SHOOT_FG3M": 1172,
                "CATCH_SHOOT_FG3A": 3313,
            }
    assert league_totals == {
        "MIN": 956470.0,
        "CATCH_SHOOT_FGM": 37981,
        "CATCH_SHOOT_FGA": 101524,
        "CATCH_SHOOT_PTS": 109049,
        "CATCH_SHOOT_FG3M": 33087,
        "CATCH_SHOOT_FG3A": 90075,
    }


@responses.activate
def test_player_aggregate_full_season_tracking_stats_for_seasons():
    with open("tests/data/player_2020_speed_distance_response.json") as f:
        tracking_2020_response_json = json.loads(f.read())

    with open("tests/data/player_2019_speed_distance_response.json") as f:
        tracking_2019_response_json = json.loads(f.read())

    entity_type = "player"
    measure_type = "SpeedDistance"
    seasons = ["2018-19", "2019-20"]
    season_types = ["Regular Season"]

    url_2020 = generate_url(measure_type, seasons[1], season_types[0], entity_type)
    responses.add(responses.GET, url_2020, json=tracking_2020_response_json, status=200)

    url_2019 = generate_url(measure_type, seasons[0], season_types[0], entity_type)
    responses.add(responses.GET, url_2019, json=tracking_2019_response_json, status=200)

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, seasons, season_types, entity_type
    )
    assert len(stats) == 645
    for stat in stats:
        if stat["PLAYER_ID"] == 203932:
            assert stat["MIN"] == 4035.0
            assert stat["DIST_FEET"] == 1604918
    assert league_totals["MIN"] == 961707.0
    assert league_totals["DIST_FEET"] == 379831114


@responses.activate
def test_generate_tracking_game_logs():
    with open("tests/data/scoreboard_response.json") as f:
        scoreboard_response = json.loads(f.read())
    scoreboard_response["resultSets"][0]["rowSet"] = [
        [
            "2020-02-02T00:00:00",
            4,
            "0021900740",
            3,
            "Final",
            "20200202/CHITOR",
            1610612761,
            1610612741,
            "2019",
            4,
            "     ",
            None,
            "TSN1/4",
            "NBCSCH",
            "Q4       - ",
            "Scotiabank Arena",
            1,
        ]
    ]
    scoreboard_response_url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=02/02/2020"

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )

    with open("tests/data/game_boxscore_response.json") as f:
        game_response_json = json.loads(f.read())

    game_id = "0021900740"

    boxscore_url = "https://stats.nba.com/stats/boxscoretraditionalv2"
    query_params = {
        "GameId": game_id,
        "StartPeriod": 0,
        "EndPeriod": 10,
        "RangeType": 2,
        "StartRange": 0,
        "EndRange": 55800,
    }
    url = furl(boxscore_url).add(query_params).url

    responses.add(responses.GET, url, json=game_response_json, status=200)

    with open("tests/data/player_catch_shoot_date_filter.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = "player"
    measure_type = "CatchShoot"
    season = "2019-20"
    season_type = "Regular Season"
    date = "02/02/2020"

    base_url = "https://stats.nba.com/stats/leaguedashptstats"
    query_params = {
        "PlayerOrTeam": entity_type.title(),
        "PtMeasureType": measure_type,
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": date,
        "DateTo": date,
        "GameScope": "",
        "LastNGames": 0,
        "LeagueID": "00",
        "Location": "",
        "Month": 0,
        "OpponentTeamID": 0,
        "Outcome": "",
        "PerMode": "PerGame",
        "PlayerExperience": "",
        "PlayerPosition": "",
        "SeasonSegment": "",
        "StarterBench": "",
        "VsConference": "",
        "VsDivision": "",
    }
    tracking_url = furl(base_url).add(query_params).url

    responses.add(responses.GET, tracking_url, json=tracking_response_json, status=200)

    game_logs = tracking.generate_tracking_game_logs(
        measure_type, entity_type, date, date
    )
    assert len(game_logs) == 24
    for game_log in game_logs:
        if game_log["PLAYER_ID"] == 1627832:
            assert game_log == {
                "PLAYER_ID": 1627832,
                "PLAYER_NAME": "Fred VanVleet",
                "TEAM_ID": 1610612761,
                "TEAM_ABBREVIATION": "TOR",
                "GP": 1,
                "W": 1,
                "L": 0,
                "MIN": 32.0,
                "CATCH_SHOOT_FGM": 1,
                "CATCH_SHOOT_FGA": 5,
                "CATCH_SHOOT_FG_PCT": 0.2,
                "CATCH_SHOOT_PTS": 3,
                "CATCH_SHOOT_FG3M": 1,
                "CATCH_SHOOT_FG3A": 5,
                "CATCH_SHOOT_FG3_PCT": 0.2,
                "CATCH_SHOOT_EFG_PCT": 0.3,
                "SEASON": "2019-20 Regular Season",
                "GAME_ID": "0021900740",
                "OPPONENT_TEAM_ID": 1610612741,
            }
