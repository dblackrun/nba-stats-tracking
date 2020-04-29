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
