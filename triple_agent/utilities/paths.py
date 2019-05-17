import os
from pathlib import Path


LONG_FILE_HEADER = "\\\\?\\"

# TODO: convert everything to Pathlib?
SPY_PARTY_REPLAYS = os.path.join(os.getenv("LOCALAPPDATA"), "SpyParty", "replays")
ALL_EVENTS_FOLDER = os.path.join(SPY_PARTY_REPLAYS, "Events")
SCL5_REPLAYS_FOLDER = os.path.join(ALL_EVENTS_FOLDER, "SCL5")
SPECTATION_REPLAYS = os.path.join(SPY_PARTY_REPLAYS, "SPECTATION_REPLAY")
UNPARSED_REPLAYS_FOLDER = os.path.join(SPY_PARTY_REPLAYS, "UNPARSED_REPLAYS")
REPLAY_PICKLE_FOLDER = Path(__file__).parents[2].joinpath("replay_pickles")
PICKLE_ISOLATION = Path(__file__).parents[2].joinpath("debug_isolation")
PARSE_LOG = Path(__file__).parents[2].joinpath("replay_parse_log.log")
PORTRAITS_FOLDER = Path(__file__).parents[1].joinpath("portraits")
