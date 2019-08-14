from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.books import Books
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)

_DIRECT = "direct"
_AT = "action test"

TRANSFER_TO_COLORS_RGB = {_DIRECT: "xkcd:sea blue", _AT: "xkcd:pumpkin"}
TRANSFER_PLOT_ORDER = [_DIRECT, _AT]

BOOK_PLOT_LABEL_DICT = {
    (Books.Red, Books.Green): "Red->Green",
    (Books.Blue, Books.Green): "Blue->Green",
    (Books.Yellow, Books.Green): "Yellow->Green",
    (Books.Red, Books.Blue): "Red->Blue",
    (Books.Green, Books.Blue): "Green->Blue",
    (Books.Yellow, Books.Blue): "Yellow->Blue",
    (Books.Red, Books.Yellow): "Red->Yellow",
    (Books.Green, Books.Yellow): "Green->Yellow",
    (Books.Blue, Books.Yellow): "Blue->Yellow",
    (Books.Yellow, Books.Red): "Red->Red",
    (Books.Green, Books.Red): "Green->Red",
    (Books.Blue, Books.Red): "Blue->Red",
}


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


def _microfilm_direction(games, data_dictionary):
    for game in games:
        if game.completed_missions & Missions.Transfer:
            for timeline_event in game.timeline:
                if (
                    timeline_event.category & TimelineCategory.MissionComplete
                    and timeline_event.mission == Missions.Transfer
                ):
                    data_dictionary[BOOK_PLOT_LABEL_DICT[timeline_event.books]] += 1


def at_or_direct_mf(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        DataQueryProperties(
            query_function=_classify_microfilms,
            data_stack_order=TRANSFER_PLOT_ORDER,
            data_color_dict=TRANSFER_TO_COLORS_RGB,
        ),
    )

    query(games, data_query, axis_properties)


def microfilm_direction(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        DataQueryProperties(
            query_function=_microfilm_direction,
            data_stack_order=TRANSFER_PLOT_ORDER,
            data_color_dict=TRANSFER_TO_COLORS_RGB,
        ),
    )

    query(games, data_query, axis_properties)
