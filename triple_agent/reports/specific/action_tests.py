from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.action_tests import (
    AT_TO_COLORS_RGB,
    AT_TO_COLORS_DARK_MODE,
)
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
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
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=AT_TO_COLORS_DARK_MODE
            if axis_properties.dark_mode
            else AT_TO_COLORS_RGB
        ),
        DataQueryProperties(
            query_function=_at_rates_excluding_difficults,
        ),
    )

    return query(games, data_query, axis_properties)


def diff_action_test_percentages(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=AT_TO_COLORS_DARK_MODE
            if axis_properties.dark_mode
            else AT_TO_COLORS_RGB
        ),
        DataQueryProperties(
            query_function=_difficult_at_rate,
        ),
    )

    return query(games, data_query, axis_properties)
