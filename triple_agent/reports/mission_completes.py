from collections import defaultdict, Counter
from typing import List

from triple_agent.reports.report_utilities import create_bar_plot
from triple_agent.reports.plot_utilities import create_data_label
from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import (
    MISSIONS_ENUM_TO_COLOR,
    MISSION_PLOT_ORDER,
    MISSION_LETTERS_TO_ENUM,
    Missions,
)

_COMPLETE = "Complete"
_INCOMPLETE = "Incomplete"


def _mission_completes(games: List[Game], data_dictionary: Counter):
    for game in games:
        for mission in Missions:
            if mission & game.completed_missions:
                data_dictionary[mission] += 1


def mission_completion_query(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": MISSION_PLOT_ORDER,
        "data_color_dict": MISSIONS_ENUM_TO_COLOR,
    }

    default_kwargs.update(kwargs)

    query(games, title, _mission_completes, **default_kwargs)


# This is a very slightly different version of the other query methods, because this doesn't have a
# single counter value for each game, there are many pieces of data per game.
def _count_mission_available_and_complete(games: List[Game]):
    completion_dictionary = defaultdict(Counter)

    for game in games:
        for mission in Missions:
            if mission & game.completed_missions:
                completion_dictionary[mission][_COMPLETE] += 1
            elif mission & game.selected_missions:
                completion_dictionary[mission][_INCOMPLETE] += 1

    return completion_dictionary


def mission_completion(games: List[Game], title: str, **kwargs):
    completion_dictionary = _count_mission_available_and_complete(games)
    total_games = len(games)

    assert total_games > 0

    default_kwargs = {
        "data_stack_order": MISSION_PLOT_ORDER,
        "data_color_dict": MISSIONS_ENUM_TO_COLOR,
    }

    default_kwargs.update(kwargs)

    complete_bars = []
    incomplete_bars = []

    complete_labels = []
    incomplete_labels = []

    for mission in Missions:
        num_completes = completion_dictionary[mission][_COMPLETE]
        num_incompletes = completion_dictionary[mission][_INCOMPLETE]

        complete_bars.append(num_completes / total_games)
        complete_labels.append(create_data_label(num_completes, num_incompletes))

        incomplete_bars.append(num_incompletes / total_games)
        incomplete_labels.append(create_data_label(num_incompletes, total_games))

    create_bar_plot(
        title,
        [complete_bars, incomplete_bars],
        [m.name for m in MISSION_LETTERS_TO_ENUM.values()],
        bar_labels=[complete_labels, incomplete_labels],
        colors=["xkcd:green", "xkcd:light grey"],
        percentage=True,
    )
