import os

from triple_agent.utilities.paths import REPLAY_PICKLE_FOLDER
from triple_agent.utilities.game import game_unpickle


def get_parsed_replays(game_filter):
    game_list = []

    for replay_pickle_file in os.listdir(REPLAY_PICKLE_FOLDER):
        unpickled_game = game_unpickle(
            os.path.join(REPLAY_PICKLE_FOLDER, replay_pickle_file)
        )
        if unpickled_game is not None:
            if game_filter(unpickled_game):
                game_list.append(unpickled_game)

    return game_list
