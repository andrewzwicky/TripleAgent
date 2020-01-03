import os
from typing import List

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.game import game_unpickle, Game

def _yield_unpickled_games(pickle_folder):
    for f in os.listdir(pickle_folder):
        yield game_unpickle(os.path.join(pickle_folder, f))

def get_parsed_replays(
    game_filter, pickle_folder: str = REPLAY_PICKLE_FOLDER
) -> List[Game]:

    return list(filter(game_filter, _yield_unpickled_games(pickle_folder)))
