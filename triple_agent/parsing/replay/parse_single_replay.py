from collections import defaultdict
from typing import Optional, Dict, AnyStr

from triple_agent.classes.game import Game, game_load_or_new
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.missions import convert_mission_set_to_enum
from triple_agent.classes.outcomes import WinType

from spyparty.ReplayParser import ReplayParser


def get_replay_dict(replay_file: str) -> Optional[defaultdict]:
    # noinspection PyBroadException
    try:
        return defaultdict(lambda: None, ReplayParser(replay_file).parse())
    # no option, the parser raises general exceptions
    # pylint: disable=broad-except
    except Exception:
        # there's not much we can do about unparseable
        # replays, so just return None
        return None


def parse_replay_dict_into_game(
    replay_dict: Optional[Dict[str, AnyStr]],
    replay_file: str,
    pickle_folder: str = REPLAY_PICKLE_FOLDER,
    **kwargs,
) -> Optional[Game]:
    if replay_dict is None:
        return None

    return game_load_or_new(
        replay_dict["spy_displayname"],
        replay_dict["sniper_displayname"],
        replay_dict["spy_username"],
        replay_dict["sniper_username"],
        replay_dict["level"],
        WinType[replay_dict["result"].replace(" ", "")],
        replay_dict["game_type"],
        convert_mission_set_to_enum(
            set(m.split(" ")[0] for m in replay_dict["picked_missions"])
        ),
        convert_mission_set_to_enum(
            set(m.split(" ")[0] for m in replay_dict["selected_missions"])
        ),
        convert_mission_set_to_enum(
            set(m.split(" ")[0] for m in replay_dict["completed_missions"])
        ),
        start_time=replay_dict["start_time"],
        guest_count=replay_dict["guest_count"],
        start_clock_seconds=replay_dict["start_clock_seconds"],
        duration=replay_dict["duration"],
        uuid=replay_dict["uuid"],
        file=replay_file,
        initial_pickle=kwargs.pop("initial_pickle", False),
        pickle_folder=pickle_folder,
        **kwargs,
    )


def parse_single_replay(
    replay_file: str, pickle_folder: str = REPLAY_PICKLE_FOLDER, **kwargs
) -> Optional[Game]:
    return parse_replay_dict_into_game(
        get_replay_dict(replay_file), replay_file, pickle_folder=pickle_folder, **kwargs
    )
