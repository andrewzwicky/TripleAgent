from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.books import Books
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import Missions
from triple_agent.utilities.timeline import TimelineCategory

_DIRECT = "direct"
_AT = "action test"

TRANSFER_TO_COLORS_RGB = {_DIRECT: "xkcd:sea blue", _AT: "xkcd:pumpkin"}
TRANSFER_PLOT_ORDER = [_DIRECT, _AT]
TRANSFER_PLOT_COLOR = [
    TRANSFER_TO_COLORS_RGB[transfer_type] for transfer_type in TRANSFER_PLOT_ORDER
]

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


def at_or_direct_mf(games: List[Game], title: str, **kwargs):
    query(
        games,
        title,
        _classify_microfilms,
        TRANSFER_PLOT_ORDER,
        TRANSFER_PLOT_COLOR,
        **kwargs
    )


def microfilm_direction(games: List[Game], title: str, **kwargs):
    query(games, title, _microfilm_direction, **kwargs)
