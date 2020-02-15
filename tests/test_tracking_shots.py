import json

import responses
from furl import furl

from nba_stats_tracking import tracking_shots


@responses.activate
def test_get_tracking_shots_response_team():
    with open('tests/data/team_wide_open_response.json') as f:
        tracking_response_json = json.loads(f.read())

    season = '2019-20'
    season_type = 'Regular Season'
    close_def_dist = '6+ Feet - Wide Open'

    base_url = 'https://stats.nba.com/stats/leaguedashteamptshot'
    query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': close_def_dist,
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    url = furl(base_url).add(query_params).url

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    response_json = tracking_shots.get_tracking_shots_response('team', season, season_type, close_def_dist=close_def_dist)
    assert len(response_json['resultSets'][0]['rowSet']) == 30


@responses.activate
def test_get_tracking_shots_response_player():
    with open('tests/data/player_late_clock_response.json') as f:
        tracking_response_json = json.loads(f.read())

    season = '2019-20'
    season_type = 'Regular Season'
    shot_clock = '4-0 Very Late'

    base_url = 'https://stats.nba.com/stats/leaguedashplayerptshot'
    query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': '',
        'ShotClockRange': shot_clock,
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    url = furl(base_url).add(query_params).url

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    response_json = tracking_shots.get_tracking_shots_response('player', season, season_type, shot_clock=shot_clock)
    assert len(response_json['resultSets'][0]['rowSet']) == 457


@responses.activate
def test_get_tracking_shots_response_opponent():
    with open('tests/data/opponent_0_dribbles_response.json') as f:
        tracking_response_json = json.loads(f.read())

    season = '2019-20'
    season_type = 'Regular Season'
    dribbles = '0 Dribbles'

    base_url = 'https://stats.nba.com/stats/leaguedashoppptshot'
    query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': '',
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': dribbles,
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    url = furl(base_url).add(query_params).url

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    response_json = tracking_shots.get_tracking_shots_response('opponent', season, season_type, dribbles=dribbles)
    assert len(response_json['resultSets'][0]['rowSet']) == 30


def test_get_tracking_shots_response_invalid_entity_type():
    entity_type = 'bad_type'
    season = '2019-20'
    season_type = 'Regular Season'

    response_json = tracking_shots.get_tracking_shots_response(entity_type, season, season_type)
    assert response_json is None


@responses.activate
def test_get_tracking_shot_stats():
    with open('tests/data/player_wide_open_catch_and_shoot_response.json') as f:
        wide_open_response_json = json.loads(f.read())

    with open('tests/data/player_open_catch_and_shoot_response.json') as f:
        open_response_json = json.loads(f.read())

    season = '2019-20'
    season_type = 'Regular Season'
    def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
    general_range = 'CatchShoot'

    base_url = 'https://stats.nba.com/stats/leaguedashplayerptshot'
    wide_open_query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': def_distances[0],
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': general_range,
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    wide_open_url = furl(base_url).add(wide_open_query_params).url
    responses.add(responses.GET, wide_open_url, json=wide_open_response_json, status=200)

    open_query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': def_distances[1],
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': general_range,
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    open_url = furl(base_url).add(open_query_params).url
    responses.add(responses.GET, open_url, json=open_response_json, status=200)

    with open('tests/data/player_overall_response.json') as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': '',
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    overall_url = furl(base_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    stats = tracking_shots.get_tracking_shot_stats('player', [season], [season_type], close_def_dists=def_distances, general_ranges=[general_range])
    assert len(stats) == 486
    for stat in stats:
        if stat['PLAYER_ID'] == 203507:
            assert stat == {
                'PLAYER_ID': 203507,
                'PLAYER_NAME': 'Giannis Antetokounmpo',
                'PLAYER_LAST_TEAM_ID': 1610612749,
                'PLAYER_LAST_TEAM_ABBREVIATION': 'MIL',
                'FGM': 186,
                'FGA': 409,
                'FG2M': 114,
                'FG2A': 187,
                'FG3M': 72,
                'FG3A': 222,
                'FG2_PCT': 114 / 187,
                'FG3_PCT': 72 / 222,
                'EFG_PCT': (114 + 1.5 * 72) / 409,
                'SEASON': '2019-20 Regular Season',
                'OVERALL_FG2A': 707,
                'OVERALL_FG3A': 232,
                'OVERALL_FGA': 939,
                'FG2A_FREQUENCY': 187 / 939,
                'FG3A_FREQUENCY': 222 / 939,
                'FGA_FREQUENCY': 409 / 939,
                'FREQUENCY_OF_FG2A': 187 / 707,
                'FREQUENCY_OF_FG3A': 222 / 232,
            }


@responses.activate
def test_aggregate_full_season_tracking_shot_stats_for_seasons():
    with open('tests/data/player_wide_open_catch_and_shoot_response.json') as f:
        wide_open_response_json = json.loads(f.read())

    with open('tests/data/player_open_catch_and_shoot_response.json') as f:
        open_response_json = json.loads(f.read())

    season = '2019-20'
    season_type = 'Regular Season'
    def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
    general_range = 'CatchShoot'

    base_url = 'https://stats.nba.com/stats/leaguedashplayerptshot'
    wide_open_query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': def_distances[0],
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': general_range,
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    wide_open_url = furl(base_url).add(wide_open_query_params).url
    responses.add(responses.GET, wide_open_url, json=wide_open_response_json, status=200)

    open_query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': def_distances[1],
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': general_range,
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    open_url = furl(base_url).add(open_query_params).url
    responses.add(responses.GET, open_url, json=open_response_json, status=200)

    with open('tests/data/player_overall_response.json') as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'CloseDefDistRange': '',
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    overall_url = furl(base_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    stats, league_totals = tracking_shots.aggregate_full_season_tracking_shot_stats_for_seasons('player', [season], [season_type], close_def_dists=def_distances, general_ranges=[general_range])
    assert len(stats) == 486
    for stat in stats:
        if stat['PLAYER_ID'] == 203507:
            assert stat == {
                'PLAYER_ID': 203507,
                'PLAYER_NAME': 'Giannis Antetokounmpo',
                'PLAYER_LAST_TEAM_ID': 1610612749,
                'PLAYER_LAST_TEAM_ABBREVIATION': 'MIL',
                'FGM': 186,
                'FGA': 409,
                'FG2M': 114,
                'FG2A': 187,
                'FG3M': 72,
                'FG3A': 222,
                'FG2_PCT': 114 / 187,
                'FG3_PCT': 72 / 222,
                'EFG_PCT': (114 + 1.5 * 72) / 409,
                'OVERALL_FG2A': 707,
                'OVERALL_FG3A': 232,
                'OVERALL_FGA': 939,
                'FG2A_FREQUENCY': 187 / 939,
                'FG3A_FREQUENCY': 222 / 939,
                'FGA_FREQUENCY': 409 / 939,
                'FREQUENCY_OF_FG2A': 187 / 707,
                'FREQUENCY_OF_FG3A': 222 / 232,
            }
    assert league_totals == {
        'EFG_PCT': (13285 + 1.5 * 16175) / (24199 + 44439),
        'FG2A': 24199,
        'FG2M': 13285,
        'FG2_PCT': 13285 / 24199,
        'FG3A': 44439,
        'FG3M': 16175,
        'FG3_PCT': 16175 / 44439,
        'FGA': 68638,
        'FGM': 29460,
        'OVERALL_FG2A': 86795,
        'OVERALL_FG3A': 53065,
        'OVERALL_FGA': 139860,
        'FG2A_FREQUENCY': 24199 / 139860,
        'FG3A_FREQUENCY': 44439 / 139860,
        'FGA_FREQUENCY': 68638 / 139860,
        'FREQUENCY_OF_FG2A': 24199 / 86795,
        'FREQUENCY_OF_FG3A': 44439 / 53065,
    }


@responses.activate
def test_generate_tracking_shot_game_logs():
    with open('tests/data/scoreboard_response.json') as f:
        scoreboard_response = json.loads(f.read())
    scoreboard_response['resultSets'][0]['rowSet'] = [['2020-02-02T00:00:00', 4, '0021900740', 3, 'Final', '20200202/CHITOR', 1610612761, 1610612741, '2019', 4, '     ', None, 'TSN1/4', 'NBCSCH', 'Q4       - ', 'Scotiabank Arena', 1]]
    scoreboard_response_url = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=02/02/2020'

    responses.add(responses.GET, scoreboard_response_url, json=scoreboard_response, status=200)

    with open('tests/data/game_boxscore_response.json') as f:
        game_response_json = json.loads(f.read())

    game_id = '0021900740'

    boxscore_url = 'https://stats.nba.com/stats/boxscoretraditionalv2'
    query_params = {
        'GameId': game_id,
        'StartPeriod': 0,
        'EndPeriod': 10,
        'RangeType': 2,
        'StartRange': 0,
        'EndRange': 55800
    }
    url = furl(boxscore_url).add(query_params).url

    responses.add(responses.GET, url, json=game_response_json, status=200)

    with open('tests/data/player_wide_open_single_date_response.json') as f:
        shots_response_json = json.loads(f.read())

    def_distance = '6+ Feet - Wide Open'
    date = '02/02/2020'

    shots_url = 'https://stats.nba.com/stats/leaguedashplayerptshot'
    shots_query_params = {
        'Season': '2019-20',
        'SeasonType': 'Regular Season',
        'DateFrom': date,
        'DateTo': date,
        'CloseDefDistRange': def_distance,
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }

    url = furl(shots_url).add(shots_query_params).url

    responses.add(responses.GET, url, json=shots_response_json, status=200)

    with open('tests/data/player_overall_response_for_date.json') as f:
        overall_response_json = json.loads(f.read())

    overall_query_params = {
        'Season': '2019-20',
        'SeasonType': 'Regular Season',
        'DateFrom': date,
        'DateTo': date,
        'CloseDefDistRange': '',
        'ShotClockRange': '',
        'ShotDistRange': '',
        'TouchTimeRange': '',
        'DribbleRange': '',
        'GeneralRange': 'Overall',
        'PerMode': 'Totals',
        'LeagueID': '00',
    }
    overall_url = furl(shots_url).add(overall_query_params).url

    responses.add(responses.GET, overall_url, json=overall_response_json, status=200)

    game_logs = tracking_shots.generate_tracking_shot_game_logs('player', date, date, close_def_dists=[def_distance])
    assert len(game_logs) == 17
    for game_log in game_logs:
        if game_log['PLAYER_ID'] == 1627832:
            assert game_log == {
                'PLAYER_ID': 1627832,
                'PLAYER_NAME': 'Fred VanVleet',
                'PLAYER_LAST_TEAM_ID': 1610612761,
                'PLAYER_LAST_TEAM_ABBREVIATION': 'TOR',
                'FGM': 2,
                'FGA': 6,
                'FG2M': 0,
                'FG2A': 0,
                'FG3M': 2,
                'FG3A': 6,
                'FG2_PCT': 0,
                'FG3_PCT': 2 / 6,
                'EFG_PCT': 0.5,
                'TEAM_ID': 1610612761,
                'GAME_ID': '0021900740',
                'OPPONENT_TEAM_ID': 1610612741,
                'OVERALL_FG2A': 5,
                'OVERALL_FG3A': 6,
                'OVERALL_FGA': 11,
                'FG2A_FREQUENCY': 0,
                'FG3A_FREQUENCY': 6 / 11,
                'FGA_FREQUENCY': 6 / 11,
                'FREQUENCY_OF_FG2A': 0,
                'FREQUENCY_OF_FG3A': 6 / 6,
            }


@responses.activate
def test_generate_tracking_shot_game_logs_for_date_with_no_games():
    with open('tests/data/scoreboard_response.json') as f:
        scoreboard_response = json.loads(f.read())
    scoreboard_response['resultSets'][0]['rowSet'] = []
    scoreboard_response_url = 'https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=02/02/2020'

    responses.add(responses.GET, scoreboard_response_url, json=scoreboard_response, status=200)

    def_distance = '6+ Feet - Wide Open'
    date = '02/02/2020'

    game_logs = tracking_shots.generate_tracking_shot_game_logs('player', date, date, close_def_dists=[def_distance])
    assert game_logs == []


def test_sum_tracking_shot_totals_player():
    items1 = [
        {'PLAYER_ID': 201954, 'PLAYER_NAME': 'Darren Collison', 'PLAYER_LAST_TEAM_ID': 1610612754, 'PLAYER_LAST_TEAM_ABBREVIATION': 'IND', 'AGE': 31.0, 'GP': 76, 'G': 55, 'FGA_FREQUENCY': 0.147, 'FGM': 46, 'FGA': 97, 'FG_PCT': 0.474, 'EFG_PCT': 0.665, 'FG2A_FREQUENCY': 0.026, 'FG2M': 9, 'FG2A': 17, 'FG2_PCT': 0.529, 'FG3A_FREQUENCY': 0.121, 'FG3M': 37, 'FG3A': 80, 'FG3_PCT': 0.463, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
        {'PLAYER_ID': 203081, 'PLAYER_NAME': 'Damian Lillard', 'PLAYER_LAST_TEAM_ID': 1610612757, 'PLAYER_LAST_TEAM_ABBREVIATION': 'POR', 'AGE': 28.0, 'GP': 80, 'G': 58, 'FGA_FREQUENCY': 0.063, 'FGM': 41, 'FGA': 97, 'FG_PCT': 0.423, 'EFG_PCT': 0.608, 'FG2A_FREQUENCY': 0.007, 'FG2M': 5, 'FG2A': 10, 'FG2_PCT': 0.5, 'FG3A_FREQUENCY': 0.057, 'FG3M': 36, 'FG3A': 87, 'FG3_PCT': 0.414, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
        {'PLAYER_ID': 1629016, 'PLAYER_NAME': 'Omari Spellman', 'PLAYER_LAST_TEAM_ID': 1610612737, 'PLAYER_LAST_TEAM_ABBREVIATION': 'ATL', 'AGE': 21.0, 'GP': 46, 'G': 37, 'FGA_FREQUENCY': 0.398, 'FGM': 32, 'FGA': 97, 'FG_PCT': 0.33, 'EFG_PCT': 0.495, 'FG2A_FREQUENCY': 0.008, 'FG2M': 0, 'FG2A': 2, 'FG2_PCT': 0.0, 'FG3A_FREQUENCY': 0.389, 'FG3M': 32, 'FG3A': 95, 'FG3_PCT': 0.337, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
        {'PLAYER_ID': 202681, 'PLAYER_NAME': 'Kyrie Irving', 'PLAYER_LAST_TEAM_ID': 1610612738, 'PLAYER_LAST_TEAM_ABBREVIATION': 'BOS', 'AGE': 27.0, 'GP': 67, 'G': 50, 'FGA_FREQUENCY': 0.077, 'FGM': 52, 'FGA': 96, 'FG_PCT': 0.542, 'EFG_PCT': 0.792, 'FG2A_FREQUENCY': 0.007, 'FG2M': 4, 'FG2A': 9, 'FG2_PCT': 0.444, 'FG3A_FREQUENCY': 0.07, 'FG3M': 48, 'FG3A': 87, 'FG3_PCT': 0.552, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
    ]
    items2 = [
        {'PLAYER_ID': 1626179, 'PLAYER_NAME': 'Terry Rozier', 'PLAYER_LAST_TEAM_ID': 1610612738, 'PLAYER_LAST_TEAM_ABBREVIATION': 'BOS', 'AGE': 25.0, 'GP': 79, 'G': 55, 'FGA_FREQUENCY': 0.144, 'FGM': 35, 'FGA': 96, 'FG_PCT': 0.365, 'EFG_PCT': 0.542, 'FG2A_FREQUENCY': 0.003, 'FG2M': 1, 'FG2A': 2, 'FG2_PCT': 0.5, 'FG3A_FREQUENCY': 0.141, 'FG3M': 34, 'FG3A': 94, 'FG3_PCT': 0.362, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
        {'PLAYER_ID': 203081, 'PLAYER_NAME': 'Damian Lillard', 'PLAYER_LAST_TEAM_ID': 1610612757, 'PLAYER_LAST_TEAM_ABBREVIATION': 'POR', 'AGE': 28.0, 'GP': 80, 'G': 55, 'FGA_FREQUENCY': 0.062, 'FGM': 39, 'FGA': 95, 'FG_PCT': 0.411, 'EFG_PCT': 0.595, 'FG2A_FREQUENCY': 0.007, 'FG2M': 4, 'FG2A': 11, 'FG2_PCT': 0.364, 'FG3A_FREQUENCY': 0.055, 'FG3M': 35, 'FG3A': 84, 'FG3_PCT': 0.417, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
        {'PLAYER_ID': 1628390, 'PLAYER_NAME': 'Terrance Ferguson', 'PLAYER_LAST_TEAM_ID': 1610612760, 'PLAYER_LAST_TEAM_ABBREVIATION': 'OKC', 'AGE': 21.0, 'GP': 73, 'G': 47, 'FGA_FREQUENCY': 0.225, 'FGM': 32, 'FGA': 95, 'FG_PCT': 0.337, 'EFG_PCT': 0.5, 'FG2A_FREQUENCY': 0.007, 'FG2M': 1, 'FG2A': 3, 'FG2_PCT': 0.333, 'FG3A_FREQUENCY': 0.217, 'FG3M': 31, 'FG3A': 92, 'FG3_PCT': 0.337, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
        {'PLAYER_ID': 1628470, 'PLAYER_NAME': 'Torrey Craig', 'PLAYER_LAST_TEAM_ID': 1610612743, 'PLAYER_LAST_TEAM_ABBREVIATION': 'DEN', 'AGE': 28.0, 'GP': 75, 'G': 55, 'FGA_FREQUENCY': 0.262, 'FGM': 29, 'FGA': 95, 'FG_PCT': 0.305, 'EFG_PCT': 0.458, 'FG2A_FREQUENCY': 0.0, 'FG2M': 0, 'FG2A': 0, 'FG2_PCT': None, 'FG3A_FREQUENCY': 0.262, 'FG3M': 29, 'FG3A': 95, 'FG3_PCT': 0.305, 'OVERALL_FGA': 324, 'OVERALL_FG2A': 224, 'OVERALL_FG3A': 100},
    ]
    totals = tracking_shots.sum_tracking_shot_totals('player', items1, items2)
    assert len(totals) == 7
    for player in totals:
        if player['PLAYER_ID'] == 203081:
            assert player == {
                'PLAYER_ID': 203081,
                'PLAYER_NAME': 'Damian Lillard',
                'PLAYER_LAST_TEAM_ID': 1610612757,
                'PLAYER_LAST_TEAM_ABBREVIATION': 'POR',
                'FGM': 80,
                'FGA': 192,
                'EFG_PCT': (9 + 1.5 * 71) / 192,
                'FG2M': 9,
                'FG2A': 21,
                'FG2_PCT': 9 / 21,
                'FG3M': 71,
                'FG3A': 171,
                'FG3_PCT': 71 / 171,
                'OVERALL_FG2A': 448,
                'OVERALL_FG3A': 200,
                'OVERALL_FGA': 648,
                'FG2A_FREQUENCY': 21 / 648,
                'FG3A_FREQUENCY': 171 / 648,
                'FGA_FREQUENCY': 192 / 648,
                'FREQUENCY_OF_FG2A': 21 / 448,
                'FREQUENCY_OF_FG3A': 171 / 200,
            }


def test_sum_tracking_shot_totals_team():
    items1 = [
        {'TEAM_ID': 1610612737, 'TEAM_NAME': 'Atlanta Hawks', 'TEAM_ABBREVIATION': 'ATL', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.2, 'FGM': 574, 'FGA': 1502, 'FG_PCT': 0.382, 'EFG_PCT': 0.568, 'FG2A_FREQUENCY': 0.007, 'FG2M': 16, 'FG2A': 49, 'FG2_PCT': 0.327, 'FG3A_FREQUENCY': 0.193, 'FG3M': 558, 'FG3A': 1453, 'FG3_PCT': 0.384, 'OVERALL_FGA': 6324, 'OVERALL_FG2A': 3224, 'OVERALL_FG3A': 3100},
        {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'TEAM_ABBREVIATION': 'TOR', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.204, 'FGM': 632, 'FGA': 1490, 'FG_PCT': 0.424, 'EFG_PCT': 0.607, 'FG2A_FREQUENCY': 0.021, 'FG2M': 86, 'FG2A': 153, 'FG2_PCT': 0.562, 'FG3A_FREQUENCY': 0.183, 'FG3M': 546, 'FG3A': 1337, 'FG3_PCT': 0.408, 'OVERALL_FGA': 6326, 'OVERALL_FG2A': 3225, 'OVERALL_FG3A': 3101},
        {'TEAM_ID': 1610612749, 'TEAM_NAME': 'Milwaukee Bucks', 'TEAM_ABBREVIATION': 'MIL', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.197, 'FGM': 539, 'FGA': 1469, 'FG_PCT': 0.367, 'EFG_PCT': 0.545, 'FG2A_FREQUENCY': 0.004, 'FG2M': 16, 'FG2A': 30, 'FG2_PCT': 0.533, 'FG3A_FREQUENCY': 0.193, 'FG3M': 523, 'FG3A': 1439, 'FG3_PCT': 0.363, 'OVERALL_FGA': 6328, 'OVERALL_FG2A': 3226, 'OVERALL_FG3A': 3102},
    ]
    items2 = [
        {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'TEAM_ABBREVIATION': 'TOR', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.099, 'FGM': 280, 'FGA': 722, 'FG_PCT': 0.388, 'EFG_PCT': 0.528, 'FG2A_FREQUENCY': 0.023, 'FG2M': 78, 'FG2A': 167, 'FG2_PCT': 0.467, 'FG3A_FREQUENCY': 0.076, 'FG3M': 202, 'FG3A': 555, 'FG3_PCT': 0.364, 'OVERALL_FGA': 6324, 'OVERALL_FG2A': 3224, 'OVERALL_FG3A': 3100},
        {'TEAM_ID': 1610612765, 'TEAM_NAME': 'Detroit Pistons', 'TEAM_ABBREVIATION': 'DET', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.098, 'FGM': 240, 'FGA': 712, 'FG_PCT': 0.337, 'EFG_PCT': 0.489, 'FG2A_FREQUENCY': 0.007, 'FG2M': 23, 'FG2A': 50, 'FG2_PCT': 0.46, 'FG3A_FREQUENCY': 0.091, 'FG3M': 217, 'FG3A': 662, 'FG3_PCT': 0.328, 'OVERALL_FGA': 6325, 'OVERALL_FG2A': 3325, 'OVERALL_FG3A': 3000},
        {'TEAM_ID': 1610612760, 'TEAM_NAME': 'Oklahoma City Thunder', 'TEAM_ABBREVIATION': 'OKC', 'GP': 81, 'G': 81, 'FGA_FREQUENCY': 0.089, 'FGM': 226, 'FGA': 674, 'FG_PCT': 0.335, 'EFG_PCT': 0.469, 'FG2A_FREQUENCY': 0.014, 'FG2M': 46, 'FG2A': 105, 'FG2_PCT': 0.438, 'FG3A_FREQUENCY': 0.075, 'FG3M': 180, 'FG3A': 569, 'FG3_PCT': 0.316, 'OVERALL_FGA': 6326, 'OVERALL_FG2A': 3426, 'OVERALL_FG3A': 2900},
    ]
    totals = tracking_shots.sum_tracking_shot_totals('team', items1, items2)
    assert len(totals) == 5
    for player in totals:
        if player['TEAM_ID'] == 1610612761:
            assert player == {
                'TEAM_ID': 1610612761,
                'TEAM_NAME': 'Toronto Raptors',
                'TEAM_ABBREVIATION': 'TOR',
                'FGM': 912,
                'FGA': 2212,
                'EFG_PCT': (164 + 1.5 * 748) / 2212,
                'FG2M': 164,
                'FG2A': 320,
                'FG2_PCT': 164 / 320,
                'FG3M': 748,
                'FG3A': 1892,
                'FG3_PCT': 748 / 1892,
                'OVERALL_FG2A': 6449,
                'OVERALL_FG3A': 6201,
                'OVERALL_FGA': 12650,
                'FG2A_FREQUENCY': 320 / 12650,
                'FG3A_FREQUENCY': 1892 / 12650,
                'FGA_FREQUENCY': 2212 / 12650,
                'FREQUENCY_OF_FG2A': 320 / 6449,
                'FREQUENCY_OF_FG3A': 1892 / 6201,
            }


def test_sum_tracking_shot_totals_league():
    items1 = [
        {'TEAM_ID': 1610612737, 'TEAM_NAME': 'Atlanta Hawks', 'TEAM_ABBREVIATION': 'ATL', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.2, 'FGM': 574, 'FGA': 1502, 'FG_PCT': 0.382, 'EFG_PCT': 0.568, 'FG2A_FREQUENCY': 0.007, 'FG2M': 16, 'FG2A': 49, 'FG2_PCT': 0.327, 'FG3A_FREQUENCY': 0.193, 'FG3M': 558, 'FG3A': 1453, 'FG3_PCT': 0.384, 'OVERALL_FGA': 6324, 'OVERALL_FG2A': 3224, 'OVERALL_FG3A': 3100},
        {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'TEAM_ABBREVIATION': 'TOR', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.204, 'FGM': 632, 'FGA': 1490, 'FG_PCT': 0.424, 'EFG_PCT': 0.607, 'FG2A_FREQUENCY': 0.021, 'FG2M': 86, 'FG2A': 153, 'FG2_PCT': 0.562, 'FG3A_FREQUENCY': 0.183, 'FG3M': 546, 'FG3A': 1337, 'FG3_PCT': 0.408, 'OVERALL_FGA': 6326, 'OVERALL_FG2A': 3225, 'OVERALL_FG3A': 3101},
        {'TEAM_ID': 1610612749, 'TEAM_NAME': 'Milwaukee Bucks', 'TEAM_ABBREVIATION': 'MIL', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.197, 'FGM': 539, 'FGA': 1469, 'FG_PCT': 0.367, 'EFG_PCT': 0.545, 'FG2A_FREQUENCY': 0.004, 'FG2M': 16, 'FG2A': 30, 'FG2_PCT': 0.533, 'FG3A_FREQUENCY': 0.193, 'FG3M': 523, 'FG3A': 1439, 'FG3_PCT': 0.363, 'OVERALL_FGA': 6328, 'OVERALL_FG2A': 3226, 'OVERALL_FG3A': 3102},
    ]
    items2 = [
        {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'TEAM_ABBREVIATION': 'TOR', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.099, 'FGM': 280, 'FGA': 722, 'FG_PCT': 0.388, 'EFG_PCT': 0.528, 'FG2A_FREQUENCY': 0.023, 'FG2M': 78, 'FG2A': 167, 'FG2_PCT': 0.467, 'FG3A_FREQUENCY': 0.076, 'FG3M': 202, 'FG3A': 555, 'FG3_PCT': 0.364, 'OVERALL_FGA': 6324, 'OVERALL_FG2A': 3224, 'OVERALL_FG3A': 3100},
        {'TEAM_ID': 1610612765, 'TEAM_NAME': 'Detroit Pistons', 'TEAM_ABBREVIATION': 'DET', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.098, 'FGM': 240, 'FGA': 712, 'FG_PCT': 0.337, 'EFG_PCT': 0.489, 'FG2A_FREQUENCY': 0.007, 'FG2M': 23, 'FG2A': 50, 'FG2_PCT': 0.46, 'FG3A_FREQUENCY': 0.091, 'FG3M': 217, 'FG3A': 662, 'FG3_PCT': 0.328, 'OVERALL_FGA': 6325, 'OVERALL_FG2A': 3325, 'OVERALL_FG3A': 3000},
        {'TEAM_ID': 1610612760, 'TEAM_NAME': 'Oklahoma City Thunder', 'TEAM_ABBREVIATION': 'OKC', 'GP': 81, 'G': 81, 'FGA_FREQUENCY': 0.089, 'FGM': 226, 'FGA': 674, 'FG_PCT': 0.335, 'EFG_PCT': 0.469, 'FG2A_FREQUENCY': 0.014, 'FG2M': 46, 'FG2A': 105, 'FG2_PCT': 0.438, 'FG3A_FREQUENCY': 0.075, 'FG3M': 180, 'FG3A': 569, 'FG3_PCT': 0.316, 'OVERALL_FGA': 6326, 'OVERALL_FG2A': 3426, 'OVERALL_FG3A': 2900},
    ]
    totals = tracking_shots.sum_tracking_shot_totals('league', items1, items2)
    assert totals == {
        'FGM': 2491,
        'FGA': 6569,
        'EFG_PCT': (265 + 1.5 * 2226) / 6569,
        'FG2M': 265,
        'FG2A': 554,
        'FG2_PCT': 265 / 554,
        'FG3M': 2226,
        'FG3A': 6015,
        'FG3_PCT': 2226 / 6015,
        'OVERALL_FG2A': 19650,
        'OVERALL_FG3A': 18303,
        'OVERALL_FGA': 37953,
        'FG2A_FREQUENCY': 554 / 37953,
        'FG3A_FREQUENCY': 6015 / 37953,
        'FGA_FREQUENCY': 6569 / 37953,
        'FREQUENCY_OF_FG2A': 554 / 19650,
        'FREQUENCY_OF_FG3A': 6015 / 18303,
    }


def test_sum_tracking_shot_totals_invalid_entity_type():
    items1 = [
        {'TEAM_ID': 1610612737, 'TEAM_NAME': 'Atlanta Hawks', 'TEAM_ABBREVIATION': 'ATL', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.2, 'FGM': 574, 'FGA': 1502, 'FG_PCT': 0.382, 'EFG_PCT': 0.568, 'FG2A_FREQUENCY': 0.007, 'FG2M': 16, 'FG2A': 49, 'FG2_PCT': 0.327, 'FG3A_FREQUENCY': 0.193, 'FG3M': 558, 'FG3A': 1453, 'FG3_PCT': 0.384},
        {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'TEAM_ABBREVIATION': 'TOR', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.204, 'FGM': 632, 'FGA': 1490, 'FG_PCT': 0.424, 'EFG_PCT': 0.607, 'FG2A_FREQUENCY': 0.021, 'FG2M': 86, 'FG2A': 153, 'FG2_PCT': 0.562, 'FG3A_FREQUENCY': 0.183, 'FG3M': 546, 'FG3A': 1337, 'FG3_PCT': 0.408},
        {'TEAM_ID': 1610612749, 'TEAM_NAME': 'Milwaukee Bucks', 'TEAM_ABBREVIATION': 'MIL', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.197, 'FGM': 539, 'FGA': 1469, 'FG_PCT': 0.367, 'EFG_PCT': 0.545, 'FG2A_FREQUENCY': 0.004, 'FG2M': 16, 'FG2A': 30, 'FG2_PCT': 0.533, 'FG3A_FREQUENCY': 0.193, 'FG3M': 523, 'FG3A': 1439, 'FG3_PCT': 0.363},
    ]
    items2 = [
        {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'TEAM_ABBREVIATION': 'TOR', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.099, 'FGM': 280, 'FGA': 722, 'FG_PCT': 0.388, 'EFG_PCT': 0.528, 'FG2A_FREQUENCY': 0.023, 'FG2M': 78, 'FG2A': 167, 'FG2_PCT': 0.467, 'FG3A_FREQUENCY': 0.076, 'FG3M': 202, 'FG3A': 555, 'FG3_PCT': 0.364},
        {'TEAM_ID': 1610612765, 'TEAM_NAME': 'Detroit Pistons', 'TEAM_ABBREVIATION': 'DET', 'GP': 82, 'G': 82, 'FGA_FREQUENCY': 0.098, 'FGM': 240, 'FGA': 712, 'FG_PCT': 0.337, 'EFG_PCT': 0.489, 'FG2A_FREQUENCY': 0.007, 'FG2M': 23, 'FG2A': 50, 'FG2_PCT': 0.46, 'FG3A_FREQUENCY': 0.091, 'FG3M': 217, 'FG3A': 662, 'FG3_PCT': 0.328},
        {'TEAM_ID': 1610612760, 'TEAM_NAME': 'Oklahoma City Thunder', 'TEAM_ABBREVIATION': 'OKC', 'GP': 81, 'G': 81, 'FGA_FREQUENCY': 0.089, 'FGM': 226, 'FGA': 674, 'FG_PCT': 0.335, 'EFG_PCT': 0.469, 'FG2A_FREQUENCY': 0.014, 'FG2M': 46, 'FG2A': 105, 'FG2_PCT': 0.438, 'FG3A_FREQUENCY': 0.075, 'FG3M': 180, 'FG3A': 569, 'FG3_PCT': 0.316},
    ]
    totals = tracking_shots.sum_tracking_shot_totals('league_totals', items1, items2)
    assert totals is None
