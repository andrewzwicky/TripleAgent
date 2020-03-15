import os
from typing import List, Callable, Optional

import jsonpickle
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER, ALIAS_LIST_PATH
from triple_agent.classes.game import game_unpickle, Game


def _yield_unpickled_games(pickle_folder, alias_list: Optional[dict] = None):
    for file in os.listdir(pickle_folder):
        yield game_unpickle(os.path.join(pickle_folder, file), alias_list=alias_list)


def get_parsed_replays(
    game_filter: Callable = lambda game: True,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
    use_alias_list=True,
) -> List[Game]:

    alias_list = (
        jsonpickle.decode(open(ALIAS_LIST_PATH, "r").read()) if use_alias_list else None
    )

    return list(
        filter(
            game_filter, _yield_unpickled_games(pickle_folder, alias_list=alias_list)
        )
    )
