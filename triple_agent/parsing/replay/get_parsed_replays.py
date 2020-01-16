from typing import List
from multiprocessing import Pool, cpu_count
from pathlib import Path

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.game import game_unpickle, Game


def get_parsed_replays(
    game_filter, pickle_folder: str = REPLAY_PICKLE_FOLDER
) -> List[Game]:
    pool = Pool(processes=cpu_count() * 2)

    try:
        games = pool.map(game_unpickle, Path(pickle_folder).iterdir())
    finally:
        pool.close()
        pool.join()

    return list(filter(game_filter, games))
