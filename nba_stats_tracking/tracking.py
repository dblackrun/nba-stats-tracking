import time

from dateutil.rrule import rrule, DAILY
from datetime import datetime

from nba_stats_tracking import utils


def get_tracking_response_json_for_stat_measure(
    stat_measure, season, season_type, entity_type, **kwargs
):
    """
    Makes API call to `NBA Advanced Stats <https://www.stats.nba.com/>`_ and returns JSON response

    :param str stat_measure: Options: Drives, Defense, CatchShoot, Passing, Possessions,
        PullUpShot, Rebounding, Efficiency, SpeedDistance, ElbowTouch, PostTouch, PaintTouch
    :param str season: Format YYYY-YY ex 2019-20
    :param str season_type: Options are Regular Season or Playoffs or Play In
    :param str entity_type: Options are player or team
    :param str date_from: (optional) Format - MM/DD/YYYY
    :param str date_to: (optional) Format - MM/DD/YYYY
    :param str opponent_team_id: (optional) nba.com team id

    :return: response json
    :rtype: dict
    """
    url = "https://stats.nba.com/stats/leaguedashptstats"

    parameters = {
        "PlayerOrTeam": entity_type.title(),
        "PtMeasureType": stat_measure,
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": kwargs.get("date_from", ""),
        "DateTo": kwargs.get("date_to", ""),
        "GameScope": "",
        "LastNGames": 0,
        "LeagueID": "00",
        "Location": "",
        "Month": 0,
        "OpponentTeamID": kwargs.get("opponent_team_id", 0),
        "Outcome": "",
        "PerMode": "Totals",
        "PlayerExperience": "",
        "PlayerPosition": "",
        "SeasonSegment": "",
        "StarterBench": "",
        "VsConference": "",
        "VsDivision": "",
    }

    return utils.get_json_response(url, parameters)


def get_tracking_stats(stat_measure, seasons, season_types, entity_type, **kwargs):
    """
    Gets stat measure tracking stats for filter

    :param str stat_measure: Options: Drives, Defense, CatchShoot, Passing, Possessions,
        PullUpShot, Rebounding, Efficiency, SpeedDistance, ElbowTouch, PostTouch, PaintTouch
    :param list[str] seasons: List of seasons.Format YYYY-YY ex 2019-20
    :param list[str] season_types: List of season types. Options are Regular Season or Playoffs or Play In
    :param str entity_type: Options are player or team
    :param str date_from: (optional) Format - MM/DD/YYYY
    :param str date_to: (optional) Format - MM/DD/YYYY
    :param str opponent_team_id: (optional) nba.com team id
    :return: list of dicts with stats for each player/team
    :rtype: list[dict]
    """
    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            time.sleep(2)
            response_json = get_tracking_response_json_for_stat_measure(
                stat_measure, season, season_type, entity_type, **kwargs
            )
            stats = utils.make_array_of_dicts_from_response_json(response_json, 0)
            for stat in stats:
                stat["SEASON"] = f"{season} {season_type}"
            all_season_stats += stats
    return all_season_stats


def aggregate_full_season_tracking_stats_for_seasons(
    stat_measure, seasons, season_types, entity_type, **kwargs
):
    """
    Aggregates full season stats for stat measure for desired filters.
    Returns list of dicts for stats for each team/player and dict with league totals.

    :param str stat_measure: Options: Drives, Defense, CatchShoot, Passing, Possessions,
        PullUpShot, Rebounding, Efficiency, SpeedDistance, ElbowTouch, PostTouch, PaintTouch
    :param list[str] seasons: List of seasons.Format YYYY-YY ex 2019-20
    :param list[str] season_types: List of season types. Options are Regular Season or Playoffs or Play In
    :param str entity_type: Options are player or team
    :param str opponent_team_id: (optional) nba.com team id
    :return: tuple with list of dicts for stats for each player/team and dict with league totals
    :rtype: tuple(list[dict], dict)
    """
    stats_by_season = get_tracking_stats(
        stat_measure, seasons, season_types, entity_type, **kwargs
    )

    stats = sum_tracking_totals(entity_type, stats_by_season)
    league_totals = sum_tracking_totals("league", stats_by_season)
    return stats, league_totals


def generate_tracking_game_logs(
    stat_measure, entity_type, date_from, date_to, **kwargs
):
    """
    Generates game logs for all games between two dates for desired filters

    :param str stat_measure: Options: Drives, Defense, CatchShoot, Passing, Possessions,
        PullUpShot, Rebounding, Efficiency, SpeedDistance, ElbowTouch, PostTouch, PaintTouch
    :param str entity_type: Options are player or team
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

            tracking_game_logs = get_tracking_stats(
                stat_measure,
                [season],
                [season_type],
                entity_type,
                date_from=date,
                date_to=date,
            )
            if entity_type == "player":
                # need to add team id for player because results only have last team id,
                # which may not be the team for which they played the game
                for game_log in tracking_game_logs:
                    game_log["TEAM_ID"] = player_id_team_id_map[game_log["PLAYER_ID"]]
            for game_log in tracking_game_logs:
                game_log["GAME_ID"] = team_id_game_id_map[game_log["TEAM_ID"]]
                game_log["OPPONENT_TEAM_ID"] = team_id_opponent_team_id_map[
                    game_log["TEAM_ID"]
                ]
            game_logs += tracking_game_logs
    return game_logs


def sum_tracking_totals(entity_type, *args):
    r"""
    Sums totals for given dicts and grouped by entity type

    :param str entity_type: Options are player, team, opponent or league
    :param dict \*args: Variable length argument list of dicts to be summed up
    :return: list of dicts with totals for each entity
    :rtype: list[dict]
    """
    if entity_type == "player":
        entity_key = "PLAYER_ID"
    elif entity_type == "team":
        entity_key = "TEAM_ID"
    elif entity_type == "league":
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
                if entity_type == "player":
                    totals_dict[entity_id] = {
                        "PLAYER_ID": item["PLAYER_ID"],
                        "PLAYER_NAME": item["PLAYER_NAME"],
                        "TEAM_ID": item["TEAM_ID"],
                        "TEAM_ABBREVIATION": item["TEAM_ABBREVIATION"],
                    }
                elif entity_type == "team":
                    totals_dict[entity_id] = {
                        "TEAM_ID": item["TEAM_ID"],
                        "TEAM_NAME": item["TEAM_NAME"],
                        "TEAM_ABBREVIATION": item["TEAM_ABBREVIATION"],
                    }
            totals_dict[entity_id] = add_to_tracking_totals(
                totals_dict[entity_id], item
            )

    return list(totals_dict.values())


def add_to_tracking_totals(totals, item):
    """
    Adds totals from item to totals

    :param dict totals: Totals to be added to
    :param dict item: Item to be added to totals dict
    :return: totals dict
    :rtype: dict
    """
    for key, value in item.items():
        if (
            type(value) is int and key not in ["GP", "W", "L", "TEAM_ID", "PLAYER_ID"]
        ) or key in [
            "MIN",
            "DIST_MILES",
            "DIST_MILES_OFF",
            "DIST_MILES_DEF",
            "TIME_OF_POSS",
        ]:
            if value is not None:
                totals[key] = totals.get(key, 0) + value

    return totals
