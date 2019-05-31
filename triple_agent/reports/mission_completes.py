from collections import Counter, defaultdict
from typing import List, Dict

from triple_agent.reports.generic_query import query
from triple_agent.reports.report_utilities import create_bar_plot
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import (
    print_complete_string,
    MISSION_LETTERS_TO_ENUM,
    MISSIONS_ENUM_TO_COLOR,
    MISSION_PLOT_ORDER,
    Missions,
)


def _mission_completes(games, data_dictionary):
    for game in games:
        for m in Missions:
            if m & game.completed_missions:
                data_dictionary[m] += 1


def mission_completion_query(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": MISSION_PLOT_ORDER,
        "data_color_dict": MISSIONS_ENUM_TO_COLOR,
    }

    default_kwargs.update(kwargs)

    query(games, title, _mission_completes, **default_kwargs)
