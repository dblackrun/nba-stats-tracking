import time
from datetime import date
from typing import Any, Dict, List, Tuple, Union

from dateutil.rrule import DAILY, rrule

from nba_stats_tracking import helpers
from nba_stats_tracking.models.request import PerMode, SeasonType
from nba_stats_tracking.models.tracking import (
    CatchAndShootItem,
    CatchAndShootResults,
    DefenseItem,
    DefenseResults,
    DrivesItem,
    DrivesResults,
    EfficiencyItem,
    EfficiencyResults,
    ElbowTouchesItem,
    ElbowTouchesResults,
    PaintTouchesItem,
    PaintTouchesResults,
    PassingItem,
    PassingResults,
    PlayerOrTeam,
    PossessionsItem,
    PossessionsResults,
    PostTouchesItem,
    PostTouchesResults,
    PullUpItem,
    PullUpResults,
    ReboundingItem,
    ReboundingResults,
    SpeedDistanceItem,
    SpeedDistanceResults,
    TrackingMeasureType,
    TrackingRequestParameters,
)

RESPONSE_MODEL_MAP = {
    TrackingMeasureType.catch_and_shoot: CatchAndShootResults,
    TrackingMeasureType.defense: DefenseResults,
    TrackingMeasureType.drives: DrivesResults,
    TrackingMeasureType.shooting: EfficiencyResults,
    TrackingMeasureType.elbow_touches: ElbowTouchesResults,
    TrackingMeasureType.paint_touches: PaintTouchesResults,
    TrackingMeasureType.passing: PassingResults,
    TrackingMeasureType.possessions: PossessionsResults,
    TrackingMeasureType.post_touches: PostTouchesResults,
    TrackingMeasureType.pull_up: PullUpResults,
    TrackingMeasureType.rebounding: ReboundingResults,
    TrackingMeasureType.speed_distance: SpeedDistanceResults,
}

DATA_ITEM_MAP = {
    TrackingMeasureType.catch_and_shoot: CatchAndShootItem,
    TrackingMeasureType.defense: DefenseItem,
    TrackingMeasureType.drives: DrivesItem,
    TrackingMeasureType.shooting: EfficiencyItem,
    TrackingMeasureType.elbow_touches: ElbowTouchesItem,
    TrackingMeasureType.paint_touches: PaintTouchesItem,
    TrackingMeasureType.passing: PassingItem,
    TrackingMeasureType.possessions: PossessionsItem,
    TrackingMeasureType.post_touches: PostTouchesItem,
    TrackingMeasureType.pull_up: PullUpItem,
    TrackingMeasureType.rebounding: ReboundingItem,
    TrackingMeasureType.speed_distance: SpeedDistanceItem,
}


def get_tracking_results_for_stat_measure(
    measure_type: TrackingMeasureType,
    season: str,
    season_type: SeasonType,
    player_or_team: PlayerOrTeam,
    **kwargs,
) -> Dict:
    """
    Makes API call to `NBA Advanced Stats <https://www.stats.nba.com/>`_ and returns JSON response results

    :param measure_type: Stat measure type to get stats for
    :param season: Format YYYY-YY ex 2019-20
    :param season_type: Season type to get stats for
    :param player_or_team: get stats for player or team
    :param str DateFrom: (optional) Format - MM/DD/YYYY
    :param str DateTo: (optional) Format - MM/DD/YYYY
    :param str OpponentTeamID: (optional) nba.com team id
    :param `~nba_stats_tracking.models.request.PerMode` PerMode: (optional) Defaults to totals.

    :return: response json
    :rtype: dict
    """
    url = "https://stats.nba.com/stats/leaguedashptstats"

    parameters = TrackingRequestParameters(
        PtMeasureType=measure_type,
        Season=season,
        SeasonType=season_type,
        PlayerOrTeam=player_or_team,
        **kwargs,
    )

    response_json = helpers.get_json_response(
        url, parameters.dict(by_alias=True, exclude_none=True)
    )

    # stats will be contained in first item of resultSets
    return response_json["resultSets"][0]


def get_tracking_stats(
    measure_type: TrackingMeasureType,
    seasons: List[str],
    season_types: List[SeasonType],
    player_or_team: PlayerOrTeam,
    **kwargs,
) -> List[Any]:
    """
    Gets stat measure tracking stats for filter
    Returns list of ResultItem with stats for each player/team

    :param measure_type: Stat measure type to get stats for
    :param seasons: List of seasons. Format YYYY-YY ex 2019-20
    :param season_types: List of season types.
    :param player_or_team: get stats for player or team
    :param str DateFrom: (optional) Format - MM/DD/YYYY
    :param str DateTo: (optional) Format - MM/DD/YYYY
    :param str OpponentTeamID: (optional) nba.com team id
    :param `~nba_stats_tracking.models.request.PerMode` PerMode: (optional) Defaults to totals.
    """
    all_season_stats = []
    for season in seasons:
        for season_type in season_types:
            # Making too many requests in a short period can result in timeouts. Add a delay between requests
            time.sleep(2)
            results = get_tracking_results_for_stat_measure(
                measure_type, season, season_type, player_or_team, **kwargs
            )
            stats = RESPONSE_MODEL_MAP[measure_type](**results)
            for stat in stats.results:
                stat.season = f"{season} {season_type}"
            all_season_stats += stats.results
    return all_season_stats


def aggregate_full_season_tracking_stats_for_seasons(
    measure_type: TrackingMeasureType,
    seasons: List[str],
    season_types: List[SeasonType],
    player_or_team: PlayerOrTeam,
    **kwargs,
) -> Tuple[List[Any], Any]:
    """
    Aggregates full season stats for stat measure for desired filters.
    Returns list of ResultItem for stats for each team/player and ResultItem with league totals.

    :param measure_type: Stat measure type to get stats for
    :param seasons: List of seasons. Format YYYY-YY ex 2019-20
    :param season_types: List of season types.
    :param player_or_team: get stats for player or team
    :param str OpponentTeamID: (optional) nba.com team id
    """
    stats_by_season = get_tracking_stats(
        measure_type, seasons, season_types, player_or_team, **kwargs
    )

    stats = sum_tracking_totals(player_or_team, measure_type, stats_by_season)
    league_totals = sum_tracking_totals("league", measure_type, stats)
    return stats, league_totals


def generate_tracking_game_logs(
    measure_type: TrackingMeasureType,
    player_or_team: PlayerOrTeam,
    date_from: date,
    date_to: date,
    **kwargs,
) -> List[Any]:
    """
    Generates game logs for all games between two dates for desired filters
    Returns list of game log ResultItem

    :param measure_type: Stat measure type to get stats for
    :param player_or_team: get stats for player or team
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

            tracking_game_logs = get_tracking_stats(
                measure_type,
                [season],
                [season_type],
                player_or_team,
                # User per game here because it gives results to more decimal places
                PerMode=PerMode.per_game,  # camel case to match request param key
                DateFrom=dt.strftime("%m/%d/%Y"),
                DateTo=dt.strftime("%m/%d/%Y"),
            )
            if player_or_team == PlayerOrTeam.player:
                # need to add team id for player because results only have last team id,
                # which may not be the team for which they played the game
                for game_log in tracking_game_logs:
                    game_log.team_id = player_id_team_id_map[game_log.player_id]
            for game_log in tracking_game_logs:
                game_log.game_id = team_id_game_id_map[game_log.team_id]
                game_log.opponent_team_id = team_id_opponent_team_id_map[
                    game_log.team_id
                ]
            game_logs += tracking_game_logs
    return game_logs


def sum_tracking_totals(
    entity_type: str, measure_type: TrackingMeasureType, *args
) -> Union[List[Any], Any]:
    r"""
    Sums totals for given dicts and grouped by entity type
    Returns list of ResultItem with totals for each entity or ResultItem if entity type is league

    :param entity_type: Options are Player, Team or league
    :param measure_type: Stat measure type to get stats for
    :param \*args: Variable length argument list of ResultItem to be summed up
    """
    if entity_type == PlayerOrTeam.player:
        entity_key = "player_id"
    elif entity_type == PlayerOrTeam.team:
        entity_key = "team_id"
    elif entity_type == "league":
        totals = DATA_ITEM_MAP[measure_type](TEAM_ID="00", TEAM_ABBREVIATION="LEAGUE")
        for items in args:
            for item in items:
                totals += item
        return totals
    else:
        return []
    totals = {}
    for items in args:
        for item in items:
            entity_id = item[entity_key]
            if entity_id not in totals.keys():
                totals[entity_id] = item
            else:
                totals[entity_id] += item

    return list(totals.values())
