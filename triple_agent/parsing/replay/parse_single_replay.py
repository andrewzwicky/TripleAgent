from pathlib import Path
from collections import defaultdict
from typing import Dict, AnyStr

from triple_agent.classes.game import Game, game_load_or_new
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.parsing.replay.parse_rply_file import (
    parse_rply_file,
    RplyParseException,
)


def get_replay_dict(replay_file: Path) -> defaultdict:
    try:
        return parse_rply_file(replay_file)
    except RplyParseException as rply_parse_exception:
        # re-raise exception about unreadable files
        # so issue can be resolved / files removed.
        print(f"{str(rply_parse_exception)} - {replay_file}")
        raise rply_parse_exception


def parse_replay_dict_into_game(
    replay_dict: Dict[str, AnyStr],
    replay_file: Path,
    pickle_folder: Path = REPLAY_PICKLE_FOLDER,
    **kwargs,
) -> Game:
    return game_load_or_new(replay_dict, pickle_folder, replay_file=replay_file, **kwargs)


def parse_single_replay(
    replay_file: Path, pickle_folder: Path = REPLAY_PICKLE_FOLDER, **kwargs
) -> Game:
    return parse_replay_dict_into_game(
        get_replay_dict(replay_file), replay_file, pickle_folder=pickle_folder, **kwargs
    )
