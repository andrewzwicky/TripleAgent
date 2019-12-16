import os
from pathlib import Path


LONG_FILE_HEADER = "\\\\?\\"

# TODO: convert everything to Pathlib?
SPY_PARTY_REPLAYS = os.path.join(os.getenv("LOCALAPPDATA"), "SpyParty", "replays")
ALL_EVENTS_FOLDER = os.path.join(SPY_PARTY_REPLAYS, "Events")
SCL5_REPLAYS_FOLDER = os.path.join(ALL_EVENTS_FOLDER, "SCL5")
TEMP_EXTRACT_FOLDER = os.path.join(SCL5_REPLAYS_FOLDER, "TEMP")
ZIP_EXTRACT_FOLDER = os.path.join(SCL5_REPLAYS_FOLDER, "ZIPS")
SPECTATE_REPLAYS_FOLDER = os.path.join(SPY_PARTY_REPLAYS, "SPECTATION_REPLAY")
UNPARSED_REPLAYS_FOLDER = os.path.join(SPY_PARTY_REPLAYS, "UNPARSED_REPLAYS")
REPLAY_PICKLE_FOLDER = Path(__file__).parents[2].joinpath("replay_pickles")
DOCS_FOLDER = Path(__file__).parents[2].joinpath("docs")
CASTER_DATA_FOLDER = DOCS_FOLDER.joinpath("casters")
SPF_DATA_FOLDER = DOCS_FOLDER.joinpath("spy_party_fans")
JSON_GAMES_FOLDER = DOCS_FOLDER.joinpath("json_games")
PORTRAITS_FOLDER = Path(__file__).parents[1].joinpath("portraits")
