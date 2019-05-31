import pickle
import os

from triple_agent.utilities.paths import REPLAY_PICKLE_FOLDER


def recheck_parsed_replays():
    for pickle_file in REPLAY_PICKLE_FOLDER.iterdir():
        unpickled_game = pickle.load(open(pickle_file, "rb"))
        coh_bool, coh_reasons = unpickled_game.is_timeline_coherent()
        if not coh_bool:
            print(unpickled_game, coh_reasons)
            os.remove(pickle_file)


if __name__ == "__main__":
    recheck_parsed_replays()
