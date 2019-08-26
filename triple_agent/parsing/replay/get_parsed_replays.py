import os
from typing import List

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.game import game_unpickle, Game


def get_parsed_replays(
    game_filter, pickle_folder: str = REPLAY_PICKLE_FOLDER
) -> List[Game]:
    unfiltered_game_list = [
        game_unpickle(os.path.join(pickle_folder, f)) for f in os.listdir(pickle_folder)
    ]
    filtered_game_list = list(filter(game_filter, unfiltered_game_list))

    return filtered_game_list
