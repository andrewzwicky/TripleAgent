from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.action_tests import (
    AT_TO_COLORS_RGB,
    AT_PREFERRED_PIE_CHART_ORDER,
)
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    create_properties_if_none,
)


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


def action_test_percentages(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties, data_query = create_properties_if_none(axis_properties, data_query)

    data_query.query_function = _at_rates_excluding_difficults
    data_query.data_stack_order = AT_PREFERRED_PIE_CHART_ORDER
    data_query.data_color_dict = AT_TO_COLORS_RGB

    query(games, data_query, axis_properties)


def diff_action_test_percentages(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties, data_query = create_properties_if_none(axis_properties, data_query)

    data_query.query_function = _difficult_at_rate
    data_query.data_stack_order = AT_PREFERRED_PIE_CHART_ORDER
    data_query.data_color_dict = AT_TO_COLORS_RGB

    query(games, data_query, axis_properties)
