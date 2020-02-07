[![Build Status](https://travis-ci.org/dblackrun/nba-stats-tracking.svg?branch=master)](https://travis-ci.org/dblackrun/nba-stats-tracking)

A package to work with NBA player tracking stats using the NBA Stats API.

# Features
* Works with both tracking stats and tracking shot stats
* Aggregate stats across multiple seasons
* Aggregate tracking shot stats across multiple filters (ex Wide Open and 18-22 seconds left on the shot clock)
* Generate game logs

# Installation
requires Python >=3.6
```
pip install nba_stats_tracking
```

# Example Usage

## Aggregating Multiple Tracking Shot Stat Filters and/or Seasons

```
from nba_stats_tracking import tracking_shots

seasons = ['2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']
season_types = ['Regular Season', 'Playoffs']
def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
general_ranges = ['Catch and Shoot']

stats, league_totals = tracking_shots.aggregate_full_season_tracking_shot_stats_for_seasons('player', seasons, season_types, close_def_dists=def_distances, general_ranges=general_ranges)

for stat in stats:
    print(stat)
print(league_totals)
```

`tracking_shots.aggregate_full_season_tracking_shot_stats_for_seasons` takes 3 required args `entity_type`, `seasons` and `season_types`

Options for `entity_type` are 'player', 'team' or 'opponent'

`seasons` is a list of seasons, format ex. '2018-19'

`season_types` is a list of season types. Season types are 'Regular Season' and 'Playoffs'

It also takes optional kwargs for each tracking shot filter option. The default for each filter is all shots for that filter.

```
close_def_dists - list, options are: '', '0-2 Feet - Very Tight','2-4 Feet - Tight','4-6 Feet - Open','6+ Feet - Wide Open'
shot_clocks - list, options are: '', '24-22', '22-18 Very Early', '18-15 Early', '15-7 Average', '7-4 Late', '4-0 Very Late', 'ShotClock Off'
shot_dists - list, options are: '', '>=10.0'
touch_times - list, options are: '', 'Touch < 2 Seconds', 'Touch 2-6 Seconds', 'Touch 6+ Seconds'
dribble_ranges - list, options are: '', '0 Dribbles', '1 Dribble', '2 Dribbles', '3-6 Dribbles', '7+ Dribbles'
general_ranges - list, options are: 'Overall', 'Catch and Shoot', 'Pullups', 'Less Than 10 ft'
```

## Generating Tracking Shot Game Logs

```
from nba_stats_tracking import tracking_shots

def_distances = ['6+ Feet - Wide Open', '4-6 Feet - Open']
general_ranges = ['Catch and Shoot']
date_from = '02/02/2020'
date_to = '02/03/2020'

game_logs = tracking_shots.generate_tracking_shot_game_logs('player', date_from, date_to, close_def_dists=def_distances, general_ranges=general_ranges)
for game_log in game_logs:
    print(game_log)
```

`tracking_shots.generate_tracking_shot_game_logs` takes 3 required args `entity_type`, `date_from` and `date_to`

Options for `entity_type` are 'player', 'team' or 'opponent'

`date_from` and `date_to` are strings formatted MM/DD/YYYY

It also takes optional kwargs for each tracking shot filter option the same way as above.

## Aggregating Multiple Seasons of Tracking Stats

```
from nba_stats_tracking import tracking

stat_measure = 'SpeedDistance'
seasons = ['2018-19', '2019-20']
season_types = ['Regular Season']
entity_type = 'player'
stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(stat_measure, seasons, season_types, entity_type)

for stat in stats:
    print(stat)

print('-----------------------')
print(league_totals)
```

`tracking.aggregate_full_season_tracking_stats_for_seasons` takes 4 args `stat_measure`, `seasons`, `season_types` and `entity_type`

Options for `stat_measure` are 'Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch'

`seasons` is a list of seasons, format ex. '2018-19'

`season_types` is a list of season types. Season types are 'Regular Season' and 'Playoffs'

Options for `entity_type` are 'player' or 'team'

## Generating Tracking Game Logs
```
from nba_stats_tracking import tracking

stat_measure = 'CatchShoot'
entity_type = 'player'
date_from = '02/02/2020'
date_to = '02/03/2020'

game_logs = tracking.generate_tracking_game_logs(stat_measure, entity_type, date_from, date_to)
for game_log in game_logs:
    print(game_log)
```

`tracking.generate_tracking_game_logs` takes 4 args `stat_measure`, `entity_type`, `date_from` and `date_to`

Options for `stat_measure` are 'Drives', 'Defense', 'CatchShoot', 'Passing', 'Possessions', 'PullUpShot', 'Rebounding', 'Efficiency', 'SpeedDistance', 'ElbowTouch', 'PostTouch', 'PaintTouch'

Options for `entity_type` are 'player' or 'team'

`date_from` and `date_to` are strings formatted MM/DD/YYYY
