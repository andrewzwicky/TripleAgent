from pathlib import Path
import os
from shutil import rmtree, copyfile

from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.constants.paths import (
    SPECTATE_REPLAYS_FOLDER,
    LONG_FILE_HEADER,
    ALL_EVENTS_FOLDER,
)


def extract_spectate_replays(
    game_filter,
    spectate_folder: Path = SPECTATE_REPLAYS_FOLDER,
    events_folder: Path = ALL_EVENTS_FOLDER,
):
    try:
        rmtree(spectate_folder)
    except FileNotFoundError:
        pass
    os.makedirs(spectate_folder, exist_ok=True)

    for game in iterate_over_replays(game_filter, events_folder):
        file_name = os.path.split(game.file)[1]
        copyfile(game.file, LONG_FILE_HEADER / spectate_folder.joinpath(file_name))
