from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.scl_set import SCLSet


def _count_scores(sets, data_dictionary):
    for this_set in sets:
        # print(data_dictionary)
        data_dictionary[tuple(sorted(this_set.score, reverse=True))] += 1


def _game_differential(sets, data_dictionary):
    for this_set in sets:
        # print(data_dictionary)
        player_a, player_b = this_set.players
        player_a_score, player_b_score = this_set.score

        data_dictionary[player_a] += player_a_score
        data_dictionary[player_a] -= player_b_score
        data_dictionary[player_b] += player_b_score
        data_dictionary[player_b] -= player_a_score


def scl_set_scores_categorize(games: List[Game], title: str, **kwargs):
    query(games, title, _count_scores, **kwargs)


def game_differential(sets: List[SCLSet], title: str, **kwargs):
    query(sets, title, _game_differential, **kwargs, force_bar=True)
