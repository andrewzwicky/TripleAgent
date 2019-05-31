import os
from collections import defaultdict
from shutil import rmtree, copyfile
from typing import Optional, Dict, AnyStr

from spyparty.ReplayParser import ReplayParser
from triple_agent.timeline.parse_game_timelines_parallel import parse_timeline_parallel
from triple_agent.utilities.game import Game, game_load_or_new
from triple_agent.utilities.paths import (
    ALL_EVENTS_FOLDER,
    UNPARSED_REPLAYS_FOLDER,
    LONG_FILE_HEADER,
)


def get_replay_dict(replay_file: str) -> Optional[defaultdict]:
    try:
        return defaultdict(lambda: None, ReplayParser(replay_file).parse())
    # no option, the parser raises general exceptions
    # pylint: disable=broad-except
    except Exception:
        # there's not much we can do about unparseable
        # replays, so just return None
        return None


def parse_replay_dict_into_game(
    replay_dict: Optional[Dict[str, AnyStr]], replay_file: str, **kwargs
) -> Optional[Game]:
    if replay_dict is None:
        return None

    return game_load_or_new(
        replay_dict["spy_displayname"],
        replay_dict["sniper_displayname"],
        replay_dict["level"],
        replay_dict["result"].replace(" ", ""),
        replay_dict["game_type"],
        set(m.split(" ")[0] for m in replay_dict["selected_missions"]),
        set(m.split(" ")[0] for m in replay_dict["picked_missions"]),
        set(m.split(" ")[0] for m in replay_dict["completed_missions"]),
        start_time=replay_dict["start_time"],
        guest_count=replay_dict["guest_count"],
        start_clock_seconds=replay_dict["start_clock_seconds"],
        duration=replay_dict["duration"],
        uuid=replay_dict["uuid"],
        file=replay_file,
        initial_pickle=False,
        **kwargs,
    )


def parse_single_replay(replay_file: str, **kwargs) -> Optional[Game]:
    return parse_replay_dict_into_game(
        get_replay_dict(replay_file), replay_file, **kwargs
    )


def parse_replays(game_filter):
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

    game_list = []

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
                    # we are interested in this game, add it to the list
                    game_list.append(this_game)

    # check that there are no duplicates from the same file existing twice.
    assert len({game.uuid for game in game_list}) == len(game_list)

    # at this point, we will have an unsorted list of game objects
    # There may be some that do not have timelines.
    # So those should be separated now.
    unparsed_game_list = [game for game in game_list if game.timeline is None]

    if unparsed_game_list:
        print(f"{len(unparsed_game_list)} games to parse.")

        try:
            rmtree(UNPARSED_REPLAYS_FOLDER)
        except FileNotFoundError:
            pass
        os.makedirs(UNPARSED_REPLAYS_FOLDER, exist_ok=True)

        # it's important to get the replays in the correct order so that when
        # they are done in spy party, the files and the game line up correctly.
        unparsed_game_list.sort(key=lambda g: g.start_time)

        for game in unparsed_game_list:
            replay_file = game.file
            file_name = os.path.split(replay_file)[1]
            copyfile(
                replay_file,
                LONG_FILE_HEADER + os.path.join(UNPARSED_REPLAYS_FOLDER, file_name),
            )

        parse_timeline_parallel(unparsed_game_list)

        try:
            rmtree(UNPARSED_REPLAYS_FOLDER)
        except FileNotFoundError:
            pass

    return game_list


if __name__ == "__main__":
    parse_replays(lambda g: True)
