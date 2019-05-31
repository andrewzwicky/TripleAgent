from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.scl_set import SCLSet


def _count_scores(sets, data_dictionary):
    for this_set in sets:
        data_dictionary[tuple(sorted(this_set.score, reverse=True))] += 1


def _game_differential(games, data_dictionary):
    for game in games:
        data_dictionary[game.winner] += 1
        data_dictionary[game.spy if game.sniper == game.winner else game.sniper] -= 1


def scl_set_scores_categorize(games: List[Game], title: str, **kwargs):
    query(games, title, _count_scores, **kwargs)


def game_differential(games: List[Game], title: str, **kwargs):
    default_kwargs = {"force_bar": True}

    default_kwargs.update(kwargs)

    query(games, title, _game_differential, **default_kwargs)
