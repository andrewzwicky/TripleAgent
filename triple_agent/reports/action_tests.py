from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.classes.action_tests import (
    AT_TO_COLORS_RGB,
    AT_PREFERRED_PIE_CHART_ORDER,
)
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory


def _at_rates_excluding_difficults(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.category & TimelineCategory.ActionTest:
                if timeline_event.mission != Missions.Fingerprint:
                    data_dictionary[timeline_event.action_test] += 1


def _difficult_at_rate(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.category & TimelineCategory.ActionTest:
                if timeline_event.mission == Missions.Fingerprint:
                    data_dictionary[timeline_event.action_test] += 1


def action_test_percentages(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": AT_PREFERRED_PIE_CHART_ORDER,
        "data_color_dict": AT_TO_COLORS_RGB,
    }

    default_kwargs.update(kwargs)

    query(games, title, _at_rates_excluding_difficults, **default_kwargs)


def diff_action_test_percentages(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": AT_PREFERRED_PIE_CHART_ORDER,
        "data_color_dict": AT_TO_COLORS_RGB,
    }

    default_kwargs.update(kwargs)

    query(games, title, _difficult_at_rate, **default_kwargs)
