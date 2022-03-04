from nba_stats_tracking import helpers
from nba_stats_tracking.models.matchups import MatchupResults, MatchupsRequestParameters


def get_matchup_results_for_game_id(game_id: str) -> MatchupResults:
    """
    Makes API call to `NBA Advanced Stats <https://www.stats.nba.com/>`_ and returns MatchupResults object

    :param str game_id: nba.com game id
    :return: matchup results
    :rtype: MatchupResults
    """
    url = "https://stats.nba.com/stats/boxscorematchupsv3"
    parameters = MatchupsRequestParameters(
        GameID=game_id,
    )

    response_json = helpers.get_json_response(
        url, parameters.dict(by_alias=True, exclude_none=True)
    )

    return MatchupResults(**response_json["boxScoreMatchups"])
