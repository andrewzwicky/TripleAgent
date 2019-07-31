from collections import Counter

from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import MISSION_PLOT_ORDER, Missions


def _count_mission_choices(games: List[Game], data_dictionary: Counter):
    for game in games:
        for mission in Missions:
            if game.picked_missions & mission:
                data_dictionary[mission] += 1


def mission_choices(games: List[Game], title: str, **kwargs):
    default_kwargs = {"data_stack_order": MISSION_PLOT_ORDER}

    default_kwargs.update(kwargs)

    query(games, title, _count_mission_choices, **default_kwargs)
