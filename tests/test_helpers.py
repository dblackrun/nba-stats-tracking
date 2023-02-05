import json
from datetime import date

import pytest
import requests
import responses
from furl import furl

from nba_stats_tracking import helpers


@responses.activate
def test_get_json_response_bad_response():
    url = "https://stats.nba.com/stats/scoreboardV3"

    responses.add(responses.GET, url, status=400)
    params = {}
    with pytest.raises(requests.exceptions.HTTPError):
        helpers.get_json_response(url, params)


@responses.activate
def test_get_game_ids_for_date():
    with open("tests/data/scoreboard/response.json") as f:
        scoreboard_response = json.loads(f.read())

    scoreboard_response_url = (
        "https://stats.nba.com/stats/scoreboardV3?LeagueID=00&GameDate=2020-02-02"
    )

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

    scoreboard_response_url = (
        "https://stats.nba.com/stats/scoreboardV3?&LeagueID=00&GameDate=2020-02-02"
    )

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
    # hard code response to only have one game
    scoreboard_response["scoreboard"]["games"] = [
        {
            "gameId": "0021900740",
            "gameCode": "20200202/CHITOR",
            "gameStatus": 3,
            "gameStatusText": "Final",
            "period": 4,
            "gameClock": "",
            "gameTimeUTC": "2020-02-02T20:00:00Z",
            "gameEt": "2020-02-02T15:00:00Z",
            "regulationPeriods": 4,
            "seriesGameNumber": "",
            "seriesText": "",
            "ifNecessary": False,
            "gameLeaders": {
                "homeLeaders": {
                    "personId": 1629056,
                    "name": "Terence Davis",
                    "playerSlug": "terence-davis",
                    "jerseyNum": "0",
                    "position": "G",
                    "teamTricode": "TOR",
                    "points": 31,
                    "rebounds": 4,
                    "assists": 1,
                },
                "awayLeaders": {
                    "personId": 203897,
                    "name": "Zach LaVine",
                    "playerSlug": "zach-lavine",
                    "jerseyNum": "8",
                    "position": "G-F",
                    "teamTricode": "CHI",
                    "points": 18,
                    "rebounds": 7,
                    "assists": 7,
                },
            },
            "teamLeaders": {
                "homeLeaders": {
                    "personId": 1627783,
                    "name": "Pascal Siakam",
                    "playerSlug": "pascal-siakam",
                    "jerseyNum": "43",
                    "position": "F",
                    "teamTricode": "TOR",
                    "points": 22.9,
                    "rebounds": 7.3,
                    "assists": 3.5,
                },
                "awayLeaders": {
                    "personId": 203897,
                    "name": "Zach LaVine",
                    "playerSlug": "zach-lavine",
                    "jerseyNum": "8",
                    "position": "G-F",
                    "teamTricode": "CHI",
                    "points": 25.5,
                    "rebounds": 4.8,
                    "assists": 4.2,
                },
                "seasonLeadersFlag": 0,
            },
            "broadcasters": {
                "nationalBroadcasters": [],
                "nationalRadioBroadcasters": [],
                "nationalOttBroadcasters": [],
                "homeTvBroadcasters": [
                    {"broadcasterId": 1546, "broadcastDisplay": "TSN1/4"}
                ],
                "homeRadioBroadcasters": [
                    {"broadcasterId": 1053, "broadcastDisplay": "CJCL"}
                ],
                "homeOttBroadcasters": [],
                "awayTvBroadcasters": [
                    {"broadcasterId": 1656, "broadcastDisplay": "NBCSCH"}
                ],
                "awayRadioBroadcasters": [
                    {"broadcasterId": 1687, "broadcastDisplay": "WSCR"}
                ],
                "awayOttBroadcasters": [],
            },
            "homeTeam": {
                "teamId": 1610612761,
                "teamName": "Raptors",
                "teamCity": "Toronto",
                "teamTricode": "TOR",
                "teamSlug": "raptors",
                "wins": 36,
                "losses": 14,
                "score": 129,
                "seed": 0,
                "inBonus": None,
                "timeoutsRemaining": 1,
                "periods": [
                    {"period": 1, "periodType": "REGULAR", "score": 32},
                    {"period": 2, "periodType": "REGULAR", "score": 28},
                    {"period": 3, "periodType": "REGULAR", "score": 35},
                    {"period": 4, "periodType": "REGULAR", "score": 34},
                ],
            },
            "awayTeam": {
                "teamId": 1610612741,
                "teamName": "Bulls",
                "teamCity": "Chicago",
                "teamTricode": "CHI",
                "teamSlug": "bulls",
                "wins": 19,
                "losses": 33,
                "score": 102,
                "seed": 0,
                "inBonus": None,
                "timeoutsRemaining": 0,
                "periods": [
                    {"period": 1, "periodType": "REGULAR", "score": 29},
                    {"period": 2, "periodType": "REGULAR", "score": 34},
                    {"period": 3, "periodType": "REGULAR", "score": 22},
                    {"period": 4, "periodType": "REGULAR", "score": 17},
                ],
            },
        }
    ]
    scoreboard_response_url = (
        "https://stats.nba.com/stats/scoreboardV3?LeagueID=00&GameDate=2020-02-02"
    )

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )

    game_id = "0021900740"
    with open(f"tests/data/game/boxscore/{game_id}.json") as f:
        game_response_json = json.loads(f.read())

    base_url = "https://stats.nba.com/stats/boxscoretraditionalv3"
    query_params = {
        "GameID": game_id,
        "StartPeriod": 0,
        "EndPeriod": 10,
        "RangeType": 2,
        "StartRange": 0,
        "EndRange": 55800,
        "LeagueID": "00",
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
