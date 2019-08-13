from collections import Counter
from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.outcomes import (
    WINTYPES_TO_COLORS,
    WINTYPE_PREFERRED_PIE_CHART_ORDER,
)
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
)


def _categorize_outcomes(games, data_dictionary):
    data_dictionary.update(Counter([game.win_type for game in games]))


def game_outcomes(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties = AxisProperties() if axis_properties is None else axis_properties
    data_query = DataQueryProperties() if data_query is None else data_query

    data_query.query_function = _categorize_outcomes
    data_query.data_stack_order = WINTYPE_PREFERRED_PIE_CHART_ORDER
    data_query.data_color_dict = WINTYPES_TO_COLORS

    query(games, data_query, axis_properties)
