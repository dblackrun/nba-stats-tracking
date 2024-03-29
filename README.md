[![PyPI version](https://badge.fury.io/py/nba-stats-tracking.svg)](https://badge.fury.io/py/nba-stats-tracking)

A package to work with NBA player tracking stats using the NBA Stats API.

# Features
* Works with both tracking stats and tracking shot stats
* Aggregate stats across multiple seasons
* Aggregate tracking shot stats across multiple filters (ex Wide Open and 18-22 seconds left on the shot clock)
* Generate game logs

# Installation
Tested on Python >=3.8
```
pip install nba_stats_tracking
```

# Resources
[Documentation](https://nba-stats-tracking.readthedocs.io/en/latest/)

# Notes
It looks like prior to 2018-19 blocked shots aren't included in the FGA tracking shot totals

# Local Development
Using [poetry](https://python-poetry.org/) for package managment. Install it first if it is not install on your system.

`git clone https://github.com/dblackrun/nba-stats-tracking.git`

`cd nba-stats-tracking`

Install dependencies:

`poetry install`

Activate virtualenv:

`poetry shell`

Install pre-commit:

`pre-commit install`