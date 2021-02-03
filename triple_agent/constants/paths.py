from pathlib import Path

LONG_FILE_HEADER = "\\\\?\\"

SPY_PARTY_REPLAYS = Path.home().joinpath("AppData", "Local", "SpyParty", "replays")
ALL_EVENTS_FOLDER = SPY_PARTY_REPLAYS.joinpath("Events")

SCL5_REPLAYS_FOLDER = ALL_EVENTS_FOLDER.joinpath("SCL5")
SCL6_REPLAYS_FOLDER = ALL_EVENTS_FOLDER.joinpath("SCL6")

SCL5_ZIP_EXTRACT_FOLDER = SCL5_REPLAYS_FOLDER.joinpath("ZIPS")
SCL6_ZIP_EXTRACT_FOLDER = SCL6_REPLAYS_FOLDER.joinpath("ZIPS")

SCL5_TEMP_EXTRACT_FOLDER = SCL5_REPLAYS_FOLDER.joinpath("TEMP")
SCL6_TEMP_EXTRACT_FOLDER = SCL6_REPLAYS_FOLDER.joinpath("TEMP")

SPECTATE_REPLAYS_FOLDER = SPY_PARTY_REPLAYS.joinpath("SPECTATION_REPLAY")
UNPARSED_REPLAYS_FOLDER = SPY_PARTY_REPLAYS.joinpath("UNPARSED_REPLAYS")
REPLAY_PICKLE_FOLDER = Path(__file__).parents[2].joinpath("replay_pickles")
DOCS_FOLDER = Path(__file__).parents[2].joinpath("docs")
PLAYER_REPORT_FOLDER = DOCS_FOLDER.joinpath("player_reports")
ALIAS_LIST_PATH = PLAYER_REPORT_FOLDER.joinpath("alias_list.json")
EVENT_REPORT_FOLDER = DOCS_FOLDER.joinpath("event_reports")
OVERALL_REPORT_FOLDER = DOCS_FOLDER.joinpath("overall_reports")
SPF_DATA_FOLDER = DOCS_FOLDER.joinpath("spy_party_fans")
JSON_GAMES_FOLDER = DOCS_FOLDER.joinpath("json_games")
PORTRAITS_FOLDER = Path(__file__).parents[1].joinpath("portraits")
EXAMPLES_FOLDER = Path(__file__).parents[2].joinpath("examples")
DEBUG_CAPTURES = Path(__file__).parents[1].joinpath("debug_captures")
