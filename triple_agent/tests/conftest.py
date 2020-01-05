import os

from matplotlib import pyplot as plt
from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
import pytest

pytest.register_assert_rewrite("pandas.testing")
TEST_FOLDER = os.path.abspath(os.path.dirname(__file__))

# this fixture is needed because check_figures_equal doesn't clean up after itself automatically.
# the matplotlib tests do that automatically for all tests.
# https://github.com/matplotlib/matplotlib/issues/15079
@pytest.fixture(autouse=True)
def auto_close_all_figures(request):
    yield

    if "matplotlib" in request.keywords:
        plt.close("all")


@pytest.fixture(scope="session")
def get_test_replay_pickle_folder():
    return os.path.join(
        TEST_FOLDER, "test_example_folder_structure", "test_replay_pickles"
    )


@pytest.fixture(scope="session")
def get_test_json_games_folder():
    return os.path.join(TEST_FOLDER, "test_example_folder_structure", "test_json_games")


@pytest.fixture(scope="session")
def get_test_unparsed_folder():
    return os.path.join(TEST_FOLDER, "test_example_folder_structure", "test_unparsed")


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
            os.remove(os.path.join(get_test_replay_pickle_folder, test_file))
