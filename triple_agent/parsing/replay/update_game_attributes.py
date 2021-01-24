import os
import logging

from triple_agent.constants.paths import ALL_EVENTS_FOLDER, REPLAY_PICKLE_FOLDER
from triple_agent.parsing.replay.parse_single_replay import get_replay_dict
from triple_agent.organization.replay_file_iterator import (
    separate_event_components,
    iterate_event_folder,
)
from triple_agent.classes.game import get_game_expected_pkl, game_unpickle, Game

logger = logging.getLogger("triple_agent")


if __name__ == "__main__":  # pragma: no cover
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("{levelname:<8} {message}", style="{")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    for i, (root, replay_file) in enumerate(iterate_event_folder(ALL_EVENTS_FOLDER)):
        division, event, week = separate_event_components(ALL_EVENTS_FOLDER, root)
        replay_dict = get_replay_dict(os.path.join(root, replay_file))
        expected_file = get_game_expected_pkl(replay_dict["uuid"], REPLAY_PICKLE_FOLDER)
        unpickled_game = game_unpickle(expected_file)

        new_game = Game(
            replay_dict["spy_displayname"],
            replay_dict["sniper_displayname"],
            replay_dict["spy_username"],
            replay_dict["sniper_username"],
            replay_dict["level"],
            replay_dict["result"],
            replay_dict["game_type"],
            replay_dict["picked_missions"],
            replay_dict["selected_missions"],
            replay_dict["completed_missions"],
            start_time=replay_dict["start_time"],
            guest_count=replay_dict["guest_count"],
            start_clock_seconds=replay_dict["start_clock_seconds"],
            duration=replay_dict["duration"],
            uuid=replay_dict["uuid"],
            file=replay_file,
            event=event,
            division=division,
            week=week,
            pickle_folder=REPLAY_PICKLE_FOLDER,
        )

        new_game.timeline = unpickled_game.timeline
        new_game.repickle()
        new_game.serialize_to_json()

        if (i % 500) == 0:
            print("500 pt. break")
