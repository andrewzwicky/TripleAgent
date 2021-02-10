import shutil
from pathlib import Path
import numpy as np
from typing import Iterator, Tuple, List
import cv2

from triple_agent.classes.game import Game
from triple_agent.organization.replay_file_iterator import iterate_over_replays
from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
import pytest

pytest.register_assert_rewrite("pandas.testing")

@pytest.fixture(scope="session")
def base_temp_dir(tmp_path_factory):
    base = tmp_path_factory.mktemp("tests")
    for p in Path(__file__).resolve().parent.iterdir():
        if p.is_dir() and p.stem.startswith('test'):
            shutil.copytree(p, base.joinpath(p.stem))
    return base


@pytest.fixture(scope="session")
def get_test_replay_pickle_folder(base_temp_dir):
    return base_temp_dir.joinpath("test_example_folder_structure", "test_replay_pickles")


@pytest.fixture(scope="session")
def get_test_unparsed_folder(base_temp_dir):
    return base_temp_dir.joinpath("test_example_folder_structure", "test_unparsed")


@pytest.fixture(scope="session")
def get_test_events_folder(base_temp_dir):
    return base_temp_dir.joinpath("test_example_folder_structure", "test_events")


@pytest.fixture(scope="session")
def get_test_events_folder_in_progress(base_temp_dir):
    return base_temp_dir.joinpath("test_example_folder_with_in_progress")


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


@pytest.fixture(scope="session")
def mock_screenshot_iterator(base_temp_dir):
    def _mock_screenshot_iterator(
        games: List[Game],
    ) -> Iterator[Tuple[int, int, np.ndarray, bool]]:

        outputs = []

        for game_index, game in enumerate(games):
            ss_files = sorted(
                base_temp_dir.joinpath(
                    "test_parallel_replay_screenshots", game.uuid
                ).iterdir(),
                # because we can now have double digit ss_indices, must parse as index, otherwise sort order is 1 10 2, etc.
                key=lambda x: int(x.stem),
            )

            for screenshot_index, f in enumerate(ss_files, start=1):
                outputs.append(
                    (
                        game_index,
                        screenshot_index,
                        cv2.imread(
                            str(
                                base_temp_dir.joinpath(
                                    "test_parallel_replay_screenshots",
                                    game.uuid,
                                    f,
                                ).resolve()
                            )
                        ),
                        screenshot_index == len(ss_files),
                    )
                )

        for output in outputs:
            yield output

    return _mock_screenshot_iterator