import os
from shutil import rmtree, copyfile

from triple_agent.replays.replay_file_iterator import iterate_over_event_replays
from triple_agent.utilities.paths import SPECTATE_REPLAYS_FOLDER, LONG_FILE_HEADER


def extract_spectate_replays(game_filter):
    try:
        rmtree(SPECTATE_REPLAYS_FOLDER)
    except FileNotFoundError:
        pass
    os.makedirs(SPECTATE_REPLAYS_FOLDER, exist_ok=True)

    for replay_file in iterate_over_event_replays(game_filter):
        file_name = os.path.split(replay_file)[1]
        copyfile(
            replay_file,
            LONG_FILE_HEADER + os.path.join(SPECTATE_REPLAYS_FOLDER, file_name),
        )
