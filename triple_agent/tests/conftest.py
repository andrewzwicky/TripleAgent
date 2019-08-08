from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
import pytest
import os

TEST_FOLDER = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def get_test_replay_pickle_folder():
    return os.path.join(
        TEST_FOLDER, "test_example_folder_structure", "test_replay_pickles"
    )


@pytest.fixture(scope="session")
def get_test_events_folder():
    return os.path.join(TEST_FOLDER, "test_example_folder_structure", "test_events")


@pytest.fixture
def get_preparsed_timeline_games(get_test_events_folder, get_test_replay_pickle_folder):
    # provide the fixture value
    yield get_parsed_replays(
        lambda game: game.event == "Summer Cup 2019",
        pickle_folder=get_test_replay_pickle_folder,
    )
    # perform the teardown code (delete any pickled games)
    # for test_file in os.listdir(get_test_replay_pickle_folder):
    #     os.remove(os.path.join(get_test_replay_pickle_folder, test_file))


@pytest.fixture
def get_unparsed_test_games(get_test_events_folder, get_test_replay_pickle_folder):
    # provide the fixture value
    games = list(
        iterate_over_replays(
            lambda game: game.division == "Copper",
            events_folder=get_test_events_folder,
            pickle_folder=get_test_replay_pickle_folder,
        )
    )
    yield games
    uuids = [g.uuid for g in games]
    # perform the teardown code (delete any pickled for the unparsed games)
    for test_file in os.listdir(get_test_replay_pickle_folder):
        if os.path.splitext(test_file)[0] in uuids:
            os.remove(os.path.join(get_test_replay_pickle_folder, test_file))