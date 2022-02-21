.. _quickstart:

Installation
================

.. code-block:: bash

    $ pip install nba_stats_tracking

Code Examples
================

Aggregating Multiple Tracking Shot Stat Filters and/or Seasons
--------------------------------------------------------------

The following will get aggregate player stats for Catch and Shoot, Open or Wide-Open shots in the Regular Season and Playoffs from 2013-14 to 2019-20::

    from nba_stats_tracking import tracking_shots
    from nba_stats_tracking.models.request import SeasonType
    from nba_stats_tracking.models.tracking_shots import CloseDefDist, GeneralRange

    seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']
    season_types = [SeasonType.regular_season, SeasonType.playoffs]
    def_distances = [CloseDefDist.range_6_plus_ft, CloseDefDist.range_4_6_ft]
    general_ranges = [GeneralRange.catch_and_shoot]

    stats, league_totals = tracking_shots.aggregate_full_season_tracking_shot_stats_for_seasons(
        'player',
        seasons,
        season_types,
        CloseDefDistRange=def_distances,
        GeneralRange=general_ranges
    )

    for stat in stats:
        print(stat)
    print(league_totals)

Generating Tracking Shot Game Logs
-----------------------------------

The following gets player game logs for Open and Wide Open Catch and Shoot shots for games from 02/02/2020 to 02/03/2020::

    from datetime import date

    from nba_stats_tracking import tracking_shots
    from nba_stats_tracking.models.tracking_shots import CloseDefDist, GeneralRange

    def_distances = [CloseDefDist.range_6_plus_ft, CloseDefDist.range_4_6_ft]
    general_ranges = [GeneralRange.catch_and_shoot]
    date_from = date(2020, 2, 2)
    date_to = date(2020, 2, 3)

    game_logs = tracking_shots.generate_tracking_shot_game_logs(
        tracking_shots.EntityType.player,
        date_from,
        date_to,
        CloseDefDistRange=def_distances,
        GeneralRange=general_ranges
    )
    for game_log in game_logs:
        print(game_log)

Aggregating Multiple Tracking Shot Stat Filters and Grouping by Season
----------------------------------------------------------------------

The following gets player stats for Catch and Shoot, Open or Wide-Open shots in the Regular Season from 2013-14 to 2019-20 and groups the results by season::

    from nba_stats_tracking import tracking_shots
    from nba_stats_tracking.models.request import SeasonType
    from nba_stats_tracking.models.tracking_shots import CloseDefDist, GeneralRange

    seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']
    season_types = [SeasonType.regular_season]
    def_distances = [CloseDefDist.range_6_plus_ft, CloseDefDist.range_4_6_ft]
    general_ranges = [GeneralRange.catch_and_shoot]

    stats = tracking_shots.get_tracking_shot_stats(
        tracking_shots.EntityType.player,
        seasons,
        season_types,
        CloseDefDistRange=def_distances,
        GeneralRange=general_ranges
    )

    for stat in stats:
        print(stat)

Aggregating Multiple Seasons of Tracking Stats
-----------------------------------------------

The following gets player speed and distance stats from 2018-19 to 2019-20::

    from nba_stats_tracking import tracking
    from nba_stats_tracking.models.request import SeasonType
    from nba_stats_tracking.models.tracking import TrackingMeasureType, PlayerOrTeam

    stat_measure = TrackingMeasureType.speed_distance
    seasons = ['2018-19', '2019-20']
    season_types = [SeasonType.regular_season]
    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        stat_measure,
        seasons,
        season_types,
        PlayerOrTeam.player
    )

    for stat in stats:
        print(stat)

    print('-----------------------')
    print(league_totals)

Generating Tracking Game Logs
------------------------------

The following gets player game logs for all tracking stats for games on 02/02/2020::

    from datetime import date

    from nba_stats_tracking import tracking
    from nba_stats_tracking.helpers import get_team_id_maps_for_date, get_player_team_map_for_date
    from nba_stats_tracking.models.tracking import TrackingMeasureType, PlayerOrTeam

    game_date = date(2020, 2, 2)

    team_id_game_id_map, team_id_opponent_team_id_map = get_team_id_maps_for_date(game_date)
    player_id_team_id_map = get_player_team_map_for_date(game_date)

    for stat_measure in TrackingMeasureType:
        game_logs = tracking.generate_tracking_game_logs(
            stat_measure,
            PlayerOrTeam.player,
            game_date,
            game_date,
            team_id_game_id_map=team_id_game_id_map,
            team_id_opponent_team_id_map=team_id_opponent_team_id_map,
            player_id_team_id_map=player_id_team_id_map,
        )
        for game_log in game_logs:
            print(game_log)


Get Opponent Tracking Stats For An Individual Team
---------------------------------------------------

The following gets opponent catch and shoot stats for the Boston Celtics in 2019-20 ::

    from nba_stats_tracking import tracking
    from nba_stats_tracking.models.request import SeasonType
    from nba_stats_tracking.models.tracking import TrackingMeasureType, PlayerOrTeam

    stat_measure = TrackingMeasureType.catch_and_shoot
    seasons = ['2019-20']
    season_types = [SeasonType.regular_season]
    opponent_team_id = 1610612738

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        stat_measure,
        seasons,
        season_types,
        PlayerOrTeam.player,
        OpponentTeamID=opponent_team_id
    )

    for stat in stats:
        print(stat)
    print(league_totals)

Get Matchup stats for game id
---------------------------------------------------

The following gets matchup data for a single game id ::

    from nba_stats_tracking import matchups

    game_id = "0022100831"
    results = matchups.get_matchup_results_for_game_id(game_id)
    print(results)