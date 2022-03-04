"""Module containing functions for accessing tracking shot stats"""

import itertools
import time
from datetime import date
from enum import Enum
from typing import Dict, List, Tuple, TypedDict, Union

from dateutil.rrule import DAILY, rrule

from nba_stats_tracking import helpers
from nba_stats_tracking.models.request import SeasonType
from nba_stats_tracking.models.tracking_shots import (
    CloseDefDist,
    Dribbles,
    GeneralRange,
    ShotClock,
    ShotDist,
    TouchTime,
    TrackingRequestParameters,
    TrackingShotItem,
    TrackingShotResults,
)


class EntityType(str, Enum):
    team = "team"
    player = "player"
    opponent = "opponent"


def get_tracking_shots_response_results_for_filter(
    entity_type: EntityType, season: str, season_type: SeasonType, **kwargs
) -> Dict:
    """
    Makes API call to `NBA Advanced Stats <https://www.stats.nba.com/>`_ and returns JSON response results

    :param entity_type: Get results for player, team or opponent
    :param str season: Format YYYY-YY ex 2019-20
    :param season_type: Season type to get stats for
    :param str DateFrom: (optional) Format - MM/DD/YYYY
    :param str DateTo: (optional) Format - MM/DD/YYYY
    :param CloseDefDist CloseDefDistRange: (optional) Defaults to "".
    :param ShotClock ShotClockRange: (optional) - Defaults to "".
    :param ShotDist ShotDistRange: (optional) - Defaults to "".
    :param TouchTime TouchTimeRange: (optional) - Defaults to "".
    :param Dribbles DribbleRange: (optional) - Defaults to "".
    :param GeneralRange GeneralRange: (optional) - Defaults to "Overall".
    :param int Period: (optional) Only get stats for specific period
    :param str Location: (optional) - Options: 'Home' or 'Road'
    """
    if entity_type == EntityType.team:
        url = "https://stats.nba.com/stats/leaguedashteamptshot"
    elif entity_type == EntityType.player:
        url = "https://stats.nba.com/stats/leaguedashplayerptshot"
    elif entity_type == EntityType.opponent:
        url = "https://stats.nba.com/stats/leaguedashoppptshot"

    parameters = TrackingRequestParameters(
        Season=season,
        SeasonType=season_type,
        **kwargs,
    )

    response_json = helpers.get_json_response(
        url, parameters.dict(by_alias=True, exclude_none=True)
    )

    # stats will be contained in first item of resultSets
    return response_json["resultSets"][0]


def get_tracking_shot_stats(
    entity_type: EntityType,
    seasons: List[str],
    season_types: List[SeasonType],
    **kwargs,
) -> List[TrackingShotItem]:
    """
    Gets tracking shot stats for filters
    Returns list of TrackingShotItem with stats for each player/team

    :param entity_type: Get results for player, team or opponent
    :param seasons: Seasons to get stats for. Format YYYY-YY ex 2019-20
    :param season_types: Season types to get stats for
    :param str DateFrom: (optional) Format - MM/DD/YYYY
    :param str DateTo: (optional) Format - MM/DD/YYYY
    :param list[CloseDefDist] CloseDefDistRange: (optional)
    :param list[ShotClock] ShotClockRange: (optional)
    :param list[ShotDist] ShotDistRange: (optional)
    :param list[TouchTime] TouchTimeRange: (optional)
    :param list[Dribbles] DribbleRange: (optional)
    :param list[General] GeneralRange: (optional)
    :param list[int] Period: (optional) Only get stats for specific period
    :param str Location: (optional) - Options: 'Home' or 'Road'
    """
    close_def_dists = kwargs.get("CloseDefDistRange", [CloseDefDist.all])
    shot_clocks = kwargs.get("ShotClockRange", [ShotClock.all])
    shot_dists = kwargs.get("ShotDistRange", [ShotDist.all])
    touch_times = kwargs.get("TouchTimeRange", [TouchTime.all])
    dribble_ranges = kwargs.get("DribbleRange", [Dribbles.all])
    general_ranges = kwargs.get("GeneralRange", [GeneralRange.overall])
    periods = kwargs.get("Period", [""])
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
                # Making too many requests in a short period can result in timeouts. Add a delay between requests
                time.sleep(2)
                results = get_tracking_shots_response_results_for_filter(
                    entity_type,
                    season,
                    season_type,
                    CloseDefDistRange=close_def,  # camel case to match request param key
                    ShotClockRange=clock,
                    ShotDistRange=dist,
                    TouchTimeRange=touch,
                    DribbleRange=dribbles,
                    GeneralRange=general,
                    DateFrom=kwargs.get("DateFrom", ""),
                    DateTo=kwargs.get("DateTo", ""),
                    Period=str(period),
                    Location=kwargs.get("Location", ""),
                )
                filter_stats = TrackingShotResults(**results)
                season_stats.append(filter_stats.results)
            stats = sum_tracking_shot_totals(entity_type, *season_stats)
            # Get overall FGA, FG2A and FG3A to compute frequencies
            overall_results = get_tracking_shots_response_results_for_filter(
                entity_type,
                season,
                season_type,
                GeneralRange=GeneralRange.overall,
                DateFrom=kwargs.get("DateFrom", ""),
                DateTo=kwargs.get("DateTo", ""),
            )
            overall_stats = TrackingShotResults(**overall_results)
            entity_id_key = "player_id" if entity_type == "player" else "team_id"
            overall_stats_by_entity = {
                stat[entity_id_key]: {
                    "fga": stat.fga,
                    "fg2a": stat.fg2a,
                    "fg3a": stat.fg3a,
                }
                for stat in overall_stats.results
            }
            for stat in stats:
                entity_id = stat[entity_id_key]
                stat.season = f"{season} {season_type}"
                stat.overall_fga = overall_stats_by_entity[entity_id]["fga"]
                stat.overall_fg2a = overall_stats_by_entity[entity_id]["fg2a"]
                stat.overall_fg3a = overall_stats_by_entity[entity_id]["fg3a"]

            all_season_stats += stats
    return all_season_stats


def aggregate_full_season_tracking_shot_stats_for_seasons(
    entity_type: EntityType,
    seasons: List[str],
    season_types: List[SeasonType],
    **kwargs,
) -> Tuple[List[TrackingShotItem], TrackingShotItem]:
    """
    Aggregates full season stats for desired filters.
    Returns list of TrackingShotItem for stats for each team/player and TrackingShotItem with league totals.

    :param entity_type: Get results for player, team or opponent
    :param seasons: List of seasons.Format YYYY-YY ex 2019-20
    :param season_types: Season types to get stats for
    :param list[CloseDefDist] CloseDefDistRange: (optional)
    :param list[ShotClock] ShotClockRange: (optional)
    :param list[ShotDist] ShotDistRange: (optional)
    :param list[TouchTime] TouchTimeRange: (optional)
    :param list[Dribbles] DribbleRange: (optional)
    :param list[GeneralRange] GeneralRange: (optional)
    :param list[int] Period: (optional) Only get stats for specific period
    :param str Location: (optional) - Options: 'Home' or 'Road'
    """
    stats_by_season = get_tracking_shot_stats(
        entity_type, seasons, season_types, **kwargs
    )

    stats = sum_tracking_shot_totals(entity_type, stats_by_season)
    league_totals = sum_tracking_shot_totals("league", stats_by_season)
    return stats, league_totals


def generate_tracking_shot_game_logs(
    entity_type: EntityType, date_from: date, date_to: date, **kwargs
) -> List[TrackingShotItem]:
    """
    Generates game logs for all games between two dates for desired filters
    Returns list of TrackingShotItem

    :param entity_type: Get results for player, team or opponent
    :param date_from: start date
    :param date_to: end date
    :param dict team_id_game_id_map: (optional) dict mapping team id to game id. When
        getting game logs for multiple separate filters for the same date it is recommended
        that you pass this in to avoid making the same request multiple times
    :param dict team_id_opponent_team_id_map: (optional) dict mapping team id to opponent team id.
        When getting game logs for multiple separate filters for the same date it is recommended
        that you pass this in to avoid making the same request multiple times
    :param dict player_id_team_id_map: (optional) dict mapping player id to team id. When
        getting game logs for multiple separate filters for the same date it is recommended
        that you pass this in to avoid making the same request multiple times
    :param CloseDefDist CloseDefDistRange: (optional) Defaults to "".
    :param ShotClock ShotClockRange: (optional) - Defaults to "".
    :param ShotDist ShotDistRange: (optional) - Defaults to "".
    :param TouchTime TouchTimeRange: (optional) - Defaults to "".
    :param Dribbles DribbleRange: (optional) - Defaults to "".
    :param GeneralRange GeneralRange: (optional) - Defaults to "Overall".
    :param int Period: (optional) Only get stats for specific period
    :param str Location: (optional) - Options: 'Home' or 'Road'
    """
    team_id_game_id_map = kwargs.get("team_id_game_id_map")
    team_id_opponent_team_id_map = kwargs.get("team_id_opponent_team_id_map")
    player_id_team_id_map = kwargs.get("player_id_team_id_map")
    get_player_id_team_id_map = player_id_team_id_map is None
    get_team_id_maps = (
        team_id_game_id_map is None or team_id_opponent_team_id_map is None
    )
    game_logs = []
    for dt in rrule(DAILY, dtstart=date_from, until=date_to):
        if get_team_id_maps:
            (
                team_id_game_id_map,
                team_id_opponent_team_id_map,
            ) = helpers.get_team_id_maps_for_date(dt)
        if len(team_id_game_id_map.values()) != 0:
            if get_player_id_team_id_map:
                player_id_team_id_map = helpers.get_player_team_map_for_date(dt)
            date_game_id = list(team_id_game_id_map.values())[0]

            season = helpers.get_season_from_game_id(date_game_id)
            season_type = helpers.get_season_type_from_game_id(date_game_id)

            tracking_shots_data = get_tracking_shot_stats(
                entity_type,
                [season],
                [season_type],
                DateFrom=dt.strftime("%m/%d/%Y"),
                DateTo=dt.strftime("%m/%d/%Y"),
                **kwargs,
            )
            tracking_shots_game_logs = sum_tracking_shot_totals(
                entity_type, tracking_shots_data
            )
            if entity_type == "player":
                # need to add team id for player because results only have PLAYER_LAST_TEAM_ID,
                # which may not be the team for which they played the game
                for game_log in tracking_shots_game_logs:
                    if game_log.player_id in player_id_team_id_map.keys():
                        game_log.team_id = player_id_team_id_map[game_log.player_id]
            for game_log in tracking_shots_game_logs:
                if game_log.team_id is not None:
                    game_log.game_id = team_id_game_id_map[game_log.team_id]
                    game_log.opponent_team_id = team_id_opponent_team_id_map[
                        game_log.team_id
                    ]
            game_logs += tracking_shots_game_logs
    return game_logs


def sum_tracking_shot_totals(
    entity_type: str, *args: List[TrackingShotItem]
) -> Union[List[TrackingShotItem], TrackingShotItem]:
    r"""
    Sums totals for given TrackingShotItem and grouped by entity type
    Returns list of TrackingShotItem with totals for each entity or TrackingShotItem if entity type is league

    :param entity_type: Options are player, team, opponent or league
    :param \*args: Variable length argument list of TrackingShotItem to be summed up
    """
    if entity_type == "player":
        entity_key = "player_id"
    elif entity_type == "team" or entity_type == "opponent":
        entity_key = "team_id"
    elif entity_type == "league":
        totals = TrackingShotItem(TEAM_ID=0, TEAM_ABBREVIATION="LEAGUE")
        for items in args:
            for item in items:
                totals += item
        return totals
    else:
        return []
    totals = {}
    for item in args:
        for result in item:
            entity_id = result[entity_key]
            if entity_id not in totals.keys():
                totals[entity_id] = result
            else:
                totals[entity_id] += result

    return list(totals.values())
