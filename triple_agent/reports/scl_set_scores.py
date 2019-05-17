from collections import Counter
from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.reports.report_utilities import create_bar_plot
from triple_agent.utilities.game import Game
from triple_agent.utilities.scl_set import sort_games_into_sets


def _count_scores(games, data_dictionary):
    sets = sort_games_into_sets(games)
    for this_set in sets:
        # print(data_dictionary)
        data_dictionary[tuple(sorted(this_set.score, reverse=True))] += 1


def _game_differential(games, data_dictionary):
    sets = sort_games_into_sets(games)
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


def game_differential(games: List[Game], title: str):
    data_dictionary = Counter()
    _game_differential(games, data_dictionary)
    players, differentials = zip(*data_dictionary.most_common())
    create_bar_plot(title, [differentials[:20]], players[:20], label_rotation=90)

    create_bar_plot(
        title, [differentials[-20:][::-1]], players[-20:][::-1], label_rotation=90
    )

    abs_data_dictionary = Counter({k: abs(v) for k, v in data_dictionary.items()})

    players, _ = zip(*abs_data_dictionary.most_common())
    create_bar_plot(
        title,
        [[data_dictionary[p] for p in players[-20:][::-1]]],
        players[-20:][::-1],
        label_rotation=90,
    )
