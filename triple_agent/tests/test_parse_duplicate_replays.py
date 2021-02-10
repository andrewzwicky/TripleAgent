import pytest
import shutil

from triple_agent.parsing.replay.parse_replays import (
    parse_replays,
    DuplicateFileException,
)
from triple_agent.constants.paths import LONG_FILE_HEADER


@pytest.mark.parsing
def test_parse_replays_duplicates(
    tmp_path,
    get_test_replay_pickle_folder,
    get_test_events_folder,
    get_test_unparsed_folder,
    mock_screenshot_iterator,
    monkeypatch,
):
    temp_events = tmp_path.joinpath("test_events")

    shutil.copytree(get_test_events_folder, temp_events)

    source_file = LONG_FILE_HEADER / temp_events.joinpath(
        "SCL5",
        "Copper",
        "8",
        "SpyPartyReplay-20190422-20-39-28-Max Edward Snax%2fsteam-vs-Calvin Schoolidge%2fsteam-k8x3n_zfTtiw9FSS6rM13w-v25.replay",
    )

    dest_file = LONG_FILE_HEADER / temp_events.joinpath(
        "SCL5",
        "Copper",
        "8",
        "duplicate_file.replay",
    )
    shutil.copy(source_file, dest_file)

    assert dest_file.exists()

    with pytest.raises(DuplicateFileException):
        parse_replays(
            lambda game: game.division == "Copper",
            get_test_unparsed_folder,
            temp_events,
            get_test_replay_pickle_folder,
            tmp_path,
            mock_screenshot_iterator,
        )
