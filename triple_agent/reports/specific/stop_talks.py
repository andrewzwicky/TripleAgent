from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    create_properties_if_none,
)

NOSTOP_TO_COLORS_RGB = {"NoStop": "xkcd:sea blue", "Stop": "xkcd:pumpkin"}

NOSTOP_PLOT_ORDER = list(NOSTOP_TO_COLORS_RGB.keys())


def _categorize_stop_talks(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.event == "stopped talking.":
                data_dictionary["Stop"] += 1
                continue

        data_dictionary["NoStop"] += 1


def stop_talk_in_game_percentage(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties, data_query = create_properties_if_none(axis_properties, data_query)

    data_query.query_function = _categorize_stop_talks
    data_query.data_stack_order = NOSTOP_PLOT_ORDER
    data_query.data_color_dict = NOSTOP_TO_COLORS_RGB

    query(games, data_query, axis_properties)
