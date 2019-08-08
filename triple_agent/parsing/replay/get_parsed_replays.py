import os
from multiprocessing import Pool
from typing import List

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.game import game_unpickle, Game


def get_parsed_replays(
    game_filter, pickle_folder: str = REPLAY_PICKLE_FOLDER
) -> List[Game]:
    pool = Pool(processes=4)

    try:
        replay_pickle_paths = [
            os.path.join(pickle_folder, f) for f in os.listdir(pickle_folder)
        ]
        unfiltered_game_list = pool.map(game_unpickle, replay_pickle_paths)
        filtered_game_list = list(filter(game_filter, unfiltered_game_list))
    finally:
        pool.close()
        pool.join()

    return filtered_game_list
