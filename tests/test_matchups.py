import json

import responses
from furl import furl

from nba_stats_tracking import matchups


@responses.activate
def test_get_matchup_results():
    game_id = "0022100831"
    with open(f"tests/data/game/matchups/{game_id}.json") as f:
        matchups_response = json.loads(f.read())

    base_url = "https://stats.nba.com/stats/boxscorematchupsv3"

    query_params = {
        "GameID": game_id,
        "startPeriod": 0,
        "endPeriod": 10,
        "rangeType": 0,
        "startRange": 0,
        "endRange": 55800,
    }
    url = furl(base_url).add(query_params).url
    responses.add(responses.GET, url, json=matchups_response, status=200)

    matchup_results = matchups.get_matchup_results_for_game_id(game_id)
    assert matchup_results.game_id == game_id
    assert matchup_results.home_team_id == 1610612765
    assert len(matchup_results.home_team.players) == 10
    assert matchup_results.home_team.players[0].player_id == 1630180
    assert matchup_results.home_team.players[0].matchups[0].player_id == 203500
    assert (
        matchup_results.home_team.players[0].matchups[0].statistics.minutes_str
        == "0:31"
    )
    assert matchup_results.home_team.players[0].matchups[0].statistics.seconds == 31
