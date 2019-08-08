import os
from typing import Callable

from triple_agent.parsing.replay.parse_single_replay import parse_single_replay
from triple_agent.constants.paths import (
    ALL_EVENTS_FOLDER,
    LONG_FILE_HEADER,
    REPLAY_PICKLE_FOLDER,
)


def iterate_over_replays(
    game_filter: Callable,
    events_folder: str = ALL_EVENTS_FOLDER,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
):
    for root, _, files in os.walk(events_folder):
        for file in files:
            if file.endswith(".replay"):
                # get the path relative to the EVENTS_FOLDER
                # this will determine if there is div and week information
                components = os.path.relpath(root, events_folder).split("\\")

                if len(components) == 3:
                    event, division, week = components
                    week = int(week)
                # account for root level replays as different than replays in an event folder
                elif len(components) == 1 and components[0] != ".":
                    event = components[0]
                    division = week = None
                else:
                    # replays are
                    event = division = week = None

                replay_file = LONG_FILE_HEADER + os.path.join(root, file)

                this_game = parse_single_replay(
                    replay_file,
                    event=event,
                    division=division,
                    week=week,
                    pickle_folder=pickle_folder,
                )

                if this_game is None:
                    # ignore unparseable games
                    continue

                # new games will not be pickled at this point.

                if game_filter(this_game):
                    # we are interested in this game, yield this
                    yield this_game