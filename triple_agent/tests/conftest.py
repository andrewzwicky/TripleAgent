from pathlib import Path

from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
import pytest

pytest.register_assert_rewrite("pandas.testing")
TEST_FOLDER = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def get_test_replay_pickle_folder():
    return TEST_FOLDER.joinpath("test_example_folder_structure", "test_replay_pickles")


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
        get_test_replay_pickle_folder,
        lambda game: game.event == "Summer Cup 2019",
    )


@pytest.fixture
def get_preparsed_fingerprint_game(
    get_test_events_folder, get_test_replay_pickle_folder
):
    # provide the fixture value
    yield get_parsed_replays(
        get_test_replay_pickle_folder,
        lambda game: game.uuid == "8VL6899HR-CcvLhYfXCPeA",
    )


@pytest.fixture
def get_unparsed_test_games(get_test_events_folder, get_test_replay_pickle_folder):
    # provide the fixture value
    games = list(
        iterate_over_replays(
            lambda game: game.division == "Copper",
            get_test_events_folder,
            get_test_replay_pickle_folder,
        )
    )
    yield games
