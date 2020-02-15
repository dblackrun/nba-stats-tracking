import time

from dateutil.rrule import rrule, DAILY
from datetime import datetime

from nba_stats_tracking import utils


def get_tracking_shots_response(entity_type, season, season_type, **kwargs):
    """
    entity_type - string, player, team, opponent
    season - string, ex 2019-20
    season_type - string, Regular Season or Playoffs

    possible kwargs:
    date_from - string, optional, format - MM/DD/YYYY
    date_to - string, optional, format - MM/DD/YYYY
    close_def_dist - string, options are: '', '0-2 Feet - Very Tight','2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    shot_clock - string, options are: '', '24-22', '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late', 'ShotClock Off'
    shot_dist - string, options are: '', '>=10.0'
    touch_time - string, options are: '', 'Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    dribbles - string, options are: '', '0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    general_range - string, options are: 'Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    period - int
    location - string, options are: 'Home' and 'Road'

    returns dict
    """
    if entity_type == 'team':
        url = 'https://stats.nba.com/stats/leaguedashteamptshot'
    elif entity_type == 'player':
        url = 'https://stats.nba.com/stats/leaguedashplayerptshot'
    elif entity_type == 'opponent':
        url = 'https://stats.nba.com/stats/leaguedashoppptshot'
    else:
        return None

    parameters = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': kwargs.get('date_from', ''),
        'DateTo': kwargs.get('date_to', ''),
        'CloseDefDistRange': kwargs.get('close_def_dist', ''),
        'ShotClockRange': kwargs.get('shot_clock', ''),
        'ShotDistRange': kwargs.get('shot_dist', ''),
        'TouchTimeRange': kwargs.get('touch_time', ''),
        'DribbleRange': kwargs.get('dribbles', ''),
        'GeneralRange': kwargs.get('general_range', 'Overall'),
        'PerMode': 'Totals',
        'LeagueID': '00',
        'Period': kwargs.get('period', ''),
        'Location': kwargs.get('location', ''),
    }
    return utils.get_json_response(url, parameters)


def get_tracking_shot_stats(entity_type, seasons, season_types, **kwargs):
    """
    entity_type - string, player, team, opponent
    seasons - list, ex season '2019-20'
    season_types - list, season types are 'Regular Season' or 'Playoffs'

    possible kwargs:
    close_def_dists - list, options are: '', '0-2 Feet - Very Tight','2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    shot_clocks - list, options are: '', '24-22', '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late', 'ShotClock Off'
    shot_dists - list, options are: '', '>=10.0'
    touch_times - list, options are: '', 'Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    dribble_ranges - list, options are: '', '0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    general_ranges - list, options are: 'Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    date_from - string, format - MM/DD/YYYY
    date_to - string, format - MM/DD/YYYY
    periods - list of ints
    location - string, 'Home' or 'Road'

    returns list of dicts
    """
    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            season_stats = []
            for close_def in kwargs.get('close_def_dists', ['']):
                for clock in kwargs.get('shot_clocks', ['']):
                    for dist in kwargs.get('shot_dists', ['']):
                        for touch in kwargs.get('touch_times', ['']):
                            for dribbles in kwargs.get('dribble_ranges', ['']):
                                for general in kwargs.get('general_ranges', ['Overall']):
                                    for period in kwargs.get('periods', ['']):
                                        time.sleep(2)
                                        response_json = get_tracking_shots_response(
                                            entity_type,
                                            season,
                                            season_type,
                                            close_def_dist=close_def,
                                            shot_clock=clock,
                                            shot_dist=dist,
                                            touch_time=touch,
                                            dribbles=dribbles,
                                            general_range=general,
                                            date_from=kwargs.get('date_from', ''),
                                            date_to=kwargs.get('date_to', ''),
                                            period=period,
                                            location=kwargs.get('location', ''),
                                        )
                                        filter_stats = utils.make_array_of_dicts_from_response_json(response_json, 0)
                                        season_stats.append(filter_stats)
            stats = sum_tracking_shot_totals(entity_type, *season_stats)
            entity_id_key = 'PLAYER_ID' if entity_type == 'player' else 'TEAM_ID'
            overall_response_json = get_tracking_shots_response(entity_type, season, season_type, general_range='Overall', date_from=kwargs.get('date_from', ''), date_to=kwargs.get('date_to', ''))
            overall_stats = utils.make_array_of_dicts_from_response_json(overall_response_json, 0)
            overall_stats_by_entity = {stat[entity_id_key]: {'FGA': stat['FGA'], 'FG2A': stat['FG2A'], 'FG3A': stat['FG3A']} for stat in overall_stats}
            for stat in stats:
                entity_id = stat[entity_id_key]
                stat['SEASON'] = f'{season} {season_type}'
                stat['OVERALL_FGA'] = overall_stats_by_entity[entity_id]['FGA']
                stat['OVERALL_FG2A'] = overall_stats_by_entity[entity_id]['FG2A']
                stat['OVERALL_FG3A'] = overall_stats_by_entity[entity_id]['FG3A']
                stat['FGA_FREQUENCY'] = stat['FGA'] / stat['OVERALL_FGA'] if stat['OVERALL_FGA'] != 0 else 0
                stat['FG2A_FREQUENCY'] = stat['FG2A'] / stat['OVERALL_FGA'] if stat['OVERALL_FGA'] != 0 else 0
                stat['FG3A_FREQUENCY'] = stat['FG3A'] / stat['OVERALL_FGA'] if stat['OVERALL_FGA'] != 0 else 0
                stat['FREQUENCY_OF_FG2A'] = stat['FG2A'] / stat['OVERALL_FG2A'] if stat['OVERALL_FG2A'] != 0 else 0
                stat['FREQUENCY_OF_FG3A'] = stat['FG3A'] / stat['OVERALL_FG3A'] if stat['OVERALL_FG3A'] != 0 else 0
            all_season_stats += stats
    return all_season_stats


def aggregate_full_season_tracking_shot_stats_for_seasons(entity_type, seasons, season_types, **kwargs):
    """
    entity_type - string, player, team, opponent
    seasons - list, ex season '2019-20'
    season_types - list, season types are 'Regular Season' or 'Playoffs'

    possible kwargs:
    close_def_dists - list, options are: '', '0-2 Feet - Very Tight','2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    shot_clocks - list, options are: '', '24-22', '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late', 'ShotClock Off'
    shot_dists - list, options are: '', '>=10.0'
    touch_times - list, options are: '', 'Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    dribble_ranges - list, options are: '', '0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    general_ranges - list, options are: 'Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    periods - list of ints
    location - string, 'Home' or 'Road'

    returns list of dicts for stats for each team or player and dict with league totals
    """
    stats_by_season = get_tracking_shot_stats(entity_type, seasons, season_types, **kwargs)

    stats = sum_tracking_shot_totals(entity_type, stats_by_season)
    league_totals = sum_tracking_shot_totals('league', stats_by_season)
    return stats, league_totals


def generate_tracking_shot_game_logs(entity_type, date_from, date_to, **kwargs):
    """
    entity_type - string, player, team, opponent
    date_from - string, format - MM/DD/YYYY
    date_to - string, format - MM/DD/YYYY

    possible kwargs:
    close_def_dists - list, options are: '', '0-2 Feet - Very Tight','2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    shot_clocks - list, options are: '', '24-22', '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late', 'ShotClock Off'
    shot_dists - list, options are: '', '>=10.0'
    touch_times - list, options are: '', 'Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    dribble_ranges - list, options are: '', '0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    general_ranges - list, options are: 'Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    periods - list of ints
    location - string, 'Home' or 'Road'

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

        tracking_shots_data = get_tracking_shot_stats(entity_type, [season], [season_type], date_from=date, date_to=date, **kwargs)
        tracking_shots_game_logs = sum_tracking_shot_totals(entity_type, tracking_shots_data)
        if entity_type == 'player':
            # need to add team id for player because results only have PLAYER_LAST_TEAM_ID, which may not be the team for which they played the game
            player_id_team_id_map = utils.get_player_team_map_for_date(date)
            for game_log in tracking_shots_game_logs:
                game_log['TEAM_ID'] = player_id_team_id_map[game_log['PLAYER_ID']]
        for game_log in tracking_shots_game_logs:
            game_log['GAME_ID'] = team_id_game_id_map[game_log['TEAM_ID']]
            game_log['OPPONENT_TEAM_ID'] = team_id_opponent_team_id_map[game_log['TEAM_ID']]
        game_logs += tracking_shots_game_logs
    return game_logs


def sum_tracking_shot_totals(entity_type, *args):
    """
    entity_type - string, player, team, opponent or league

    args - list of dicts to be summed up
    """
    if entity_type == 'player':
        entity_key = 'PLAYER_ID'
    elif entity_type == 'team' or entity_type == 'opponent':
        entity_key = 'TEAM_ID'
    elif entity_type == 'league':
        totals_dict = {
            'FGM': 0,
            'FGA': 0,
            'FG2M': 0,
            'FG2A': 0,
            'FG3M': 0,
            'FG3A': 0,
            'OVERALL_FGA': 0,
            'OVERALL_FG2A': 0,
            'OVERALL_FG3A': 0,
        }
        for items in args:
            for item in items:
                totals_dict = add_to_tracking_shot_totals(totals_dict, item)
        return totals_dict
    else:
        return None
    totals_dict = {}
    for items in args:
        for item in items:
            entity_id = item[entity_key]
            if entity_id not in totals_dict.keys():
                if entity_type == 'player':
                    totals_dict[entity_id] = {
                        'PLAYER_ID': item['PLAYER_ID'],
                        'PLAYER_NAME': item['PLAYER_NAME'],
                        'PLAYER_LAST_TEAM_ID': item['PLAYER_LAST_TEAM_ID'],
                        'PLAYER_LAST_TEAM_ABBREVIATION': item['PLAYER_LAST_TEAM_ABBREVIATION'],
                        'FGM': 0,
                        'FGA': 0,
                        'FG2M': 0,
                        'FG2A': 0,
                        'FG3M': 0,
                        'FG3A': 0,
                        'OVERALL_FGA': 0,
                        'OVERALL_FG2A': 0,
                        'OVERALL_FG3A': 0,
                    }
                elif entity_type == 'team' or entity_type == 'opponent':
                    totals_dict[entity_id] = {
                        'TEAM_ID': item['TEAM_ID'],
                        'TEAM_NAME': item['TEAM_NAME'],
                        'TEAM_ABBREVIATION': item['TEAM_ABBREVIATION'],
                        'FGM': 0,
                        'FGA': 0,
                        'FG2M': 0,
                        'FG2A': 0,
                        'FG3M': 0,
                        'FG3A': 0,
                        'OVERALL_FGA': 0,
                        'OVERALL_FG2A': 0,
                        'OVERALL_FG3A': 0,
                    }
            totals_dict[entity_id] = add_to_tracking_shot_totals(totals_dict[entity_id], item)

    return list(totals_dict.values())


def add_to_tracking_shot_totals(totals, item):
    """
    adds shot totals from item to totals dict and updates percentages

    totals - dict
    item - dict
    """
    totals['FGM'] += item['FGM']
    totals['FGA'] += item['FGA']
    totals['FG2M'] += item['FG2M']
    totals['FG2A'] += item['FG2A']
    totals['FG3M'] += item['FG3M']
    totals['FG3A'] += item['FG3A']
    totals['OVERALL_FGA'] += item.get('OVERALL_FGA', 0)
    totals['OVERALL_FG2A'] += item.get('OVERALL_FG2A', 0)
    totals['OVERALL_FG3A'] += item.get('OVERALL_FG3A', 0)
    fg2a = totals['FG2A']
    fg2m = totals['FG2M']
    fg3a = totals['FG3A']
    fg3m = totals['FG3M']
    totals['FG2_PCT'] = fg2m / fg2a if fg2a != 0 else 0
    totals['FG3_PCT'] = fg3m / fg3a if fg3a != 0 else 0
    totals['EFG_PCT'] = (1.5 * fg3m + fg2m) / (fg3a + fg2a) if (fg3a + fg2a) != 0 else 0
    totals['FGA_FREQUENCY'] = totals['FGA'] / totals['OVERALL_FGA'] if totals['OVERALL_FGA'] != 0 else 0
    totals['FG2A_FREQUENCY'] = totals['FG2A'] / totals['OVERALL_FGA'] if totals['OVERALL_FGA'] != 0 else 0
    totals['FG3A_FREQUENCY'] = totals['FG3A'] / totals['OVERALL_FGA'] if totals['OVERALL_FGA'] != 0 else 0
    totals['FREQUENCY_OF_FG2A'] = totals['FG2A'] / totals['OVERALL_FG2A'] if totals['OVERALL_FG2A'] != 0 else 0
    totals['FREQUENCY_OF_FG3A'] = totals['FG3A'] / totals['OVERALL_FG3A'] if totals['OVERALL_FG3A'] != 0 else 0

    return totals
