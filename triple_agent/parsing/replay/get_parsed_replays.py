import os
from typing import List

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.game import game_unpickle, Game


def get_parsed_replays(
    game_filter, pickle_folder: str = REPLAY_PICKLE_FOLDER
) -> List[Game]:
    replay_pickle_paths = [
        os.path.join(pickle_folder, f) for f in os.listdir(pickle_folder)
    ]
    unfiltered_game_list = [game_unpickle(path) for path in replay_pickle_paths]
    filtered_game_list = list(filter(game_filter, unfiltered_game_list))

    return filtered_game_list
