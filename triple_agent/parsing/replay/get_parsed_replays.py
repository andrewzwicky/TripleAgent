import os
from typing import List, Callable

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.game import game_unpickle, Game


def _yield_unpickled_games(pickle_folder):
    for file in os.listdir(pickle_folder):
        yield game_unpickle(os.path.join(pickle_folder, file))


def get_parsed_replays(
    game_filter: Callable = lambda game: True,
    pickle_folder: str = REPLAY_PICKLE_FOLDER
) -> List[Game]:

    return list(filter(game_filter, _yield_unpickled_games(pickle_folder)))
