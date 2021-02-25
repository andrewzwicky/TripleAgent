from collections import Counter
from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)

def _categorize_countdowns(games, data_dictionary):
    data_dictionary.update(Counter([game.did_reach_countdown() for game in games]))


def mission_win_countdown(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties=axis_properties,
        data_query=data_query,
        suggested_data_query=DataQueryProperties(
            query_function=_categorize_countdowns,
        ),
    )
    return query(games, data_query, axis_properties)
