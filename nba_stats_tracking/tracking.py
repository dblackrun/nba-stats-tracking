import time

from dateutil.rrule import rrule, DAILY
from datetime import datetime

from nba_stats_tracking import utils


def get_tracking_response_json_for_stat_measure(stat_measure, season, season_type, entity_type, **kwargs):
    """
    stat_measure - string, options: 'Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch'
    season - string, ex '2019-20'
    season_type - string, 'Regular Season' or 'Playoffs'
    entity_type - string, 'player' or 'team'

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY
    opponent_team_id - int, optional, default is 0, which gets all teams

    returns dict
    """
    url = 'https://stats.nba.com/stats/leaguedashptstats'

    parameters = {
        'PlayerOrTeam': entity_type.title(),
        'PtMeasureType': stat_measure,
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': kwargs.get('date_from', ''),
        'DateTo': kwargs.get('date_to', ''),
        'GameScope': '',
        'LastNGames': 0,
        'LeagueID': '00',
        'Location': '',
        'Month': 0,
        'OpponentTeamID': kwargs.get('opponent_team_id', 0),
        'Outcome': '',
        'PerMode': 'Totals',
        'PlayerExperience': '',
        'PlayerPosition': '',
        'SeasonSegment': '',
        'StarterBench': '',
        'VsConference': '',
        'VsDivision': '',
    }

    return utils.get_json_response(url, parameters)


def get_tracking_stats(stat_measure, seasons, season_types, entity_type, **kwargs):
    """
    stat_measure - string, options: 'Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch'
    seasons - list, ex season '2019-20'
    season_types - list, season types are 'Regular Season' or 'Playoffs'
    entity_type - string, 'player' or 'team'

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY
    opponent_team_id - int, optional, default is 0, which gets all teams

    returns list of dicts
    """
    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            time.sleep(2)
            response_json = get_tracking_response_json_for_stat_measure(stat_measure, season, season_type, entity_type, **kwargs)
            stats = utils.make_array_of_dicts_from_response_json(response_json, 0)
            for stat in stats:
                stat['SEASON'] = f'{season} {season_type}'
            all_season_stats += stats
    return all_season_stats


def aggregate_full_season_tracking_stats_for_seasons(stat_measure, seasons, season_types, entity_type, **kwargs):
    """
    stat_measure - string, options: 'Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch'
    seasons - list, ex season '2019-20'
    season_types - list, season types are 'Regular Season' or 'Playoffs'
    entity_type - string, 'player' or 'team'

    possible kwargs:
    opponent_team_id - int, optional, default is 0, which gets all teams

    returns list of dicts for stats for each team or player and dict with league totals
    """
    stats_by_season = get_tracking_stats(stat_measure, seasons, season_types, entity_type, **kwargs)

    stats = sum_tracking_totals(entity_type, stats_by_season)
    league_totals = sum_tracking_totals('league', stats_by_season)
    return stats, league_totals


def generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to):
    """
    stat_measure - string, options: 'Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch'
    entity_type - string, player, team
    date_from - string, format - MM/DD/YYYY
    date_to - string, format - MM/DD/YYYY

    returns list of dicts
    """
    start_date = datetime.strptime(date_from, '%m/%d/%Y')
    end_date = datetime.strptime(date_to, '%m/%d/%Y')
    game_logs = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        date = dt.strftime('%m/%d/%Y')
        team_id_game_id_map, team_id_opponent_team_id_map = utils.get_team_id_maps_for_date(date)
        if len(team_id_game_id_map.values()) == 0:
            return game_logs

        date_game_id = list(team_id_game_id_map.values())[0]

        season = utils.get_season_from_game_id(date_game_id)
        season_type = utils.get_season_type_from_game_id(date_game_id)

        tracking_game_logs = get_tracking_stats(stat_measure, [season], [season_type], entity_type, date_from=date, date_to=date)
        if entity_type == 'player':
            # need to add team id for player because results only have last team id, which may not be the team for which they played the game
            player_id_team_id_map = utils.get_player_team_map_for_date(date)
            for game_log in tracking_game_logs:
                game_log['TEAM_ID'] = player_id_team_id_map[game_log['PLAYER_ID']]
        for game_log in tracking_game_logs:
            game_log['GAME_ID'] = team_id_game_id_map[game_log['TEAM_ID']]
            game_log['OPPONENT_TEAM_ID'] = team_id_opponent_team_id_map[game_log['TEAM_ID']]
        game_logs += tracking_game_logs
    return game_logs


def sum_tracking_totals(entity_type, *args):
    """
    entity_type - string, player, team or league

    args - list of dicts to be summed up
    """
    if entity_type == 'player':
        entity_key = 'PLAYER_ID'
    elif entity_type == 'team':
        entity_key = 'TEAM_ID'
    elif entity_type == 'league':
        totals_dict = {}
        for items in args:
            for item in items:
                totals_dict = add_to_tracking_totals(totals_dict, item)
        return totals_dict
    else:
        return []
    totals_dict = {}
    for items in args:
        for item in items:
            entity_id = item[entity_key]
            if entity_id not in totals_dict.keys():
                if entity_type == 'player':
                    totals_dict[entity_id] = {
                        'PLAYER_ID': item['PLAYER_ID'],
                        'PLAYER_NAME': item['PLAYER_NAME'],
                        'TEAM_ID': item['TEAM_ID'],
                        'TEAM_ABBREVIATION': item['TEAM_ABBREVIATION'],
                    }
                elif entity_type == 'team':
                    totals_dict[entity_id] = {
                        'TEAM_ID': item['TEAM_ID'],
                        'TEAM_NAME': item['TEAM_NAME'],
                        'TEAM_ABBREVIATION': item['TEAM_ABBREVIATION'],
                    }
            totals_dict[entity_id] = add_to_tracking_totals(totals_dict[entity_id], item)

    return list(totals_dict.values())


def add_to_tracking_totals(totals, item):
    """
    adds totals from item to totals dict

    totals - dict
    item - dict
    """
    for key, value in item.items():
        if (type(value) is int and key not in ['GP', 'W', 'L', 'TEAM_ID', 'PLAYER_ID']) or key in ['MIN', 'DIST_MILES', 'DIST_MILES_OFF', 'DIST_MILES_DEF', 'TIME_OF_POSS']:
            if value is not None:
                totals[key] = totals.get(key, 0) + value

    return totals
