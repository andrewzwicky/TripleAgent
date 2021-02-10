from pathlib import Path
from typing import List, Callable, Optional, Iterator

import jsonpickle
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER, ALIAS_LIST_PATH
from triple_agent.classes.game import game_unpickle, Game


def _yield_unpickled_games(
    pickle_folder: Path, alias_list: Optional[dict] = None
) -> Iterator[Game]:
    for file in pickle_folder.iterdir():
        if (unpickled_game := game_unpickle(file, alias_list=alias_list)) is not None:
            yield unpickled_game


def get_parsed_replays(
    pickle_folder: Path,
    game_filter: Callable = lambda game: True,
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
