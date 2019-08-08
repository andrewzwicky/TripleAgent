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
    spectate_folder: str = SPECTATE_REPLAYS_FOLDER,
    events_folder: str = ALL_EVENTS_FOLDER,
):
    try:
        rmtree(spectate_folder)
    except FileNotFoundError:
        pass
    os.makedirs(spectate_folder, exist_ok=True)

    for replay_file in iterate_over_replays(game_filter, events_folder):
        file_name = os.path.split(replay_file)[1]
        copyfile(
            replay_file, LONG_FILE_HEADER + os.path.join(spectate_folder, file_name)
        )
