from collections import defaultdict
from typing import List, Optional

from triple_agent.classes.game import Game
from triple_agent.classes.roles import Roles
from triple_agent.classes.characters import Characters
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.generic_query import query
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
)


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
            return event.cast_name[0].name

    return None


def spy_selection(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties = AxisProperties() if axis_properties is None else axis_properties
    data_query = DataQueryProperties() if data_query is None else data_query

    data_query.query_function = _determine_spy
    data_query.data_color_dict = defaultdict(lambda: "xkcd:green")

    axis_properties.force_bar = True
    axis_properties.x_axis_portrait = True

    query(games, data_query, axis_properties)


def st_selection(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties = AxisProperties() if axis_properties is None else axis_properties
    data_query = DataQueryProperties() if data_query is None else data_query

    data_query.query_function = _determine_st
    data_query.data_color_dict = defaultdict(lambda: "xkcd:light red")

    axis_properties.force_bar = True
    axis_properties.x_axis_portrait = True

    query(games, data_query, axis_properties)


def amba_selection(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties = AxisProperties() if axis_properties is None else axis_properties
    data_query = DataQueryProperties() if data_query is None else data_query

    data_query.query_function = _determine_amba
    data_query.data_color_dict = defaultdict(lambda: "xkcd:light magenta")

    axis_properties.force_bar = True
    axis_properties.x_axis_portrait = True

    query(games, data_query, axis_properties)


def double_agent_selection(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties = AxisProperties() if axis_properties is None else axis_properties
    data_query = DataQueryProperties() if data_query is None else data_query

    data_query.query_function = _determine_da
    data_query.data_color_dict = defaultdict(lambda: "xkcd:light yellow")

    axis_properties.force_bar = True
    axis_properties.x_axis_portrait = True

    query(games, data_query, axis_properties)
