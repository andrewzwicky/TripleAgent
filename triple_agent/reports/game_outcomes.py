from collections import Counter
from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.outcomes import (
    WINTYPES_TO_COLORS,
    WINTYPE_PREFERRED_PIE_CHART_ORDER,
)


def _categorize_outcomes(games, data_dictionary):
    data_dictionary.update(Counter([game.win_type for game in games]))


def game_outcomes(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": WINTYPE_PREFERRED_PIE_CHART_ORDER,
        "data_color_dict": WINTYPES_TO_COLORS,
    }

    default_kwargs.update(kwargs)

    query(games, title, _categorize_outcomes, **default_kwargs)
