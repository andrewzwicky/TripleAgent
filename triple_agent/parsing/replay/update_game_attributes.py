import os
import logging

from triple_agent.constants.paths import ALL_EVENTS_FOLDER, REPLAY_PICKLE_FOLDER
from triple_agent.parsing.replay.parse_single_replay import get_replay_dict
from triple_agent.organization.replay_file_iterator import (
    separate_event_components,
    iterate_event_folder,
)
from triple_agent.classes.game import (
    get_game_expected_pkl,
    game_unpickle,
    create_game_from_replay_info,
)

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

        new_game = create_game_from_replay_info(
            replay_dict, replay_file, event=event, division=division, week=week
        )

        new_game.timeline = unpickled_game.timeline

        if new_game != unpickled_game:
            new_game.repickle()
            new_game.serialize_to_json()

        if (i % 5000) == 0 and i > 0:
            print(f"{i}")
