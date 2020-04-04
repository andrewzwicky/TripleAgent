from collections import Counter
from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.outcomes import (
    create_wintypes_color_dict,
    WINTYPE_PREFERRED_PIE_CHART_ORDER,
)
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)


def _categorize_outcomes(games, data_dictionary):
    data_dictionary.update(Counter([game.win_type for game in games]))


def game_outcomes(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=create_wintypes_color_dict(axis_properties.plot_colors)
        ),
        DataQueryProperties(
            query_function=_categorize_outcomes,
            primary_order=WINTYPE_PREFERRED_PIE_CHART_ORDER,
        ),
    )
    return query(games, data_query, axis_properties)
