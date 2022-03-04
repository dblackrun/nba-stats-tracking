import json
from ast import alias
from datetime import date

import responses
from furl import furl

from nba_stats_tracking import tracking
from nba_stats_tracking.models.request import SeasonType
from nba_stats_tracking.models.tracking import (
    CatchAndShootItem,
    DefenseItem,
    DrivesItem,
    ElbowTouchesItem,
    PaintTouchesItem,
    PassingItem,
    PlayerOrTeam,
    PossessionsItem,
    PostTouchesItem,
    PullUpItem,
    ReboundingItem,
    TrackingMeasureType,
)


# Helper function for generating urls for registering mock responses
def generate_url(measure_type, season, season_type, entity_type, OpponentTeamID=0):
    base_url = "https://stats.nba.com/stats/leaguedashptstats"
    query_params = {
        "PlayerOrTeam": entity_type,
        "PtMeasureType": measure_type,
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": "",
        "DateTo": "",
        "GameScope": "",
        "LastNGames": 0,
        "LeagueID": "00",
        "Location": "",
        "Month": 0,
        "OpponentTeamID": OpponentTeamID,
        "Outcome": "",
        "PerMode": "Totals",
        "PlayerExperience": "",
        "PlayerPosition": "",
        "SeasonSegment": "",
        "StarterBench": "",
        "VsConference": "",
        "VsDivision": "",
    }
    url = furl(base_url).add(query_params).url
    return url


@responses.activate
def test_team_aggregate_full_season_tracking_stats_for_seasons():
    with open("tests/data/tracking/2019-20/team-regular-season/CatchShoot.json") as f:
        tracking_2020_response_json = json.loads(f.read())

    with open("tests/data/tracking/2018-19/team-regular-season/CatchShoot.json") as f:
        tracking_2019_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.catch_and_shoot
    seasons = ["2018-19", "2019-20"]
    season_types = [SeasonType.regular_season]

    url_2020 = generate_url(measure_type, seasons[1], season_types[0], entity_type)
    responses.add(responses.GET, url_2020, json=tracking_2020_response_json, status=200)

    url_2019 = generate_url(measure_type, seasons[0], season_types[0], entity_type)
    responses.add(responses.GET, url_2019, json=tracking_2019_response_json, status=200)

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, seasons, season_types, entity_type
    )
    minutes = 0
    assert len(stats) == 30
    for stat in stats:
        if stat.team_id == 1610612737:
            assert stat.team_name == "Atlanta Hawks"
            assert stat.team_abbreviation == "ATL"
            assert stat.minutes == 36135.0
            assert stat.fgm == 1406
            assert stat.fga == 3962
            assert stat.points == 4141
            assert stat.fg3m == 1329
            assert stat.fg3a == 3719
            assert stat.fg3pct == stat.fg3m / stat.fg3a
        minutes += stat.minutes

    assert league_totals.minutes == 1106520.0
    assert league_totals.fgm == 44236
    assert league_totals.fga == 117893
    assert league_totals.points == 127215
    assert league_totals.fg3m == 38743
    assert league_totals.fg3a == 105039


@responses.activate
def test_player_aggregate_full_season_tracking_stats_for_seasons():
    with open(
        "tests/data/tracking/2019-20/player-regular-season/SpeedDistance.json"
    ) as f:
        tracking_2020_response_json = json.loads(f.read())

    with open(
        "tests/data/tracking/2018-19/player-regular-season/SpeedDistance.json"
    ) as f:
        tracking_2019_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.speed_distance
    seasons = ["2018-19", "2019-20"]
    season_types = [SeasonType.regular_season]

    url_2020 = generate_url(measure_type, seasons[1], season_types[0], entity_type)
    responses.add(responses.GET, url_2020, json=tracking_2020_response_json, status=200)

    url_2019 = generate_url(measure_type, seasons[0], season_types[0], entity_type)
    responses.add(responses.GET, url_2019, json=tracking_2019_response_json, status=200)

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, seasons, season_types, entity_type
    )
    assert len(stats) == 659
    for stat in stats:
        if stat.player_id == 203932:
            assert stat.minutes == 4584.0
            assert stat.dist_feet == 1821576
    assert league_totals.minutes == 1101624.0
    assert league_totals.dist_feet == 434945971


@responses.activate
def test_get_tracking_results_for_team_catch_shoot():
    with open("tests/data/tracking/2019-20/team-playoffs/CatchShoot.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.catch_and_shoot
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.fga == 408
            assert stat.fg3pct == stat.fg3m / stat.fg3a
            assert round(stat.efg, 3) == 0.542

    assert league_totals.fga == 4477


@responses.activate
def test_get_tracking_results_for_player_catch_shoot():
    with open("tests/data/tracking/2019-20/player-regular-season/CatchShoot.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.catch_and_shoot
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, league_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.points == 184
            assert stat.fgm == 66
            assert stat.fga == 198
            assert stat.fg3m == 52
            assert stat.fg3a == 160
            assert stat.fg3pct == stat.fg3m / stat.fg3a
            assert round(stat.efg, 3) == 0.465

    assert league_totals.fga == 54954


@responses.activate
def test_get_tracking_results_for_team_defense():
    with open("tests/data/tracking/2019-20/team-playoffs/Defense.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.defense
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.def_rim_fga == 400
            assert stat.blocks == 82
            assert stat.def_rim_fgpct == stat.def_rim_fgm / stat.def_rim_fga


@responses.activate
def test_get_tracking_results_for_player_defense():
    with open("tests/data/tracking/2019-20/player-regular-season/Defense.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.defense
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.def_rim_fga == 185
            assert stat.blocks == 39
            assert stat.def_rim_fgpct == stat.def_rim_fgm / stat.def_rim_fga


@responses.activate
def test_get_tracking_results_for_team_drives():
    with open("tests/data/tracking/2019-20/team-playoffs/Drives.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.drives
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.drives == 764
            assert stat.passes == 306
            assert stat.pass_pct == stat.passes / stat.drives
            assert stat.assist_pct == stat.assists / stat.drives
            assert stat.turnover_pct == stat.turnovers / stat.drives
            assert stat.foul_pct == stat.fouls / stat.drives
            assert stat.pts_per_drive == stat.points / stat.drives


@responses.activate
def test_get_tracking_results_for_player_drives():
    with open("tests/data/tracking/2019-20/player-regular-season/Drives.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.drives
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.drives == 296
            assert stat.passes == 104
            assert stat.pass_pct == stat.passes / stat.drives
            assert stat.assist_pct == stat.assists / stat.drives
            assert stat.turnover_pct == stat.turnovers / stat.drives
            assert stat.foul_pct == stat.fouls / stat.drives
            assert stat.pts_per_drive == stat.points / stat.drives


@responses.activate
def test_get_tracking_results_for_team_efficiency():
    with open("tests/data/tracking/2019-20/team-playoffs/Efficiency.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.shooting
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.drive_pts == 436
            assert stat.catch_shoot_pts == 454
            assert stat.pull_up_pts == 409
            assert stat.paint_touch_pts == 292
            assert stat.post_touch_pts == 55
            assert stat.elbow_touch_pts == 92


@responses.activate
def test_get_tracking_results_for_player_efficiency():
    with open("tests/data/tracking/2019-20/player-regular-season/Efficiency.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.shooting
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.drive_pts == 145
            assert stat.catch_shoot_pts == 193
            assert stat.pull_up_pts == 142
            assert stat.paint_touch_pts == 262
            assert stat.post_touch_pts == 109
            assert stat.elbow_touch_pts == 43


@responses.activate
def test_get_tracking_results_for_team_elbow_touch():
    with open("tests/data/tracking/2019-20/team-playoffs/ElbowTouch.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.elbow_touches
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.elbow_touches == 140
            assert stat.points == 92
            assert stat.pass_pct == stat.passes / stat.elbow_touches
            assert stat.assist_pct == stat.assists / stat.elbow_touches
            assert stat.turnover_pct == stat.turnovers / stat.elbow_touches
            assert stat.foul_pct == stat.fouls / stat.elbow_touches
            assert stat.pts_per_elbow_touch == stat.points / stat.elbow_touches


@responses.activate
def test_get_tracking_results_for_player_elbow_touch():
    with open("tests/data/tracking/2019-20/player-regular-season/ElbowTouch.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.elbow_touches
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.elbow_touches == 110
            assert stat.points == 43
            assert stat.pass_pct == stat.passes / stat.elbow_touches
            assert stat.assist_pct == stat.assists / stat.elbow_touches
            assert stat.turnover_pct == stat.turnovers / stat.elbow_touches
            assert stat.foul_pct == stat.fouls / stat.elbow_touches
            assert stat.pts_per_elbow_touch == stat.points / stat.elbow_touches


@responses.activate
def test_get_tracking_results_for_team_paint_touch():
    with open("tests/data/tracking/2019-20/team-playoffs/PaintTouch.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.paint_touches
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.paint_touches == 346
            assert stat.points == 292
            assert stat.pass_pct == stat.passes / stat.paint_touches
            assert stat.assist_pct == stat.assists / stat.paint_touches
            assert stat.turnover_pct == stat.turnovers / stat.paint_touches
            assert stat.foul_pct == stat.fouls / stat.paint_touches
            assert stat.pts_per_paint_touch == stat.points / stat.paint_touches


@responses.activate
def test_get_tracking_results_for_player_paint_touch():
    with open("tests/data/tracking/2019-20/player-regular-season/PaintTouch.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.paint_touches
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.paint_touches == 267
            assert stat.points == 262
            assert stat.pass_pct == stat.passes / stat.paint_touches
            assert stat.assist_pct == stat.assists / stat.paint_touches
            assert stat.turnover_pct == stat.turnovers / stat.paint_touches
            assert stat.foul_pct == stat.fouls / stat.paint_touches
            assert stat.pts_per_paint_touch == stat.points / stat.paint_touches


@responses.activate
def test_get_tracking_results_for_team_passing():
    with open("tests/data/tracking/2019-20/team-playoffs/Passing.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.passing
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.passes_made == 4690
            assert stat.assists == 385
            assert stat.potential_assists == 722
            assert stat.pts_per_assist == stat.assist_pts / stat.assists
            assert stat.assists_per_pass == stat.assists / stat.passes_made
            assert (
                stat.potential_assists_per_pass
                == stat.potential_assists / stat.passes_made
            )


@responses.activate
def test_get_tracking_results_for_player_passing():
    with open("tests/data/tracking/2019-20/player-regular-season/Passing.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.passing
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.passes_made == 2223
            assert stat.assists == 228
            assert stat.potential_assists == 424
            assert stat.pts_per_assist == stat.assist_pts / stat.assists
            assert stat.assists_per_pass == stat.assists / stat.passes_made
            assert (
                stat.potential_assists_per_pass
                == stat.potential_assists / stat.passes_made
            )


@responses.activate
def test_get_tracking_results_for_team_possessions():
    with open("tests/data/tracking/2019-20/team-playoffs/Possessions.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.possessions
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.touches == 6711
            assert stat.time_of_poss == 358.2
            assert stat.pts_per_touch == stat.points / stat.touches


@responses.activate
def test_get_tracking_results_for_player_possessions():
    with open(
        "tests/data/tracking/2019-20/player-regular-season/Possessions.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.possessions
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.touches == 3286
            assert stat.time_of_poss == 158
            assert stat.pts_per_touch == stat.points / stat.touches


@responses.activate
def test_get_tracking_results_for_team_post_touch():
    with open("tests/data/tracking/2019-20/team-playoffs/PostTouch.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.post_touches
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.post_touches == 69
            assert stat.points == 55
            assert stat.pass_pct == stat.passes / stat.post_touches
            assert stat.assist_pct == stat.assists / stat.post_touches
            assert stat.turnover_pct == stat.turnovers / stat.post_touches
            assert stat.foul_pct == stat.fouls / stat.post_touches
            assert stat.pts_per_post_touch == stat.points / stat.post_touches


@responses.activate
def test_get_tracking_results_for_player_post_touch():
    with open("tests/data/tracking/2019-20/player-regular-season/PostTouch.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.post_touches
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.post_touches == 198
            assert stat.points == 109
            assert stat.pass_pct == stat.passes / stat.post_touches
            assert stat.assist_pct == stat.assists / stat.post_touches
            assert stat.turnover_pct == stat.turnovers / stat.post_touches
            assert stat.foul_pct == stat.fouls / stat.post_touches
            assert stat.pts_per_post_touch == stat.points / stat.post_touches


@responses.activate
def test_get_tracking_results_for_team_pullup_shoot():
    with open("tests/data/tracking/2019-20/team-playoffs/PullUpShot.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.pull_up
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.fga == 463
            assert stat.fg3pct == stat.fg3m / stat.fg3a
            assert round(stat.efg, 3) == 0.442


@responses.activate
def test_get_tracking_results_for_player_pullup_shoot():
    with open("tests/data/tracking/2019-20/player-regular-season/PullUpShot.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.pull_up
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.fga == 217
            assert stat.fg3pct == stat.fg3m / stat.fg3a
            assert round(stat.efg, 3) == 0.327


@responses.activate
def test_get_tracking_results_for_team_rebounding():
    with open("tests/data/tracking/2019-20/team-playoffs/Rebounding.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.rebounding
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.oreb_contest == 89
            assert stat.dreb_contest == 139
            assert stat.contested_oreb_pct == stat.oreb_contest / stat.oreb
            assert stat.contested_dreb_pct == stat.dreb_contest / stat.dreb


@responses.activate
def test_get_tracking_results_for_player_rebounding():
    with open("tests/data/tracking/2019-20/player-regular-season/Rebounding.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.rebounding
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.oreb_contest == 72
            assert stat.dreb_contest == 93
            assert stat.contested_oreb_pct == stat.oreb_contest / stat.oreb
            assert stat.contested_dreb_pct == stat.dreb_contest / stat.dreb


@responses.activate
def test_get_tracking_results_for_team_speed_distance():
    with open("tests/data/tracking/2019-20/team-playoffs/SpeedDistance.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.speed_distance
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 16

    for stat in stats:
        if stat.team_id == 1610612738:
            assert stat.season == f"{season} {season_type}"
            assert stat.minutes == 4155.0
            assert stat.dist_miles == 301.0
            assert stat.dist_miles_off == 161.5
            assert stat.dist_miles_def == 139.5


@responses.activate
def test_get_tracking_results_for_player_speed_distance():
    with open(
        "tests/data/tracking/2019-20/player-regular-season/SpeedDistance.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.speed_distance
    season = "2019-20"
    season_type = SeasonType.regular_season

    url = generate_url(measure_type, season, season_type, entity_type)

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    stats, _ = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type
    )
    assert len(stats) == 529

    for stat in stats:
        if stat.player_id == 203932:
            assert stat.season == f"{season} {season_type}"
            assert stat.team_id == 1610612753
            assert stat.minutes == 2017.0
            assert stat.dist_miles == 150.5
            assert stat.dist_miles_off == 83.4
            assert stat.dist_miles_def == 67.2


@responses.activate
def test_get_tracking_results_for_opponent_catch_shoot():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/CatchShoot.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.catch_and_shoot
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 72


@responses.activate
def test_get_tracking_results_for_opponent_defense():
    with open("tests/data/tracking/2019-20/opponent-regular-season/Defense.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.defense
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_drives():
    with open("tests/data/tracking/2019-20/opponent-regular-season/Drives.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.drives
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_efficiency():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/Efficiency.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.shooting
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_elbow_touch():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/ElbowTouch.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.elbow_touches
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_paint_touch():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/PaintTouch.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.paint_touches
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_passing():
    with open("tests/data/tracking/2019-20/opponent-regular-season/Passing.json") as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.passing
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_possessions():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/Possessions.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.possessions
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_post_touch():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/PostTouch.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.post_touches
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_pullup_shoot():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/PullUpShot.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.pull_up
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 72


@responses.activate
def test_get_tracking_results_for_opponent_rebounding():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/Rebounding.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.rebounding
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_get_tracking_results_for_opponent_speed_distance():
    with open(
        "tests/data/tracking/2019-20/opponent-regular-season/SpeedDistance.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.team
    measure_type = TrackingMeasureType.speed_distance
    season = "2019-20"
    season_type = SeasonType.playoffs

    url = generate_url(
        measure_type, season, season_type, entity_type, OpponentTeamID=1610612761
    )

    responses.add(responses.GET, url, json=tracking_response_json, status=200)

    _, opponent_totals = tracking.aggregate_full_season_tracking_stats_for_seasons(
        measure_type, [season], [season_type], entity_type, OpponentTeamID=1610612761
    )
    assert opponent_totals.games_played == 71


@responses.activate
def test_generate_tracking_game_logs():
    with open("tests/data/scoreboard/response.json") as f:
        scoreboard_response = json.loads(f.read())
    scoreboard_response["resultSets"][0]["rowSet"] = [
        [
            "2020-02-02T00:00:00",
            4,
            "0021900740",
            3,
            "Final",
            "20200202/CHITOR",
            1610612761,
            1610612741,
            "2019",
            4,
            "     ",
            None,
            "TSN1/4",
            "NBCSCH",
            "Q4       - ",
            "Scotiabank Arena",
            1,
        ]
    ]
    scoreboard_response_url = "https://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&GameDate=2020-02-02"

    responses.add(
        responses.GET, scoreboard_response_url, json=scoreboard_response, status=200
    )

    game_id = "0021900740"
    with open(f"tests/data/game/boxscore/{game_id}.json") as f:
        game_response_json = json.loads(f.read())

    boxscore_url = "https://stats.nba.com/stats/boxscoretraditionalv2"
    query_params = {
        "GameId": game_id,
        "StartPeriod": 0,
        "EndPeriod": 10,
        "RangeType": 2,
        "StartRange": 0,
        "EndRange": 55800,
    }
    url = furl(boxscore_url).add(query_params).url

    responses.add(responses.GET, url, json=game_response_json, status=200)

    with open(
        "tests/data/tracking/2019-20/player-regular-season/CatchShootByDate.json"
    ) as f:
        tracking_response_json = json.loads(f.read())

    entity_type = PlayerOrTeam.player
    measure_type = TrackingMeasureType.catch_and_shoot
    season = "2019-20"
    season_type = SeasonType.regular_season
    game_date = date(2020, 2, 2)

    base_url = "https://stats.nba.com/stats/leaguedashptstats"
    query_params = {
        "PlayerOrTeam": entity_type,
        "PtMeasureType": measure_type,
        "Season": season,
        "SeasonType": season_type,
        "DateFrom": game_date.strftime("%m/%d/%Y"),
        "DateTo": game_date.strftime("%m/%d/%Y"),
        "GameScope": "",
        "LastNGames": 0,
        "LeagueID": "00",
        "Location": "",
        "Month": 0,
        "OpponentTeamID": 0,
        "Outcome": "",
        "PerMode": "PerGame",
        "PlayerExperience": "",
        "PlayerPosition": "",
        "SeasonSegment": "",
        "StarterBench": "",
        "VsConference": "",
        "VsDivision": "",
    }
    tracking_url = furl(base_url).add(query_params).url

    responses.add(responses.GET, tracking_url, json=tracking_response_json, status=200)

    game_logs = tracking.generate_tracking_game_logs(
        measure_type, entity_type, game_date, game_date
    )
    assert len(game_logs) == 24
    for game_log in game_logs:
        if game_log.player_id == 1627832:
            assert game_log.player_name == "Fred VanVleet"
            assert game_log.team_id == 1610612761
            assert game_log.team_abbreviation == "TOR"
            assert game_log.games_played == 1
            assert game_log.wins == 1
            assert game_log.losses == 0
            assert game_log.minutes == 32.0
            assert game_log.fgm == 1
            assert game_log.fga == 5
            assert game_log.points == 3
            assert game_log.fg3m == 1
            assert game_log.fg3a == 5
            assert game_log.fg3pct == 0.2
            assert game_log.efg == 0.3
            assert game_log.season == "2019-20 Regular Season"
            assert game_log.game_id == "0021900740"
            assert game_log.opponent_team_id == 1610612741


def test_catch_and_shoot_0_as_denominator_returns_0_pct():
    a = CatchAndShootItem(
        TEAM_ID=0, TEAM_ABBREVIATION="", CATCH_SHOOT_FG3A=0, CATCH_SHOOT_FGA=0
    )
    assert a.fg3pct == 0
    assert a.efg == 0


def test_defense_0_as_denominator_returns_0_pct():
    a = DefenseItem(TEAM_ID=0, TEAM_ABBREVIATION="", DEF_RIM_FGA=0)
    assert a.def_rim_fgpct == 0


def test_drives_0_as_denominator_returns_0_pct():
    a = DrivesItem(TEAM_ID=0, TEAM_ABBREVIATION="", DRIVES=0)
    assert a.pass_pct == 0
    assert a.assist_pct == 0
    assert a.turnover_pct == 0
    assert a.foul_pct == 0
    assert a.pts_per_drive == 0


def test_elbow_touches_0_as_denominator_returns_0_pct():
    a = ElbowTouchesItem(TEAM_ID=0, TEAM_ABBREVIATION="", ELBOW_TOUCHES=0)
    assert a.pass_pct == 0
    assert a.assist_pct == 0
    assert a.turnover_pct == 0
    assert a.foul_pct == 0
    assert a.pts_per_elbow_touch == 0


def test_paint_touches_0_as_denominator_returns_0_pct():
    a = PaintTouchesItem(TEAM_ID=0, TEAM_ABBREVIATION="", ELBOW_TOUCHES=0)
    assert a.pass_pct == 0
    assert a.assist_pct == 0
    assert a.turnover_pct == 0
    assert a.foul_pct == 0
    assert a.pts_per_paint_touch == 0


def test_passing_0_as_denominator_returns_0_pct():
    a = PassingItem(TEAM_ID=0, TEAM_ABBREVIATION="", AST=0, PASSES_MADE=0)
    assert a.pts_per_assist == 0
    assert a.assists_per_pass == 0
    assert a.potential_assists_per_pass == 0


def test_possessions_0_as_denominator_returns_0_pct():
    a = PossessionsItem(TEAM_ID=0, TEAM_ABBREVIATION="", TOUCHES=0)
    assert a.pts_per_touch == 0


def test_post_touches_0_as_denominator_returns_0_pct():
    a = PostTouchesItem(TEAM_ID=0, TEAM_ABBREVIATION="", ELBOW_TOUCHES=0)
    assert a.pass_pct == 0
    assert a.assist_pct == 0
    assert a.turnover_pct == 0
    assert a.foul_pct == 0
    assert a.pts_per_post_touch == 0


def test_pull_up_0_as_denominator_returns_0_pct():
    a = PullUpItem(TEAM_ID=0, TEAM_ABBREVIATION="", PULL_UP_FG3A=0, PULL_UP_FGA=0)
    assert a.fg3pct == 0
    assert a.efg == 0


def test_rebounding_0_as_denominator_returns_0_pct():
    a = ReboundingItem(TEAM_ID=0, TEAM_ABBREVIATION="", OREB=0, DREB=0)
    assert a.contested_oreb_pct == 0
    assert a.contested_dreb_pct == 0


def test_sum_tracking_totals_for_not_entity_returns_empty_list():
    a = tracking.sum_tracking_totals(
        "asdgsd",
        TrackingMeasureType.catch_and_shoot,
        [ReboundingItem(TEAM_ID=0, TEAM_ABBREVIATION="", OREB=0, DREB=0)],
    )
    assert a == []
