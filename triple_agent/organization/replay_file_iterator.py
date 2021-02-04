from pathlib import Path

from typing import Callable, Iterator, Tuple, Optional, Union


from triple_agent.parsing.replay.parse_single_replay import parse_single_replay
from triple_agent.classes.game import Game
from triple_agent.constants.paths import (
    ALL_EVENTS_FOLDER,
    LONG_FILE_HEADER,
    REPLAY_PICKLE_FOLDER,
)


def iterate_over_replays(
    game_filter: Callable,
    events_folder: Path = ALL_EVENTS_FOLDER,
    pickle_folder: Path = REPLAY_PICKLE_FOLDER,
) -> Iterator[Game]:
    for replay_file in iterate_event_folder(events_folder):
        division, event, week = separate_event_components(events_folder, replay_file)

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


def separate_event_components(
    events_folder: Path, replay_file: Path
) -> Tuple[Optional[str], Optional[str], Optional[Union[str, int]]]:
    event: Optional[str] = None
    division: Optional[str] = None
    week: Optional[Union[str, int]] = None

    # get the path relative to the EVENTS_FOLDER
    # this will determine if there is div and week information
    components = str(replay_file.relative_to(events_folder).parent).split("\\")
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

    return division, event, week


def iterate_event_folder(events_folder: Path = ALL_EVENTS_FOLDER) -> Iterator[Path]:
    for file_path in events_folder.glob("**/*.replay"):
        yield LONG_FILE_HEADER / file_path
