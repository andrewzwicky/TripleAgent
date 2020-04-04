from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)

_NOSTOP = "NoStop"
_STOP = "Stop"


NOSTOP_PLOT_ORDER = [_NOSTOP, _STOP]


def _categorize_stop_talks(games, data_dictionary):
    # This is only checking whether a stop talk occured in a game
    # Not counting whether each start talk has a corresponding stop.
    for game in games:
        did_stop = None
        for timeline_event in game.timeline:
            if timeline_event.event == "stopped talking.":
                did_stop = True
                break

        if did_stop is None:
            data_dictionary[_NOSTOP] += 1
        else:
            data_dictionary[_STOP] += 1


def stop_talk_in_game_percentage(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict={
                _NOSTOP: axis_properties.plot_colors.color_1,
                _STOP: axis_properties.plot_colors.color_2,
            }
        ),
        DataQueryProperties(
            query_function=_categorize_stop_talks, primary_order=NOSTOP_PLOT_ORDER
        ),
    )

    return query(games, data_query, axis_properties)
