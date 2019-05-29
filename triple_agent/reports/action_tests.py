from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.action_tests import (
    AT_TO_COLORS_RGB,
    AT_PREFERRED_PIE_CHART_ORDER,
)
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import Missions
from triple_agent.utilities.timeline import TimelineCategory


def _normal_fingerprint_count(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.category & TimelineCategory.ActionTest:
                if timeline_event.mission != Missions.Fingerprint:
                    data_dictionary[timeline_event.action_test] += 1


def _difficult_fingerprint_count(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.category & TimelineCategory.ActionTest:
                if timeline_event.mission == Missions.Fingerprint:
                    data_dictionary[timeline_event.action_test] += 1


def action_test_percentages(games: List[Game], title: str, **kwargs):
    query(
        games,
        title,
        _normal_fingerprint_count,
        AT_PREFERRED_PIE_CHART_ORDER,
        AT_TO_COLORS_RGB,
        **kwargs,
    )


def diff_action_test_percentages(games: List[Game], title: str, **kwargs):
    query(
        games,
        title,
        _difficult_fingerprint_count,
        AT_PREFERRED_PIE_CHART_ORDER,
        AT_TO_COLORS_RGB,
        **kwargs,
    )
