import os
from typing import Callable, Iterator


from triple_agent.parsing.replay.parse_single_replay import parse_single_replay
from triple_agent.classes.game import Game
from triple_agent.constants.paths import (
    ALL_EVENTS_FOLDER,
    LONG_FILE_HEADER,
    REPLAY_PICKLE_FOLDER,
)


def iterate_over_replays(
    game_filter: Callable,
    events_folder: str = ALL_EVENTS_FOLDER,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
) -> Iterator[Game]:
    for root, replay_file in iterate_event_folder(events_folder):
        division, event, week = separate_event_components(events_folder, root)

        this_game = parse_single_replay(
            replay_file,
            event=event,
            division=division,
            week=week,
            pickle_folder=pickle_folder,
        )

        # check that there every game was parseable
        assert this_game is not None

        # new games will not be pickled at this point.
        if game_filter(this_game):
            # we are interested in this game, yield this
            yield this_game


def separate_event_components(events_folder, root):
    # get the path relative to the EVENTS_FOLDER
    # this will determine if there is div and week information
    components = os.path.relpath(root, events_folder).split("\\")
    if len(components) == 3:
        event, division, week = components
        week = int(week)
    elif len(components) == 2:
        event, division = components
        week = None
    elif len(components) == 1 and components[0] != ".":
        # account for root level replays as different than replays in an event folder
        event = components[0]
        division = week = None
    else:
        # replays are
        event = division = week = None
    return division, event, week


def iterate_event_folder(events_folder: str = ALL_EVENTS_FOLDER):
    for root, _, files in os.walk(events_folder):
        for file in files:
            if file.endswith(".replay"):
                replay_file = LONG_FILE_HEADER + os.path.join(root, file)
                yield root, replay_file
