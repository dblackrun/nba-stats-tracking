"""Module containing functions for accessing tracking shot stats"""

import time
import itertools

from dateutil.rrule import rrule, DAILY
from datetime import datetime

from nba_stats_tracking import utils


def get_tracking_shots_response(entity_type, season, season_type, **kwargs):
    """
    Makes API call to `NBA Advanced Stats <https://www.stats.nba.com/>`_ and returns JSON response

    :param str entity_type: Options are player, team or opponent
    :param str season: Format YYYY-YY ex 2019-20
    :param str season_type: Options are Regular Season or Playoffs or Play In
    :param str date_from: (optional) Format - MM/DD/YYYY
    :param str date_to: (optional) Format - MM/DD/YYYY
    :param str close_def_dist: (optional) Defaults to "". Options: '', '0-2 Feet - Very Tight',
        '2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    :param str shot_clock: (optional) - Defaults to "". Options: '', '24-22',
        '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late'
    :param str shot_dist: (optional) - Defaults to "". Options: '', '>=10.0'
    :param str touch_time: (optional) - Defaults to "". Options: '', 'Touch < 2 Seconds',
        'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    :param str dribbles: (optional) - Defaults to "". Options: '', '0 Dribbles', '1 Dribble',
        '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    :param str general_range: (optional) - Defaults to "Overall". Options: 'Overall',
        'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    :param int period: (optional) Only get stats for specific period
    :param str location: (optional) - Options: 'Home' or 'Road'
    :return: response json
    :rtype: dict
    """
    if entity_type == "team":
        url = "https://stats.nba.com/stats/leaguedashteamptshot"
    elif entity_type == "player":
        url = "https://stats.nba.com/stats/leaguedashplayerptshot"
    elif entity_type == "opponent":
        url = "https://stats.nba.com/stats/leaguedashoppptshot"
    else:
        return None

    parameters = {
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": kwargs.get("date_from", ""),
        "DateTo": kwargs.get("date_to", ""),
        "CloseDefDistRange": kwargs.get("close_def_dist", ""),
        "ShotClockRange": kwargs.get("shot_clock", ""),
        "ShotDistRange": kwargs.get("shot_dist", ""),
        "TouchTimeRange": kwargs.get("touch_time", ""),
        "DribbleRange": kwargs.get("dribbles", ""),
        "GeneralRange": kwargs.get("general_range", "Overall"),
        "PerMode": "Totals",
        "LeagueID": "00",
        "Period": kwargs.get("period", ""),
        "Location": kwargs.get("location", ""),
    }
    return utils.get_json_response(url, parameters)


def get_tracking_shot_stats(entity_type, seasons, season_types, **kwargs):
    """
    Gets tracking shot stats for filters

    :param str entity_type: Options are player, team or opponent
    :param list[str] seasons: List of seasons.Format YYYY-YY ex 2019-20
    :param list[str] season_types: List of season types. Options are Regular Season or Playoffs or Play In
    :param list[str] close_def_dists: (optional) Options: '', '0-2 Feet - Very Tight',
        '2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    :param list[str] shot_clocks: (optional) - Options: '', '24-22',
        '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late'
    :param list[str] shot_dists: (optional) - Options: '', '>=10.0'
    :param list[str] touch_times: (optional) - Options: '', 'Touch < 2 Seconds',
        'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    :param list[str] dribble_ranges: (optional) - Options: '', '0 Dribbles', '1 Dribble',
        '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    :param list[str] general_ranges: (optional) - Options: 'Overall',
        'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    :param str date_from: (optional) Format - MM/DD/YYYY
    :param str date_to: (optional) Format - MM/DD/YYYY
    :param list[int] periods: (optional) Only get stats for specific periods
    :param str location: (optional) - Options: 'Home' or 'Road'
    :return: list of dicts with stats for each player/team
    :rtype: list[dict]
    """
    close_def_dists = kwargs.get("close_def_dists", [""])
    shot_clocks = kwargs.get("shot_clocks", [""])
    shot_dists = kwargs.get("shot_dists", [""])
    touch_times = kwargs.get("touch_times", [""])
    dribble_ranges = kwargs.get("dribble_ranges", [""])
    general_ranges = kwargs.get("general_ranges", ["Overall"])
    periods = kwargs.get("periods", [""])
    filters = list(
        itertools.product(
            close_def_dists,
            shot_clocks,
            shot_dists,
            touch_times,
            dribble_ranges,
            general_ranges,
            periods,
        )
    )

    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            season_stats = []
            for close_def, clock, dist, touch, dribbles, general, period in filters:
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
                    date_from=kwargs.get("date_from", ""),
                    date_to=kwargs.get("date_to", ""),
                    period=period,
                    location=kwargs.get("location", ""),
                )
                filter_stats = utils.make_array_of_dicts_from_response_json(
                    response_json, 0
                )
                season_stats.append(filter_stats)
            stats = sum_tracking_shot_totals(entity_type, *season_stats)
            entity_id_key = "PLAYER_ID" if entity_type == "player" else "TEAM_ID"
            overall_response_json = get_tracking_shots_response(
                entity_type,
                season,
                season_type,
                general_range="Overall",
                date_from=kwargs.get("date_from", ""),
                date_to=kwargs.get("date_to", ""),
            )
            overall_stats = utils.make_array_of_dicts_from_response_json(
                overall_response_json, 0
            )
            overall_stats_by_entity = {
                stat[entity_id_key]: {
                    "FGA": stat["FGA"],
                    "FG2A": stat["FG2A"],
                    "FG3A": stat["FG3A"],
                }
                for stat in overall_stats
            }
            for stat in stats:
                entity_id = stat[entity_id_key]
                stat["SEASON"] = f"{season} {season_type}"
                stat["OVERALL_FGA"] = overall_stats_by_entity[entity_id]["FGA"]
                stat["OVERALL_FG2A"] = overall_stats_by_entity[entity_id]["FG2A"]
                stat["OVERALL_FG3A"] = overall_stats_by_entity[entity_id]["FG3A"]
                stat["FGA_FREQUENCY"] = (
                    stat["FGA"] / stat["OVERALL_FGA"] if stat["OVERALL_FGA"] != 0 else 0
                )
                stat["FG2A_FREQUENCY"] = (
                    stat["FG2A"] / stat["OVERALL_FGA"]
                    if stat["OVERALL_FGA"] != 0
                    else 0
                )
                stat["FG3A_FREQUENCY"] = (
                    stat["FG3A"] / stat["OVERALL_FGA"]
                    if stat["OVERALL_FGA"] != 0
                    else 0
                )
                stat["FREQUENCY_OF_FG2A"] = (
                    stat["FG2A"] / stat["OVERALL_FG2A"]
                    if stat["OVERALL_FG2A"] != 0
                    else 0
                )
                stat["FREQUENCY_OF_FG3A"] = (
                    stat["FG3A"] / stat["OVERALL_FG3A"]
                    if stat["OVERALL_FG3A"] != 0
                    else 0
                )
            all_season_stats += stats
    return all_season_stats


def aggregate_full_season_tracking_shot_stats_for_seasons(
    entity_type, seasons, season_types, **kwargs
):
    """
    Aggregates full season stats for desired filters.
    Returns list of dicts for stats for each team/player and dict with league totals.

    :param str entity_type: Options are player, team or opponent
    :param list[str] seasons: List of seasons.Format YYYY-YY ex 2019-20
    :param list[str] season_types: List of season types. Options are Regular Season or Playoffs or Play In
    :param list[str] close_def_dists: (optional) Options: '', '0-2 Feet - Very Tight',
        '2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    :param list[str] shot_clocks: (optional) - Options: '', '24-22',
        '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late'
    :param list[str] shot_dists: (optional) - Options: '', '>=10.0'
    :param list[str] touch_times: (optional) - Options: '', 'Touch < 2 Seconds',
        'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    :param list[str] dribble_ranges: (optional) - Options: '', '0 Dribbles', '1 Dribble',
        '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    :param list[str] general_ranges: (optional) - Options: 'Overall',
        'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    :param list[int] periods: (optional) Only get stats for specific periods
    :param str location: (optional) - Options: 'Home' or 'Road'
    :return: tuple with list of dicts for stats for each player/team and dict with league totals
    :rtype: tuple(list[dict], dict)
    """
    stats_by_season = get_tracking_shot_stats(
        entity_type, seasons, season_types, **kwargs
    )

    stats = sum_tracking_shot_totals(entity_type, stats_by_season)
    league_totals = sum_tracking_shot_totals("league", stats_by_season)
    return stats, league_totals


def generate_tracking_shot_game_logs(entity_type, date_from, date_to, **kwargs):
    """
    Generates game logs for all games between two dates for desired filters

    :param str entity_type: Options are player, team or opponent
    :param str date_from: Format - MM/DD/YYYY
    :param str date_to: Format - MM/DD/YYYY
    :param dict team_id_game_id_map: (optional) dict mapping team id to game id. When
        getting game logs for multiple separate filters for the same date it is recommended
        that you pass this in to avoid making the same request multiple times
    :param dict team_id_opponent_team_id_map: (optional) dict mapping team id to opponent team id.
        When getting game logs for multiple separate filters for the same date it is recommended
        that you pass this in to avoid making the same request multiple times
    :param dict player_id_team_id_map: (optional) dict mapping player id to team id. When
        getting game logs for multiple separate filters for the same date it is recommended
        that you pass this in to avoid making the same request multiple times
    :param list[str] close_def_dists: (optional) Options: '', '0-2 Feet - Very Tight',
        '2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
    :param list[str] shot_clocks: (optional) - Options: '', '24-22',
        '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late'
    :param list[str] shot_dists: (optional) - Options: '', '>=10.0'
    :param list[str] touch_times: (optional) - Options: '', 'Touch < 2 Seconds',
        'Touch 2-6 Seconds', 'Touch 6+ Seconds'
    :param list[str] dribble_ranges: (optional) - Options: '', '0 Dribbles', '1 Dribble',
        '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
    :param list[str] general_ranges: (optional) - Options: 'Overall',
        'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
    :param list[int] periods: (optional) Only get stats for specific periods
    :param str location: (optional) - Options: 'Home' or 'Road'
    :return: list of game log dicts
    :rtype: list[dict]
    """
    start_date = datetime.strptime(date_from, "%m/%d/%Y")
    end_date = datetime.strptime(date_to, "%m/%d/%Y")
    team_id_game_id_map = kwargs.get("team_id_game_id_map")
    team_id_opponent_team_id_map = kwargs.get("team_id_opponent_team_id_map")
    player_id_team_id_map = kwargs.get("player_id_team_id_map")
    get_player_id_team_id_map = player_id_team_id_map is None
    get_team_id_maps = (
        team_id_game_id_map is None or team_id_opponent_team_id_map is None
    )
    game_logs = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        date = dt.strftime("%m/%d/%Y")
        if get_team_id_maps:
            (
                team_id_game_id_map,
                team_id_opponent_team_id_map,
            ) = utils.get_team_id_maps_for_date(date)
        if len(team_id_game_id_map.values()) != 0:
            if get_player_id_team_id_map:
                player_id_team_id_map = utils.get_player_team_map_for_date(date)
            date_game_id = list(team_id_game_id_map.values())[0]

            season = utils.get_season_from_game_id(date_game_id)
            season_type = utils.get_season_type_from_game_id(date_game_id)

            tracking_shots_data = get_tracking_shot_stats(
                entity_type,
                [season],
                [season_type],
                date_from=date,
                date_to=date,
                **kwargs,
            )
            tracking_shots_game_logs = sum_tracking_shot_totals(
                entity_type, tracking_shots_data
            )
            if entity_type == "player":
                # need to add team id for player because results only have PLAYER_LAST_TEAM_ID,
                # which may not be the team for which they played the game
                for game_log in tracking_shots_game_logs:
                    game_log["TEAM_ID"] = player_id_team_id_map[game_log["PLAYER_ID"]]
            for game_log in tracking_shots_game_logs:
                game_log["GAME_ID"] = team_id_game_id_map[game_log["TEAM_ID"]]
                game_log["OPPONENT_TEAM_ID"] = team_id_opponent_team_id_map[
                    game_log["TEAM_ID"]
                ]
            game_logs += tracking_shots_game_logs
    return game_logs


def sum_tracking_shot_totals(entity_type, *args):
    r"""
    Sums totals for given dicts and grouped by entity type

    :param str entity_type: Options are player, team, opponent or league
    :param dict \*args: Variable length argument list of dicts to be summed up
    :return: list of dicts with totals for each entity
    :rtype: list[dict]
    """
    if entity_type == "player":
        entity_key = "PLAYER_ID"
    elif entity_type == "team" or entity_type == "opponent":
        entity_key = "TEAM_ID"
    elif entity_type == "league":
        totals_dict = {
            "FGM": 0,
            "FGA": 0,
            "FG2M": 0,
            "FG2A": 0,
            "FG3M": 0,
            "FG3A": 0,
            "OVERALL_FGA": 0,
            "OVERALL_FG2A": 0,
            "OVERALL_FG3A": 0,
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
                if entity_type == "player":
                    totals_dict[entity_id] = {
                        "PLAYER_ID": item["PLAYER_ID"],
                        "PLAYER_NAME": item["PLAYER_NAME"],
                        "PLAYER_LAST_TEAM_ID": item["PLAYER_LAST_TEAM_ID"],
                        "PLAYER_LAST_TEAM_ABBREVIATION": item[
                            "PLAYER_LAST_TEAM_ABBREVIATION"
                        ],
                        "FGM": 0,
                        "FGA": 0,
                        "FG2M": 0,
                        "FG2A": 0,
                        "FG3M": 0,
                        "FG3A": 0,
                        "OVERALL_FGA": 0,
                        "OVERALL_FG2A": 0,
                        "OVERALL_FG3A": 0,
                    }
                elif entity_type == "team" or entity_type == "opponent":
                    totals_dict[entity_id] = {
                        "TEAM_ID": item["TEAM_ID"],
                        "TEAM_NAME": item["TEAM_NAME"],
                        "TEAM_ABBREVIATION": item["TEAM_ABBREVIATION"],
                        "FGM": 0,
                        "FGA": 0,
                        "FG2M": 0,
                        "FG2A": 0,
                        "FG3M": 0,
                        "FG3A": 0,
                        "OVERALL_FGA": 0,
                        "OVERALL_FG2A": 0,
                        "OVERALL_FG3A": 0,
                    }
            totals_dict[entity_id] = add_to_tracking_shot_totals(
                totals_dict[entity_id], item
            )

    return list(totals_dict.values())


def add_to_tracking_shot_totals(totals, item):
    """
    Adds shot totals from item to totals and updates percentages

    :param dict totals: Totals to be added to
    :param dict item: Item to be added to totals dict
    :return: totals dict
    :rtype: dict
    """
    totals["FGM"] += item["FGM"]
    totals["FGA"] += item["FGA"]
    totals["FG2M"] += item["FG2M"]
    totals["FG2A"] += item["FG2A"]
    totals["FG3M"] += item["FG3M"]
    totals["FG3A"] += item["FG3A"]
    totals["OVERALL_FGA"] += item.get("OVERALL_FGA", 0)
    totals["OVERALL_FG2A"] += item.get("OVERALL_FG2A", 0)
    totals["OVERALL_FG3A"] += item.get("OVERALL_FG3A", 0)
    fg2a = totals["FG2A"]
    fg2m = totals["FG2M"]
    fg3a = totals["FG3A"]
    fg3m = totals["FG3M"]
    totals["FG2_PCT"] = fg2m / fg2a if fg2a != 0 else 0
    totals["FG3_PCT"] = fg3m / fg3a if fg3a != 0 else 0
    totals["EFG_PCT"] = (1.5 * fg3m + fg2m) / (fg3a + fg2a) if (fg3a + fg2a) != 0 else 0
    totals["FGA_FREQUENCY"] = (
        totals["FGA"] / totals["OVERALL_FGA"] if totals["OVERALL_FGA"] != 0 else 0
    )
    totals["FG2A_FREQUENCY"] = (
        totals["FG2A"] / totals["OVERALL_FGA"] if totals["OVERALL_FGA"] != 0 else 0
    )
    totals["FG3A_FREQUENCY"] = (
        totals["FG3A"] / totals["OVERALL_FGA"] if totals["OVERALL_FGA"] != 0 else 0
    )
    totals["FREQUENCY_OF_FG2A"] = (
        totals["FG2A"] / totals["OVERALL_FG2A"] if totals["OVERALL_FG2A"] != 0 else 0
    )
    totals["FREQUENCY_OF_FG3A"] = (
        totals["FG3A"] / totals["OVERALL_FG3A"] if totals["OVERALL_FG3A"] != 0 else 0
    )

    return totals
