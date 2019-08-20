import pickle
import os
from pathlib import Path

from triple_agent.constants.paths import REPLAY_PICKLE_FOLDER
from triple_agent.classes.timeline import TimelineCoherency


def recheck_parsed_replays(pickle_folder: Path = REPLAY_PICKLE_FOLDER):
    # TODO: figure out what weirdness is happening here re: Path vs. string.
    for pickle_file in pickle_folder.iterdir():
        unpickled_game = pickle.load(open(pickle_file, "rb"))
        coherency = unpickled_game.is_timeline_coherent()
        if coherency != TimelineCoherency.Coherent:
            print(unpickled_game, str(coherency))
            os.remove(pickle_file)


if __name__ == "__main__":
    recheck_parsed_replays()
