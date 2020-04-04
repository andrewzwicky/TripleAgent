from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.roles import Roles
from triple_agent.classes.lights import (
    Lights,
    create_lights_color_dict,
)
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)
from triple_agent.classes.timeline import TimelineCategory


def _determine_spy_lights(games, data_dictionary):
    _determine_lights_games(games, data_dictionary, Roles.Spy)


def _determine_amba_lights(games, data_dictionary):
    _determine_lights_games(games, data_dictionary, Roles.Ambassador)


def _determine_lights_games(games, data_dictionary, role):
    for this_game in games:
        data_dictionary[end_light_status(this_game, role)] += 1


def end_light_status(game, role_in):
    for event in reversed(game.timeline):
        if (
            event.category & TimelineCategory.SniperLights
            and not (event.category & TimelineCategory.Books)
            and role_in in event.role
        ):
            if "less" in event.event:
                return Lights.Lowlight
            if "neutral" in event.event:
                return Lights.Neutral
            return Lights.Highlight

    return Lights.Neutral


def spy_lights(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=create_lights_color_dict(AxisProperties.plot_colors)
        ),
        DataQueryProperties(query_function=_determine_spy_lights,),
    )
    return query(games, data_query, axis_properties)


def amba_lights(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=create_lights_color_dict(AxisProperties.plot_colors)
        ),
        DataQueryProperties(query_function=_determine_amba_lights,),
    )
    return query(games, data_query, axis_properties)
