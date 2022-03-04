import json
from datetime import date

import responses
from furl import furl

from nba_stats_tracking import tracking_shots
from nba_stats_tracking.models.request import SeasonType
from nba_stats_tracking.models.tracking_shots import (
    CloseDefDist,
    GeneralRange,
    TrackingShotItem,
)


@responses.activate
def test_get_tracking_shot_stats():
    with open(
        "tests/data/tracking_shots/player_wide_open_catch_and_shoot_response.json"
    ) as f:
        wide_open_response_json = json.loads(f.read())

    with open(
        "tests/data/tracking_shots/player_open_catch_and_shoot_response.json"
    ) as f:
        open_response_json = json.loads(f.read())

    season = "2019-20"
    season_type = SeasonType.regular_season
    def_distances = [CloseDefDist.range_6_plus_ft, CloseDefDist.range_4_6_ft]
    general_range = GeneralRange.catch_and_shoot

    base_url = "https://stats.nba.com/stats/leaguedashplayerptshot"
    wide_open_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": def_distances[0],
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": general_range,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    wide_open_url = furl(base_url).add(wide_open_query_params).url
    responses.add(
        responses.GET, wide_open_url, json=wide_open_response_json, status=200
    )

    open_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": def_distances[1],
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": general_range,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    open_url = furl(base_url).add(open_query_params).url
    responses.add(responses.GET, open_url, json=open_response_json, status=200)

    with open("tests/data/tracking_shots/player_overall_response.json") as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": "",
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": GeneralRange.overall,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    overall_url = furl(base_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    stats = tracking_shots.get_tracking_shot_stats(
        tracking_shots.EntityType.player,
        [season],
        [season_type],
        CloseDefDistRange=def_distances,
        GeneralRange=[general_range],
    )
    assert len(stats) == 486
    for stat in stats:
        if stat.player_id == 203507:
            assert stat.player_name == "Giannis Antetokounmpo"
            assert stat.player_last_team_id == 1610612749
            assert stat.player_last_team_abbreviation == "MIL"
            assert stat.fgm == 186
            assert stat.fga == 409
            assert stat.fg2m == 114
            assert stat.fg2a == 187
            assert stat.fg3m == 72
            assert stat.fg3a == 222
            assert stat.fg2pct == 114 / 187
            assert stat.fg3pct == 72 / 222
            assert stat.efg == (114 + 1.5 * 72) / 409
            assert stat.season == "2019-20 Regular Season"
            assert stat.overall_fg2a == 707
            assert stat.overall_fg3a == 232
            assert stat.overall_fga == 939
            assert stat.fg2a_frequency == 187 / 939
            assert stat.fg3a_frequency == 222 / 939
            assert stat.fga_frequency == 409 / 939
            assert stat.frequency_of_fg2a == 187 / 707
            assert stat.frequency_of_fg3a == 222 / 232


@responses.activate
def test_get_tracking_shot_stats_team():
    with open("tests/data/tracking_shots/team_wide_open_response.json") as f:
        wide_open_response_json = json.loads(f.read())

    season = "2019-20"
    season_type = SeasonType.regular_season
    def_distance = CloseDefDist.range_6_plus_ft
    general_range = GeneralRange.overall

    base_url = "https://stats.nba.com/stats/leaguedashteamptshot"
    wide_open_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": def_distance,
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": general_range,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    wide_open_url = furl(base_url).add(wide_open_query_params).url
    responses.add(
        responses.GET, wide_open_url, json=wide_open_response_json, status=200
    )

    with open("tests/data/tracking_shots/team_overall_response.json") as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": "",
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": GeneralRange.overall,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    overall_url = furl(base_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    stats = tracking_shots.get_tracking_shot_stats(
        tracking_shots.EntityType.team,
        [season],
        [season_type],
        CloseDefDistRange=[def_distance],
        GeneralRange=[general_range],
    )
    assert len(stats) == 30
    for stat in stats:
        if stat.team_id == 1610612749:
            assert stat.team_abbreviation == "MIL"
            assert stat.fg3m == 561
            assert stat.fg3a == 1532
            assert stat.overall_fg3a == 2804
            assert stat.fg3pct == stat.fg3m / stat.fg3a


@responses.activate
def test_get_tracking_shot_stats_opponent():
    with open("tests/data/tracking_shots/opponent_wide_open_response.json") as f:
        wide_open_response_json = json.loads(f.read())

    season = "2019-20"
    season_type = SeasonType.regular_season
    def_distance = CloseDefDist.range_6_plus_ft
    general_range = GeneralRange.overall

    base_url = "https://stats.nba.com/stats/leaguedashoppptshot"
    wide_open_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": def_distance,
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": general_range,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    wide_open_url = furl(base_url).add(wide_open_query_params).url
    responses.add(
        responses.GET, wide_open_url, json=wide_open_response_json, status=200
    )

    with open("tests/data/tracking_shots/opponent_overall_response.json") as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": "",
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": GeneralRange.overall,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    overall_url = furl(base_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    stats = tracking_shots.get_tracking_shot_stats(
        tracking_shots.EntityType.opponent,
        [season],
        [season_type],
        CloseDefDistRange=[def_distance],
        GeneralRange=[general_range],
    )
    assert len(stats) == 30
    for stat in stats:
        if stat.team_id == 1610612761:
            assert stat.team_abbreviation == "TOR"
            assert stat.fg3m == 495
            assert stat.fg3a == 1400
            assert stat.overall_fg3a == 2765
            assert stat.fg3pct == stat.fg3m / stat.fg3a


@responses.activate
def test_aggregate_full_season_tracking_shot_stats_for_seasons():
    with open(
        "tests/data/tracking_shots/player_wide_open_catch_and_shoot_response.json"
    ) as f:
        wide_open_response_json = json.loads(f.read())

    with open(
        "tests/data/tracking_shots/player_open_catch_and_shoot_response.json"
    ) as f:
        open_response_json = json.loads(f.read())

    season = "2019-20"
    season_type = SeasonType.regular_season
    def_distances = [CloseDefDist.range_6_plus_ft, CloseDefDist.range_4_6_ft]
    general_range = GeneralRange.catch_and_shoot

    base_url = "https://stats.nba.com/stats/leaguedashplayerptshot"
    wide_open_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": def_distances[0],
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": general_range,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    wide_open_url = furl(base_url).add(wide_open_query_params).url
    responses.add(
        responses.GET, wide_open_url, json=wide_open_response_json, status=200
    )

    open_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": def_distances[1],
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": general_range,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    open_url = furl(base_url).add(open_query_params).url
    responses.add(responses.GET, open_url, json=open_response_json, status=200)

    with open("tests/data/tracking_shots/player_overall_response.json") as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "CloseDefDistRange": "",
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": "Overall",
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    overall_url = furl(base_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    (
        stats,
        league_totals,
    ) = tracking_shots.aggregate_full_season_tracking_shot_stats_for_seasons(
        tracking_shots.EntityType.player,
        [season],
        [season_type],
        CloseDefDistRange=def_distances,
        GeneralRange=[general_range],
    )
    assert len(stats) == 486

    for stat in stats:
        if stat.player_id == 203507:
            assert stat.player_name == "Giannis Antetokounmpo"
            assert stat.player_last_team_id == 1610612749
            assert stat.player_last_team_abbreviation == "MIL"
            assert stat.fgm == 186
            assert stat.fga == 409
            assert stat.fg2m == 114
            assert stat.fg2a == 187
            assert stat.fg3m == 72
            assert stat.fg3a == 222
            assert stat.fg2pct == 114 / 187
            assert stat.fg3pct == 72 / 222
            assert stat.efg == (114 + 1.5 * 72) / 409
            assert stat.season == "2019-20 Regular Season"
            assert stat.overall_fg2a == 707
            assert stat.overall_fg3a == 232
            assert stat.overall_fga == 939
            assert stat.fg2a_frequency == 187 / 939
            assert stat.fg3a_frequency == 222 / 939
            assert stat.fga_frequency == 409 / 939
            assert stat.frequency_of_fg2a == 187 / 707
            assert stat.frequency_of_fg3a == 222 / 232

    assert league_totals.efg == (13285 + 1.5 * 16175) / (24199 + 44439)
    assert league_totals.fg2a == 24199
    assert league_totals.fg2m == 13285
    assert league_totals.fg2pct == 13285 / 24199
    assert league_totals.fg3a == 44439
    assert league_totals.fg3m == 16175
    assert league_totals.fg3pct == 16175 / 44439
    assert league_totals.fga == 68638
    assert league_totals.fgm == 29460
    assert league_totals.overall_fg2a == 86795
    assert league_totals.overall_fg3a == 53065
    assert league_totals.overall_fga == 139860
    assert league_totals.fg2a_frequency == 24199 / 139860
    assert league_totals.fg3a_frequency == 44439 / 139860
    assert league_totals.fga_frequency == 68638 / 139860
    assert league_totals.frequency_of_fg2a == 24199 / 86795
    assert league_totals.frequency_of_fg3a == 44439 / 53065


@responses.activate
def test_generate_tracking_shot_game_logs():
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

    with open(
        "tests/data/tracking_shots/player_wide_open_single_date_response.json"
    ) as f:
        shots_response_json = json.loads(f.read())

    def_distance = CloseDefDist.range_6_plus_ft
    game_date = date(2020, 2, 2)

    shots_url = "https://stats.nba.com/stats/leaguedashplayerptshot"
    shots_query_params = {
        "Season": "2019-20",
        "SeasonType": SeasonType.regular_season,
        "DateFrom": game_date.strftime("%m/%d/%Y"),
        "DateTo": game_date.strftime("%m/%d/%Y"),
        "CloseDefDistRange": def_distance,
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": GeneralRange.overall,
        "PerMode": "Totals",
        "LeagueID": "00",
    }

    url = furl(shots_url).add(shots_query_params).url

    responses.add(responses.GET, url, json=shots_response_json, status=200)

    with open("tests/data/tracking_shots/player_overall_response_for_date.json") as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        "Season": "2019-20",
        "SeasonType": SeasonType.regular_season,
        "DateFrom": game_date.strftime("%m/%d/%Y"),
        "DateTo": game_date.strftime("%m/%d/%Y"),
        "CloseDefDistRange": "",
        "ShotClockRange": "",
        "ShotDistRange": "",
        "TouchTimeRange": "",
        "DribbleRange": "",
        "GeneralRange": GeneralRange.overall,
        "PerMode": "Totals",
        "LeagueID": "00",
    }
    overall_url = furl(shots_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    game_logs = tracking_shots.generate_tracking_shot_game_logs(
        tracking_shots.EntityType.player,
        game_date,
        game_date,
        CloseDefDistRange=[def_distance],
    )

    for game_log in game_logs:
        if game_log.player_id == 1627832:
            assert game_log.player_name == "Fred VanVleet"
            assert game_log.player_last_team_id == 1610612761
            assert game_log.player_last_team_abbreviation == "TOR"
            assert game_log.fgm == 2
            assert game_log.fga == 6
            assert game_log.fg2m == 0
            assert game_log.fg2a == 0
            assert game_log.fg3m == 2
            assert game_log.fg3a == 6
            assert game_log.fg2pct == 0
            assert game_log.fg3pct == 2 / 6
            assert game_log.efg == 0.5
            assert game_log.team_id == 1610612761
            assert game_log.game_id == "0021900740"
            assert game_log.opponent_team_id == 1610612741
            assert game_log.overall_fg2a == 5
            assert game_log.overall_fg3a == 6
            assert game_log.overall_fga == 11
            assert game_log.fg2a_frequency == 0
            assert game_log.fg3a_frequency == 6 / 11
            assert game_log.fga_frequency == 6 / 11
            assert game_log.frequency_of_fg2a == 0
            assert game_log.frequency_of_fg3a == 6 / 6


@responses.activate
def test_generate_tracking_shot_game_logs_for_date_with_no_games():
    with open("tests/data/scoreboard/response.json") as f:
        scoreboard_response = json.loads(f.read())
    scoreboard_response["resultSets"][0]["rowSet"] = []
    scoreboard_response_url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&GameDate=2020-02-02"

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )

    def_distance = CloseDefDist.range_6_plus_ft
    game_date = date(2020, 2, 2)

    game_logs = tracking_shots.generate_tracking_shot_game_logs(
        tracking_shots.EntityType.player,
        game_date,
        game_date,
        CloseDefDistRange=[def_distance],
    )
    assert game_logs == []


def test_0_as_denominator_returns_0_pct():
    a = TrackingShotItem(
        FGA=0, FG2A=0, FG3A=0, overall_fg2a=0, overall_fg3a=0, overall_fga=0
    )
    assert a.fg2pct == 0
    assert a.fg3pct == 0
    assert a.efg == 0
    assert a.fga_frequency == 0
    assert a.fg2a_frequency == 0
    assert a.fg3a_frequency == 0
    assert a.frequency_of_fg2a == 0
    assert a.frequency_of_fg3a == 0


def test_sum_tracking_totals_for_not_entity_returns_empty_list():
    a = tracking_shots.sum_tracking_shot_totals(
        "asdgsd",
        [
            TrackingShotItem(
                FGA=0, FG2A=0, FG3A=0, overall_fg2a=0, overall_fg3a=0, overall_fga=0
            )
        ],
    )
    assert a == []
