"""
NBA Stats Tracking
~~~~~~~~~~~~~~~~~~~~
A package to work with NBA player tracking stats from
`NBA Advanced Stats <https://www.stats.nba.com/>`_.
"""

REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
REFERER = "https://www.nba.com/stats/"
HEADERS = {
    "User-Agent": USER_AGENT,
    "Referer": REFERER,
    "Origin": "https://www.nba.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "Trailers",
}
