"""
NBA Stats Tracking
~~~~~~~~~~~~~~~~~~~~
A package to work with NBA player tracking stats from
`NBA Advanced Stats <https://www.stats.nba.com/>`_.
"""

REQUEST_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
REFERER = "http://stats.nba.com/"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Referer": REFERER,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

CATCH_SHOOT_MEASURE_TYPE = "CatchShoot"
DEFENSE_MEASURE_TYPE = "Defense"
DRIVES_MEASURE_TYPE = "Drives"
PASSING_MEASURE_TYPE = "Passing"
PULL_UP_MEASURE_TYPE = "PullUpShot"
REBOUNDING_MEASURE_TYPE = "Rebounding"
SHOOTING_MEASURE_TYPE = "Efficiency"
SPEED_MEASURE_TYPE = "SpeedDistance"
ELBOW_TOUCH_MEASURE_TYPE = "ElbowTouch"
PAINT_TOUCH_MEASURE_TYPE = "PaintTouch"
POST_TOUCH_MEASURE_TYPE = "PostTouch"
POSSESSIONS_MEASURE_TYPE = "Possessions"

REGULAR_SEASON_STRING = "Regular Season"
PLAYOFFS_STRING = "Playoffs"
PLAY_IN_STRING = "Play In"

PLAYER_STRING = "Player"
TEAM_STRING = "Team"

CLOSE_DEF_DIST_RANGES = [
    "",
    "0-2 Feet - Very Tight",
    "2-4 Feet - Tight",
    "4-6 Feet - Open",
    "6+ Feet - Wide Open",
]
SHOT_CLOCK_RANGES = [
    "",
    "24-22",
    "22-18 Very Early",
    "18-15 Early",
    "15-7 Average",
    "7-4 Late",
    "4-0 Very Late",
    "ShotClock Off",
]
SHOT_DIST_RANGES = ["", ">=10.0"]
TOUCH_TIME_RANGES = ["", "Touch < 2 Seconds", "Touch 2-6 Seconds", "Touch 6+ Seconds"]
DRIBBLE_RANGES = [
    "",
    "0 Dribbles",
    "1 Dribble",
    "2 Dribbles",
    "3-6 Dribbles",
    "7+ Dribbles",
]
GENERAL_RANGES = ["Overall", "Catch and Shoot", "Pullups", "Less Than 10 ft"]
