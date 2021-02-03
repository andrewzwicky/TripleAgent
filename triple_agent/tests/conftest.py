import os
from pathlib import Path

from matplotlib import pyplot as plt
from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
import pytest

pytest.register_assert_rewrite("pandas.testing")
TEST_FOLDER = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def get_test_replay_pickle_folder():
    return TEST_FOLDER.joinpath("test_example_folder_structure", "test_replay_pickles")


@pytest.fixture(scope="session")
def get_test_json_games_folder():
    return TEST_FOLDER.joinpath("test_example_folder_structure", "test_json_games")


@pytest.fixture(scope="session")
def get_test_unparsed_folder():
    return TEST_FOLDER.joinpath("test_example_folder_structure", "test_unparsed")


@pytest.fixture(scope="session")
def get_test_events_folder():
    return TEST_FOLDER.joinpath("test_example_folder_structure", "test_events")


@pytest.fixture(scope="session")
def get_test_events_folder_in_progress():
    return TEST_FOLDER.joinpath("test_example_folder_with_in_progress")


@pytest.fixture
def get_preparsed_timeline_games(get_test_events_folder, get_test_replay_pickle_folder):
    # provide the fixture value
    yield get_parsed_replays(
        lambda game: game.event == "Summer Cup 2019",
        pickle_folder=get_test_replay_pickle_folder,
    )


@pytest.fixture
def get_preparsed_fingerprint_game(
    get_test_events_folder, get_test_replay_pickle_folder
):
    # provide the fixture value
    yield get_parsed_replays(
        lambda game: game.uuid == "8VL6899HR-CcvLhYfXCPeA",
        pickle_folder=get_test_replay_pickle_folder,
    )


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
            os.remove(Path(get_test_replay_pickle_folder).joinpath(test_file))
