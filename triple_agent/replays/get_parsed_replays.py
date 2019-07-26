import os
from multiprocessing import Pool
from typing import List

from triple_agent.utilities.paths import REPLAY_PICKLE_FOLDER
from triple_agent.utilities.game import game_unpickle, Game


def unpickle_game(replay_pickle_file: str) -> Game:
    unpickled_game = game_unpickle(
        os.path.join(REPLAY_PICKLE_FOLDER, replay_pickle_file)
    )
    if unpickled_game is not None:
        return unpickled_game


def get_parsed_replays(game_filter) -> List[Game]:
    pool = Pool(processes=4)

    try:
        unfiltered_game_list = pool.map(unpickle_game, os.listdir(REPLAY_PICKLE_FOLDER))
        filtered_game_list = list(filter(game_filter, unfiltered_game_list))
    finally:
        pool.close()
        pool.join()

    return filtered_game_list
