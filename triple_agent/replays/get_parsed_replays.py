import os
from multiprocessing import Pool
from typing import List

from triple_agent.utilities.paths import REPLAY_PICKLE_FOLDER
from triple_agent.utilities.game import game_unpickle, Game


def get_parsed_replays(game_filter) -> List[Game]:
    pool = Pool(processes=4)

    try:
        replay_pickle_paths = [os.path.join(REPLAY_PICKLE_FOLDER, f) for f in os.listdir(REPLAY_PICKLE_FOLDER)]
        unfiltered_game_list = pool.map(game_unpickle, replay_pickle_paths)
        filtered_game_list = list(filter(game_filter, unfiltered_game_list))
    finally:
        pool.close()
        pool.join()

    return filtered_game_list
