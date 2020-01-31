from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)
from triple_agent.constants.colors import PLOT_COLORS

_DIRECT = "direct"
_AT = "action test"

TRANSFER_TO_COLORS_RGB = {_DIRECT: PLOT_COLORS.color_1, _AT: PLOT_COLORS.color_2}
TRANSFER_PLOT_ORDER = [_DIRECT, _AT]


def _classify_microfilms(games, data_dictionary):
    for game in games:
        if game.completed_missions & Missions.Transfer:
            mf_moved = False
            for timeline_event in game.timeline:
                if timeline_event.event == "hide microfilm in book.":
                    if timeline_event.books[0] != timeline_event.books[1]:
                        mf_moved = True

                if (
                    timeline_event.category & TimelineCategory.MissionComplete
                    and timeline_event.mission == Missions.Transfer
                ):
                    break

            if mf_moved:
                data_dictionary[_AT] += 1
            else:
                data_dictionary[_DIRECT] += 1


def at_or_direct_mf(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(primary_color_dict=TRANSFER_TO_COLORS_RGB),
        DataQueryProperties(
            query_function=_classify_microfilms, primary_order=TRANSFER_PLOT_ORDER
        ),
    )

    return query(games, data_query, axis_properties)
