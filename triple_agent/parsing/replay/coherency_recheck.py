import pickle
import os
from pathlib import Path
from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER


def recheck_parsed_replays(pickle_folder: Path = REPLAY_PICKLE_FOLDER):
    # TODO: figure out what weirdness is happening here re: Path vs. string.
    for pickle_file in pickle_folder.iterdir():
        unpickled_game = pickle.load(open(pickle_file, "rb"))
        coh_bool, coh_reasons = unpickled_game.is_timeline_coherent()
        if not coh_bool:
            print(unpickled_game, coh_reasons)
            os.remove(pickle_file)


if __name__ == "__main__":
    recheck_parsed_replays()
