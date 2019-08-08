import os
from shutil import rmtree, copyfile

from triple_agent.parsing.timeline.parse_game_timelines_parallel import (
    parse_timeline_parallel
)
from triple_agent.constants.paths import (
    LONG_FILE_HEADER,
    ALL_EVENTS_FOLDER,
    UNPARSED_REPLAYS_FOLDER,
    REPLAY_PICKLE_FOLDER,
)
from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.timeline.screenshot_iterator import get_mss_screenshots


def parse_replays(
    game_filter,
    unparsed_folder: str = UNPARSED_REPLAYS_FOLDER,
    events_folder: str = ALL_EVENTS_FOLDER,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
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
    game_list = list(iterate_over_replays(game_filter, events_folder))

    # check that there are no duplicates from the same file existing twice.
    assert len({game.uuid for game in game_list}) == len(game_list)

    # at this point, we will have an unsorted list of game objects
    # There may be some that do not have timelines.
    # So those should be separated now.
    unparsed_game_list = [game for game in game_list if game.timeline is None]

    if unparsed_game_list:
        print(f"{len(unparsed_game_list)} games to parse.")

        try:
            rmtree(unparsed_folder)
        except FileNotFoundError:
            pass
        os.makedirs(unparsed_folder, exist_ok=True)

        # it's important to get the replays in the correct order so that when
        # they are done in spy party, the files and the game line up correctly.
        unparsed_game_list.sort(key=lambda g: g.start_time)

        for game in unparsed_game_list:
            replay_file = game.file
            file_name = os.path.split(replay_file)[1]
            copyfile(
                replay_file, LONG_FILE_HEADER + os.path.join(unparsed_folder, file_name)
            )

        parse_timeline_parallel(
            unparsed_game_list,
            screenshot_iterator=get_mss_screenshots,
            pickle_folder=pickle_folder,
        )

        try:
            rmtree(unparsed_folder)
        except FileNotFoundError:
            pass

    return game_list


if __name__ == "__main__":
    parse_replays(lambda g: True)
