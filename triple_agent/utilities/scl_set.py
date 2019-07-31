import itertools
from collections import Counter, defaultdict
from typing import List, Tuple

from triple_agent.utilities.outcomes import WinType
from triple_agent.utilities.game import Game


class SCLSet:
    def __init__(self, players: Tuple[str], games: List[Game]):
        self.players = players
        self.games = games
        self.score = self.__get_score()
        self.tie = self.score == [6, 6]
        self.division = games[0].division
        self.event = games[0].event
        self.week = games[0].week

    def __get_score(self):
        scores_dict = Counter()
        for game in self.games:
            if game.win_type & WinType.SpyWin:
                scores_dict[game.spy] += 1
            else:
                scores_dict[game.sniper] += 1

        return [scores_dict[p] for p in self.players]


def sort_games_into_sets(games: List[Game]):
    # make sure all games are from the same event
    sorted_games = sorted(games, key=lambda g: (g.week, g.division))
    assert len({game.event for game in sorted_games}) == 1

    all_sets = []

    for _, week_games in itertools.groupby(sorted_games, key=lambda g: g.week):
        for _, week_div_games in itertools.groupby(
            week_games, key=lambda g: g.division
        ):
            possible_pairings = defaultdict(list)
            participants = set()
            for game in week_div_games:
                participants.add(game.spy)
                participants.add(game.sniper)
                possible_pairings[tuple(sorted((game.spy, game.sniper)))].append(game)

            if len(participants) == len(possible_pairings.keys()) * 2:
                for pair, pairs_games in possible_pairings.items():
                    all_sets.append(SCLSet(pair, pairs_games))

    return all_sets
