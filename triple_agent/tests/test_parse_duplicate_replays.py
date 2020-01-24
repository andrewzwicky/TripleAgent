import os
import pytest
import shutil

from triple_agent.parsing.replay.parse_replays import (
    parse_replays,
    DuplicateFileException,
)
from triple_agent.tests.test_mock_screenshot_iterator import mock_screenshot_iterator
from triple_agent.constants.paths import LONG_FILE_HEADER


@pytest.mark.parsing
def test_parse_replays_duplicates(
    get_test_replay_pickle_folder,
    get_test_events_folder,
    get_test_unparsed_folder,
    monkeypatch,
):

    source_file = os.path.join(
        LONG_FILE_HEADER,
        get_test_events_folder,
        "SCL5",
        "Copper",
        "8",
        "SpyPartyReplay-20190422-20-39-28-Max Edward Snax%2fsteam-vs-Calvin Schoolidge%2fsteam-k8x3n_zfTtiw9FSS6rM13w-v25.replay",
    )

    dest_file = os.path.join(
        LONG_FILE_HEADER,
        get_test_events_folder,
        "SCL5",
        "Copper",
        "8",
        "duplicate_file.replay",
    )

    # TODO: make a fixture to properly delete and add this file before test.
    assert not os.path.exists(dest_file)

    shutil.copy(source_file, dest_file)

    assert os.path.exists(dest_file)

    with pytest.raises(DuplicateFileException):
        parse_replays(
            lambda game: game.division == "Copper",
            unparsed_folder=get_test_unparsed_folder,
            events_folder=get_test_events_folder,
            pickle_folder=get_test_replay_pickle_folder,
            screenshot_iterator=mock_screenshot_iterator,
        )

    os.remove(dest_file)

    assert not os.path.exists(dest_file)
