from pathlib import Path

import pytest
import datetime

from triple_agent.parsing.replay.parse_rply_file import (
    parse_rply_file,
    UnknownFileException,
    FileTooShortException,
    UnknownVenueException,
    UnknownFileVersion,
)

from triple_agent.classes.missions import Missions
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.venues import Venue

TEST_FOLDER = Path(__file__).resolve().parent

REPLAY_PARSE_TEST_CASES = [
    (
        "SpyPartyReplay-20151118-21-09-23-scallions-vs-fearfulferret-AOh7C-lfQR-L7p3LKBgWiQ-v16.replay",
        {
            "spy_username": "scallions",
            "spy_displayname": "scallions",
            "sniper_username": "fearfulferret",
            "sniper_displayname": "fearfulferret",
            "result": WinType.MissionsWin,
            "level": Venue.Ballroom,
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Inspect
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin,
            "game_type": "a4/8",
            "uuid": "AOh7C-lfQR-L7p3LKBgWiQ",
            "start_time": datetime.datetime(
                year=2015, month=11, day=19, hour=5, minute=9, second=23
            ),
            "duration": 115,
            "sequence_number": 7,
        },
    ),
    (
        "SpyPartyReplay-20180818-17-36-15-krazycaley-vs-canadianbacon--IrizG4mR5WT2n0Mr2bQwQ-v23.replay",
        {
            "spy_username": "krazycaley",
            "spy_displayname": "krazycaley",
            "sniper_username": "canadianbacon",
            "sniper_displayname": "canadianbacon",
            "result": WinType.SpyShot,
            "level": Venue.Moderne,
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Bug | Missions.Transfer,
            "game_type": "a5/8",
            "uuid": "-IrizG4mR5WT2n0Mr2bQwQ",
            "start_time": datetime.datetime(
                year=2018, month=8, day=19, hour=0, minute=36, second=15
            ),
            "duration": 73,
            "sequence_number": 1,
            "guest_count": 21,
            "start_clock_seconds": 240,
        },
    ),
    (
        "SpyPartyReplay-20190514-20-10-45-Calvin Schoolidge%2fsteam-vs-ninjafairy-9y7MMO4OSg2mqVi6iKBuJQ-v25.replay",
        {
            "spy_username": "s76561197991918374/steam",
            "spy_displayname": "Calvin Schoolidge/steam",
            "sniper_username": "ninjafairy",
            "sniper_displayname": "ninjafairy",
            "result": WinType.CivilianShot,
            "level": Venue.Gallery,
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Purloin,
            "game_type": "a4/8",
            "uuid": "9y7MMO4OSg2mqVi6iKBuJQ",
            "start_time": datetime.datetime(
                year=2019, month=5, day=15, hour=1, minute=10, second=45
            ),
            "duration": 234,
            "sequence_number": 2,
            "guest_count": 21,
            "start_clock_seconds": 225,
        },
    ),
    (
        "SpyPartyReplay-20190513-22-07-51-zerodoom-vs-Kmars133%2fsteam-F6YZRQ6PRxeeO66Z_N75sQ-v25.replay",
        {
            "spy_username": "zerodoom",
            "spy_displayname": "zerodoom",
            "sniper_username": "s76561198095713921/steam",
            "sniper_displayname": "Kmars133/steam",
            "result": WinType.SpyShot,
            "level": Venue.Aquarium,
            "map_variant": "Top",
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Purloin,
            "game_type": "a4/8",
            "uuid": "F6YZRQ6PRxeeO66Z_N75sQ",
            "start_time": datetime.datetime(
                year=2019, month=5, day=14, hour=2, minute=7, second=51
            ),
            "duration": 215,
            "sequence_number": 5,
            "guest_count": 19,
            "start_clock_seconds": 240,
        },
    ),
    (
        "SpyPartyReplay-20180708-18-03-52-TarekMak%2fsteam-vs-pox-VOLcw7ZYRcCs0hTK_1QgUA-v23.replay",
        {
            "spy_username": "s76561198028019690/steam",
            "spy_displayname": "TarekMak/steam",
            "sniper_username": "pox",
            "sniper_displayname": "pox",
            "result": WinType.SpyShot,
            "level": Venue.Veranda,
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin,
            "game_type": "a5/8",
            "uuid": "VOLcw7ZYRcCs0hTK_1QgUA",
            "start_time": datetime.datetime(
                year=2018, month=7, day=8, hour=8, minute=3, second=52
            ),
            "duration": 183,
            "sequence_number": 7,
            "guest_count": 21,
            "start_clock_seconds": 240,
        },
    ),
    (
        "SpyPartyReplay-20180521-23-55-55-s76561198132349669%2fsteam-vs-plastikqs-yeo4Y2vhTSS1ymTHlp2t_Q-v23.replay",
        {
            "spy_username": "s76561198132349669/steam",
            "spy_displayname": "s76561198132349669/steam",
            "sniper_username": "plastikqs",
            "sniper_displayname": "plastikqs",
            "result": WinType.SpyShot,
            "level": Venue.Pub,
            "selected_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap,
            "picked_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap,
            "completed_missions": Missions.Contact | Missions.Bug | Missions.Swap,
            "game_type": "k4",
            "uuid": "yeo4Y2vhTSS1ymTHlp2t_Q",
            "start_time": datetime.datetime(
                year=2018, month=5, day=22, hour=6, minute=55, second=55
            ),
            "duration": 175,
            "sequence_number": 1,
        },
    ),
    (
        "SpyPartyReplay-20180510-21-21-49-scallions-vs-falconhit-ZoFpgobESXW-ae3TRUZt3A-v23.replay",
        {
            "spy_username": "scallions",
            "spy_displayname": "scallions",
            "sniper_username": "falconhit",
            "sniper_displayname": "falconhit",
            "result": WinType.CivilianShot,
            "level": Venue.Library,
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Bug,
            "game_type": "a5/8",
            "uuid": "ZoFpgobESXW-ae3TRUZt3A",
            "start_time": datetime.datetime(
                year=2018, month=5, day=11, hour=1, minute=21, second=49
            ),
            "duration": 55,
            "sequence_number": 4,
        },
    ),
    (
        "SpyPartyReplay-20190421-13-42-16-Calvin Schoolidge%2fsteam-vs-biwak-lWyWAnGXSiiVgM7QvR7LzA-v25.replay",
        {
            "spy_username": "s76561197991918374/steam",
            "spy_displayname": "Calvin Schoolidge/steam",
            "sniper_username": "biwak",
            "sniper_displayname": "biwak",
            "result": WinType.MissionsWin,
            "level": Venue.Courtyard,
            "selected_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin,
            "picked_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin,
            "completed_missions": Missions.Seduce
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin,
            "game_type": "k5",
            "uuid": "lWyWAnGXSiiVgM7QvR7LzA",
            "start_time": datetime.datetime(
                year=2019, month=4, day=21, hour=18, minute=42, second=16
            ),
            "duration": 142,
            "sequence_number": 1,
            "guest_count": 11,
            "start_clock_seconds": 150,
        },
    ),
    (
        "SpyPartyReplay-20181110-12-16-46-Calvin Schoolidge%2fsteam-vs-vinishko_tyan%2fsteam-4ZeTSh2jSYmThZgTmRI7fg-v23.replay",
        {
            "spy_username": "s76561197991918374/steam",
            "spy_displayname": "Calvin Schoolidge/steam",
            "sniper_username": "s76561198450917206/steam",
            "sniper_displayname": "vinishko_tyan/steam",
            "result": WinType.MissionsWin,
            "level": Venue.Ballroom,
            "selected_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "picked_missions": Missions.Seduce
            | Missions.Inspect
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Purloin
            | Missions.Transfer,
            "completed_missions": Missions.Contact
            | Missions.Bug
            | Missions.Swap
            | Missions.Transfer,
            "game_type": "a4/8",
            "uuid": "4ZeTSh2jSYmThZgTmRI7fg",
            "start_time": datetime.datetime(
                year=2018, month=11, day=10, hour=18, minute=16, second=46
            ),
            "duration": 189,
            "sequence_number": 7,
            "guest_count": 15,
            "start_clock_seconds": 210,
        },
    ),
    (
        "SpyPartyReplay-20151121-11-22-38-lthummus-vs-iceman-weC59W1LRG2zvP_LZTstKA-v16.replay",
        {
            "spy_username": "lthummus",
            "spy_displayname": "lthummus",
            "sniper_username": "iceman",
            "sniper_displayname": "iceman",
            "result": WinType.CivilianShot,
            "level": Venue.DoubleModern,
            "selected_missions": Missions.Seduce
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Purloin,
            "picked_missions": Missions.Seduce
            | Missions.Fingerprint
            | Missions.Contact
            | Missions.Bug
            | Missions.Purloin,
            "completed_missions": Missions.Contact | Missions.Bug | Missions.Purloin,
            "game_type": "a3/5",
            "uuid": "weC59W1LRG2zvP_LZTstKA",
            "start_time": datetime.datetime(
                year=2015, month=11, day=21, hour=19, minute=22, second=38
            ),
            "duration": 130,
            "sequence_number": 5,
            # "guest_count": 10,
            # "start_clock_seconds": 150,
        },
    ),
]


@pytest.mark.parametrize("replay_file, expected_parse_dict", REPLAY_PARSE_TEST_CASES)
def test_parse_rply_files(replay_file, expected_parse_dict):
    replay_file_abs = TEST_FOLDER.joinpath("test_rply_files", replay_file)

    actual_parse_dict = parse_rply_file(replay_file_abs)

    assert actual_parse_dict == expected_parse_dict


def test_parse_bad_rply_files():
    replay_file_abs = TEST_FOLDER.joinpath(
        "test_rply_files", "__qYh7wKStG2bXq5wwu8lg.pkl"
    )

    with pytest.raises(UnknownFileException):
        parse_rply_file(replay_file_abs)


def test_parse_small_rply_files():
    replay_file_abs = TEST_FOLDER.joinpath("test_rply_files", "test.txt")

    with pytest.raises(FileTooShortException):
        parse_rply_file(replay_file_abs)


def test_parse_unknown_venue_rply_files():
    replay_file_abs = TEST_FOLDER.joinpath("test_rply_files", "unknown_venue.replay")

    with pytest.raises(UnknownVenueException):
        parse_rply_file(replay_file_abs)


def test_parse_invalid_version_rply_files():
    replay_file_abs = TEST_FOLDER.joinpath("test_rply_files", "invalid_version.replay")

    with pytest.raises(UnknownFileVersion):
        parse_rply_file(replay_file_abs)
