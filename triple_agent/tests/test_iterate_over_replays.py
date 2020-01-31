import pytest

try:
    from spyparty.ReplayParser import SpyPartyParseException
except ImportError:
    from triple_agent.mock.ReplayParser import SpyPartyParseException

from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.classes.missions import Missions
from triple_agent.classes.venues import Venue
from triple_agent.classes.outcomes import WinType
from triple_agent.parsing.replay.parse_single_replay import parse_single_replay
import os


@pytest.mark.parsing
@pytest.mark.quick
def test_iterate_over_replays(get_test_events_folder, get_test_replay_pickle_folder):
    # this test is to confirm that replays can be successfully found in the folder structure
    # and assigned the correct event, week, division, etc.
    # This also tests that the games are instatiated correctly, basically testing SpyPartyParse as well.
    games = list(
        iterate_over_replays(
            lambda g: g.event != "SCL5",
            events_folder=get_test_events_folder,
            pickle_folder=get_test_replay_pickle_folder,
        )
    )
    games.sort(key=lambda g: g.start_time)

    assert len(games) == 11

    assert games[0].uuid == "yeo4Y2vhTSS1ymTHlp2t_Q"
    assert games[1].uuid == "rIm6tv8NR-G1jXeto2yzng"
    assert games[2].uuid == "-wj1l-oaQRS25PYWbN9DLw"
    assert games[3].uuid == "YXXnB3cVRVCHSXUKWWleeQ"
    assert games[4].uuid == "wG5eWfuKTMWt9FQtfxkexQ"
    assert games[5].uuid == "IoY6dxc5Qh25yPx6f4gQbw"
    assert games[6].uuid == "w04KWeaHRCK6s3C06AzQaA"
    assert games[7].uuid == "jhIlv7roRR-gOObcd1BcFQ"
    assert games[8].uuid == "oua8JMz-R5yNpHs9kUU0dA"
    assert games[9].uuid == "r_XWMspjT9aSGx9ckxuXrw"
    assert games[10].uuid == "kWo9Gri2R5CoBvbc8HJp0A"

    assert games[0].event is None
    assert games[1].event is None
    assert games[2].event is None
    assert games[3].event is None
    assert games[4].event is None
    assert games[5].event == "BatchEvent"
    assert games[6].event == "BatchEvent"
    assert games[7].event == "DetailedEvent"
    assert games[8].event == "DetailedEvent"
    assert games[9].event == "DetailedEvent"
    assert games[10].event == "OnlyGroups"

    assert games[0].division is None
    assert games[1].division is None
    assert games[2].division is None
    assert games[3].division is None
    assert games[4].division is None
    assert games[5].division is None
    assert games[6].division is None
    assert games[7].division == "BestGroup"
    assert games[8].division == "BestGroup"
    assert games[9].division == "BestGroup"
    assert games[10].division == "Group1"

    assert games[0].week is None
    assert games[1].week is None
    assert games[2].week is None
    assert games[3].week is None
    assert games[4].week is None
    assert games[5].week is None
    assert games[6].week is None
    assert games[7].week == 6
    assert games[8].week == 6
    assert games[9].week == 6
    assert games[10].week is None

    # ensure we're using the unprocessed replays
    # (haven't loaded a pickled by accident)
    assert games[0].timeline is None
    assert games[1].timeline is None
    assert games[2].timeline is None
    assert games[3].timeline is None
    assert games[4].timeline is None
    assert games[5].timeline is None
    assert games[6].timeline is None
    assert games[7].timeline is None
    assert games[8].timeline is None
    assert games[9].timeline is None
    assert games[10].timeline is None

    # the following are regression items that should catch unintentional changes in game creation.
    assert games[0].game_type == "k4"
    assert games[1].game_type == "p4/8"

    assert (
        games[1].completed_missions
        == Missions.Contact | Missions.Transfer | Missions.Swap | Missions.Seduce
    )

    assert (
        games[1].selected_missions
        == Missions.Contact
        | Missions.Transfer
        | Missions.Swap
        | Missions.Seduce
        | Missions.Bug
        | Missions.Inspect
        | Missions.Purloin
        | Missions.Fingerprint
    )

    assert (
        games[1].picked_missions
        == Missions.Contact | Missions.Transfer | Missions.Swap | Missions.Seduce
    )
    assert games[1].venue == Venue.Ballroom
    assert games[1].guest_count == 12
    assert games[1].start_clock_seconds == 315
    assert games[1].win_type == WinType.SpyShot
    assert games[1].spy == "gabrio/steam"
    assert games[1].sniper == "Calvin Schoolidge/steam"
    assert games[1].winner == "Calvin Schoolidge/steam"
    # assert games[1].start_time == datetime.datetime(
    #     day=2, hour=15, minute=17, month=6, second=32, year=2019
    # )
    assert games[1].duration == 318


@pytest.mark.parsing
@pytest.mark.quick
def test_iterate_over_replays_in_progress(
    get_test_events_folder_in_progress, get_test_replay_pickle_folder
):
    with pytest.raises(SpyPartyParseException):
        games = list(
            iterate_over_replays(
                lambda g: True,
                events_folder=get_test_events_folder_in_progress,
                pickle_folder=get_test_replay_pickle_folder,
            )
        )


@pytest.mark.parsing
def test_initial_pickle_and_repickle(
    get_unparsed_test_games, get_test_replay_pickle_folder, get_test_events_folder
):
    this_test_replay = os.path.join(
        get_test_events_folder,
        r"SCL5\Copper\8\SpyPartyReplay-20190422-20-32-21-Max Edward Snax%2fsteam-vs-Calvin Schoolidge%2fsteam-OiG7qvC9QOaSKVGlesdpWQ-v25.replay",
    )

    assert not os.path.exists(
        os.path.join(get_test_replay_pickle_folder, "OiG7qvC9QOaSKVGlesdpWQ.pkl")
    )

    # test that initial pickle will actually pickle the file.
    this_game = parse_single_replay(
        this_test_replay, get_test_replay_pickle_folder, initial_pickle=True
    )

    this_game.winner = "Calvin Schoolidge/steam"

    # test fixture will remove the files after the test
    assert os.path.exists(
        os.path.join(get_test_replay_pickle_folder, "OiG7qvC9QOaSKVGlesdpWQ.pkl")
    )

    this_game.winner = "TEST_WINNER"
    this_game.repickle(pickle_folder=get_test_replay_pickle_folder)

    newly_parsed_game = parse_single_replay(
        this_test_replay, get_test_replay_pickle_folder
    )

    assert newly_parsed_game.winner == "TEST_WINNER"
