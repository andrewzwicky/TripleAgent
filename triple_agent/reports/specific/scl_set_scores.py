from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)


def _count_scores(sets, data_dictionary):
    for this_set in sets:
        data_dictionary[tuple(sorted(this_set.score, reverse=True))] += 1


def _game_differential(games, data_dictionary):
    for game in games:
        data_dictionary[game.winner] += 1
        data_dictionary[game.spy if game.sniper == game.winner else game.sniper] -= 1


def scl_set_scores_categorize(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties, data_query = initialize_properties(
        axis_properties, data_query, DataQueryProperties(query_function=_count_scores)
    )

    query(games, data_query, axis_properties)


def game_differential(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        DataQueryProperties(query_function=_game_differential),
    )

    query(games, data_query, axis_properties)
