import os
from shutil import rmtree, copyfile

from triple_agent.replays.fetch_scl5_replays import LONG_FILE_HEADER
from triple_agent.replays.parse_replays import parse_single_replay
from triple_agent.utilities.paths import SPECTATE_REPLAYS_FOLDER, ALL_EVENTS_FOLDER


def extract_spectate_replays(game_filter):
    try:
        rmtree(SPECTATE_REPLAYS_FOLDER)
    except FileNotFoundError:
        pass
    os.makedirs(SPECTATE_REPLAYS_FOLDER, exist_ok=True)

    for root, _, files in os.walk(ALL_EVENTS_FOLDER):
        for file in files:
            if file.endswith(".replay"):
                # get the path relative to the EVENTS_FOLDER
                # this will determine if there is div and week information
                path_rel_events = os.path.relpath(root, ALL_EVENTS_FOLDER)
                components = path_rel_events.split("\\")

                if len(components) == 3:
                    event, division, week = components
                    week = int(week)
                else:
                    event = components[0]
                    division = week = None

                replay_file = LONG_FILE_HEADER + os.path.join(root, file)

                this_game = parse_single_replay(
                    replay_file, event=event, division=division, week=week
                )

                if this_game is None:
                    # ignore unparseable games
                    continue

                if game_filter(this_game):
                    file_name = os.path.split(replay_file)[1]
                    copyfile(
                        replay_file,
                        LONG_FILE_HEADER
                        + os.path.join(SPECTATE_REPLAYS_FOLDER, file_name),
                    )
