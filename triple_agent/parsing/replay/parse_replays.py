import os
from pathlib import Path
import logging

from shutil import rmtree, copyfile
from typing import Callable
import pyautogui

from triple_agent.parsing.timeline.parse_full_timeline import (
    parse_full_timeline,
)
from triple_agent.classes.timeline import Timeline
from triple_agent.constants.paths import (
    LONG_FILE_HEADER,
    ALL_EVENTS_FOLDER,
    UNPARSED_REPLAYS_FOLDER,
    REPLAY_PICKLE_FOLDER,
)
from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.timeline.screenshot_iterator import get_mss_screenshots

logger = logging.getLogger("triple_agent")


class DuplicateFileException(Exception):
    pass


def parse_replays(
    game_filter,
    unparsed_folder: Path = UNPARSED_REPLAYS_FOLDER,
    events_folder: Path = ALL_EVENTS_FOLDER,
    pickle_folder: Path = REPLAY_PICKLE_FOLDER,
    screenshot_iterator: Callable = get_mss_screenshots,
    limit=None,
    **kwargs,
):
    """
    game filter must be a function that takes a game and returns boolean, indicating whether
    that particular game should be included in the return list.  This cannot include any
    timeline events if those wish to be parsed.

    ASSUMPTIONS:
    -replays will only be parsed from the EVENTS folder recursively.
    -event folders will be organized by either:
        1. the replays are all at the top level (winter cup, summer cup)
        2. The replays are in folders (div, week) (SCL)
    -TEMP folders from downloading replays have been cleared out.

    -The entire events folder will be traversed, searching for games which meet the filter.
    --Once all games have been found which meet the criteria, the ones which need to be parsed will
        be copied to the UNPARSED_REPLAYS_FOLDER (it will be created if it is missing).  It should
        be clear from previous runs, but if not, it will be cleared.
    --Event, Division, Week info will be properly parsed into the initial game.
    ---Once parsing of unparsed games begins, it should be done in the order that os.listdir returns
        (which is date order because of the file naming convention, so it will match SP when AHK
        is parsing replays).
    ---Once parsed, timelines will be applied and the game will finally be pickled.
    """
    game_list = list(iterate_over_replays(game_filter, events_folder, pickle_folder))

    # check that there are no duplicates from the same file existing twice.
    game_uuid_set = set({game.uuid for game in game_list})
    if len(game_uuid_set) != len(game_list):
        logger.error("duplicate unparsed files found")
        for uuid in game_uuid_set:
            games_matching = [game.file for game in game_list if game.uuid == uuid]
            if len(games_matching) > 1:
                logger.error(f"{uuid} -{games_matching}")

        raise DuplicateFileException

    # should be no way to hit this with exception above, but better safe than sorry.
    assert len(game_uuid_set) == len(game_list)

    # at this point, we will have an unsorted list of game objects
    # There may be some that do not have timelines.
    # So those should be separated now.
    unparsed_game_list = [game for game in game_list if game.timeline == Timeline([])]

    # it's important to get the replays in the correct order so that when
    # they are done in spy party, the files and the game line up correctly.
    unparsed_game_list.sort(key=lambda g: g.start_time)

    if limit is not None and unparsed_game_list:
        unparsed_game_list = unparsed_game_list[:limit]

    if unparsed_game_list:
        logger.info(f"{len(unparsed_game_list)} games to parse.")

        try:
            rmtree(unparsed_folder)
        except FileNotFoundError:  # pragma: no cover
            pass
        os.makedirs(unparsed_folder, exist_ok=True)

        for game in unparsed_game_list:
            replay_file = game.file
            file_name = os.path.split(replay_file)[1]
            copyfile(
                replay_file, LONG_FILE_HEADER / unparsed_folder.joinpath(file_name)
            )

        parse_full_timeline(
            unparsed_game_list,
            screenshot_iterator=screenshot_iterator,
            pickle_folder=pickle_folder,
            **kwargs,
        )

        try:
            rmtree(unparsed_folder)
        except FileNotFoundError:  # pragma: no cover
            pass

    # games have been modified in place.
    return unparsed_game_list


if __name__ == "__main__":  # pragma: no cover
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("{levelname:<8} {message}", style="{")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    try:
        parse_replays(lambda g: True, limit=None)
    except pyautogui.FailSafeException:
        pass
