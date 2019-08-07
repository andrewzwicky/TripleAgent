import os
from typing import Callable

from triple_agent.replays.parse_single_replay import parse_single_replay
from triple_agent.constants.paths import ALL_EVENTS_FOLDER, LONG_FILE_HEADER


def iterate_over_event_replays(game_filter: Callable):
    for root, _, files in os.walk(ALL_EVENTS_FOLDER):
        for file in files:
            if file.endswith(".replay"):
                # get the path relative to the EVENTS_FOLDER
                # this will determine if there is div and week information
                components = os.path.relpath(root, ALL_EVENTS_FOLDER).split("\\")

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

                # new games will not be pickled at this point.

                if game_filter(this_game):
                    # we are interested in this game, yield this
                    yield this_game
