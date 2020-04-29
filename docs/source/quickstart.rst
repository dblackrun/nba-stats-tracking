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

    seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']
    season_types = ['Regular Season', 'Playoffs']
    def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
    general_ranges = ['Catch and Shoot']

    stats, league_totals = tracking_shots.aggregate_full_season_tracking_shot_stats_for_seasons(
        'player',
        seasons,
        season_types,
        close_def_dists=def_distances,
        general_ranges=general_ranges
    )

    for stat in stats:
        print(stat)
    print(league_totals)

Generating Tracking Shot Game Logs
-----------------------------------

The following gets player game logs for Open and Wide Open Catch and Shoot shots for games from 02/02/2020 to 02/03/2020::

    from nba_stats_tracking import tracking_shots

    def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
    general_ranges = ['Catch and Shoot']
    date_from = '02/02/2020'
    date_to = '02/03/2020'

    game_logs = tracking_shots.generate_tracking_shot_game_logs(
        'player',
        date_from,
        date_to,
        close_def_dists=def_distances,
        general_ranges=general_ranges
    )
    for game_log in game_logs:
        print(game_log)

Aggregating Multiple Tracking Shot Stat Filters and Grouping by Season
----------------------------------------------------------------------

The following gets player stats for Catch and Shoot, Open or Wide-Open shots in the Regular Season from 2013-14 to 2019-20 and groups the results by season::

    from nba_stats_tracking import tracking_shots

    seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']
    season_types = ['Regular Season']
    def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
    general_ranges = ['Catch and Shoot']

    stats = tracking_shots.get_tracking_shot_stats(
        'player',
        seasons,
        season_types,
        close_def_dists=def_distances,
        general_ranges=general_ranges
    )

    for stat in stats:
        print(stat)

Aggregating Multiple Seasons of Tracking Stats
-----------------------------------------------

The following gets player speed and distance stats from 2018-19 to 2019-20::

    from nba_stats_tracking import tracking

    stat_measure = 'SpeedDistance'
    seasons = ['2018-19', '2019-20']
    season_types = ['Regular Season']
    entity_type = 'player'
    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        stat_measure,
        seasons,
        season_types,
        entity_type
    )

    for stat in stats:
        print(stat)

    print('-----------------------')
    print(league_totals)

Generating Tracking Game Logs
------------------------------

The following gets player game logs for catch and shoot shots for games from 02/02/2020 to 02/03/2020::

    from nba_stats_tracking import tracking

    stat_measure = 'CatchShoot'
    entity_type = 'player'
    date_from = '02/02/2020'
    date_to = '02/03/2020'

    game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
    for game_log in game_logs:
        print(game_log)

Get Opponent Tracking Stats For An Individual Team
---------------------------------------------------

The following gets opponent catch and shoot stats for the Boston Celtics in 2019-20 ::

    from nba_stats_tracking import tracking

    stat_measure = 'CatchShoot'
    seasons = ['2019-20']
    season_types = ['Regular Season']
    entity_type = 'team'
    opponent_team_id = 1610612738

    # stats will be each team's stats against opponent_team_id
    # league_totals will be aggregate opponent stats for opponents of opponent_team_id
    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        stat_measure,
        seasons,
        season_types,
        entity_type,
        opponent_team_id=opponent_team_id
    )

    for stat in stats:
        print(stat)
    print(league_totals)
