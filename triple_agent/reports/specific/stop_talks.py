from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)
from triple_agent.constants.colors import PLOT_COLORS

NOSTOP_TO_COLORS_RGB = {"NoStop": PLOT_COLORS.color_1, "Stop": PLOT_COLORS.color_2}

NOSTOP_PLOT_ORDER = list(NOSTOP_TO_COLORS_RGB.keys())


def _categorize_stop_talks(games, data_dictionary):
    for game in games:
        did_stop = None
        for timeline_event in game.timeline:
            if timeline_event.event == "stopped talking.":
                did_stop = True
                break

        if did_stop is None:
            data_dictionary["NoStop"] += 1
        else:
            data_dictionary["Stop"] += 1


def stop_talk_in_game_percentage(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(primary_color_dict=NOSTOP_TO_COLORS_RGB),
        DataQueryProperties(
            query_function=_categorize_stop_talks, primary_order=NOSTOP_PLOT_ORDER
        ),
    )

    return query(games, data_query, axis_properties)
