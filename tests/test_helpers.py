import json

import responses
import pytest
import requests
from furl import furl
from datetime import date

from nba_stats_tracking import helpers


@responses.activate
def test_get_json_response_bad_response():
    url = "https://stats.nba.com/stats/scoreboardV2"

    responses.add(responses.GET, url, status=400)
    params = {}
    with pytest.raises(requests.exceptions.HTTPError):
        helpers.get_json_response(url, params)


@responses.activate
def test_get_game_ids_for_date():
    with open("tests/data/scoreboard/response.json") as f:
        scoreboard_response = json.loads(f.read())

    scoreboard_response_url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&GameDate=2020-02-02"

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )
    game_date = date(2020, 2, 2)
    game_ids = helpers.get_game_ids_for_date(game_date)
    assert game_ids == ["0021900737", "0021900738", "0021900739", "0021900740"]


def test_get_season_from_game_id():
    assert helpers.get_season_from_game_id("0021500001") == "2015-16"
    assert helpers.get_season_from_game_id("0020000001") == "2000-01"
    assert helpers.get_season_from_game_id("0021900001") == "2019-20"


def test_get_season_type_from_game_id():
    assert helpers.get_season_type_from_game_id("0041500001") == "Playoffs"
    assert helpers.get_season_type_from_game_id("0021500001") == "Regular Season"
    assert helpers.get_season_type_from_game_id("0011500001") is None


@responses.activate
def test_get_team_id_maps_for_date():
    with open("tests/data/scoreboard/response.json") as f:
        scoreboard_response = json.loads(f.read())

    scoreboard_response_url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&GameDate=2020-02-02"

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )
    game_date = date(2020, 2, 2)
    team_id_game_id_map, team_id_opponent_map = helpers.get_team_id_maps_for_date(
        game_date
    )
    assert team_id_game_id_map == {
        1610612743: "0021900737",
        1610612765: "0021900737",
        1610612740: "0021900738",
        1610612745: "0021900738",
        1610612756: "0021900739",
        1610612749: "0021900739",
        1610612741: "0021900740",
        1610612761: "0021900740",
    }

    assert team_id_opponent_map == {
        1610612743: 1610612765,
        1610612765: 1610612743,
        1610612740: 1610612745,
        1610612745: 1610612740,
        1610612756: 1610612749,
        1610612749: 1610612756,
        1610612741: 1610612761,
        1610612761: 1610612741,
    }


@responses.activate
def test_get_player_team_map_for_date():
    with open("tests/data/scoreboard/response.json") as f:
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
    scoreboard_response_url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&GameDate=2020-02-02"

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )

    game_id = "0021900740"
    with open(f"tests/data/game/boxscore/{game_id}.json") as f:
        game_response_json = json.loads(f.read())

    base_url = "https://stats.nba.com/stats/boxscoretraditionalv2"
    query_params = {
        "GameId": game_id,
        "StartPeriod": 0,
        "EndPeriod": 10,
        "RangeType": 2,
        "StartRange": 0,
        "EndRange": 55800,
    }
    url = furl(base_url).add(query_params).url

    responses.add(responses.GET, url, json=game_response_json, status=200)

    game_date = date(2020, 2, 2)
    player_team_map = helpers.get_player_team_map_for_date(game_date)
    assert player_team_map == {
        1628990: 1610612741,
        201152: 1610612741,
        1628436: 1610612741,
        203897: 1610612741,
        203107: 1610612741,
        1629655: 1610612741,
        1629632: 1610612741,
        1627853: 1610612741,
        1627756: 1610612741,
        1626245: 1610612741,
        1629690: 1610612741,
        1627885: 1610612741,
        1628384: 1610612761,
        1627783: 1610612761,
        201586: 1610612761,
        200768: 1610612761,
        1627832: 1610612761,
        1627775: 1610612761,
        1628449: 1610612761,
        1629056: 1610612761,
        1629744: 1610612761,
        1626169: 1610612761,
        1629052: 1610612761,
        1628778: 1610612761,
        1626259: 1610612761,
    }
