from collections import defaultdict
from typing import List, Optional

from triple_agent.utilities.game import Game
from triple_agent.utilities.roles import Roles
from triple_agent.utilities.characters import Characters
from triple_agent.utilities.timeline import TimelineCategory
from triple_agent.reports.generic_query import query


def _determine_spy(games, data_dictionary):
    _determine_role_games(games, data_dictionary, Roles.Spy)


def _determine_st(games, data_dictionary):
    _determine_role_games(games, data_dictionary, Roles.SeductionTarget)


def _determine_amba(games, data_dictionary):
    _determine_role_games(games, data_dictionary, Roles.Ambassador)


def _determine_da(games, data_dictionary):
    _determine_role_games(games, data_dictionary, Roles.DoubleAgents)


def _determine_role_games(games, data_dictionary, role):
    for this_game in games:
        cast = determine_character_in_role(this_game, role)
        if cast:
            data_dictionary[cast] += 1


def determine_character_in_role(game, role) -> Optional[Characters]:
    for event in game.timeline:
        if (event.category & TimelineCategory.Cast) and (role in event.role):
            return event.cast_name[0]

    return None


def spy_selection(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_color_dict": defaultdict(lambda: "xkcd:green"),
        "force_bar": True,
        "portrait_x_axis": True,
    }

    default_kwargs.update(kwargs)

    query(games, title, _determine_spy, **default_kwargs)


def st_selection(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_color_dict": defaultdict(lambda: "xkcd:light red"),
        "force_bar": True,
        "portrait_x_axis": True,
    }

    default_kwargs.update(kwargs)

    query(games, title, _determine_st, **default_kwargs)


def amba_selection(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_color_dict": defaultdict(lambda: "xkcd:light magenta"),
        "force_bar": True,
        "portrait_x_axis": True,
    }

    default_kwargs.update(kwargs)

    query(games, title, _determine_amba, **default_kwargs)


def double_agent_selection(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_color_dict": defaultdict(lambda: "xkcd:light yellow"),
        "force_bar": True,
        "portrait_x_axis": True,
    }

    default_kwargs.update(kwargs)

    query(games, title, _determine_da, **default_kwargs)
