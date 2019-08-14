from collections import Counter

from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.missions import MISSION_PLOT_ORDER, Missions
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)


def _count_mission_choices(games: List[Game], data_dictionary: Counter):
    for game in games:
        for mission in Missions:
            if game.picked_missions & mission:
                data_dictionary[mission] += 1


def mission_choices(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        DataQueryProperties(
            query_function=_count_mission_choices, data_stack_order=MISSION_PLOT_ORDER
        ),
    )

    query(games, data_query, axis_properties)
