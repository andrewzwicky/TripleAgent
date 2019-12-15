import pytest
import os
from triple_agent.parsing.replay.parse_replays import parse_replays

from triple_agent.tests.test_mock_screenshot_iterator import mock_screenshot_iterator

TEST_FOLDER = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parsing
def test_serialize_correctly(
    get_test_replay_pickle_folder,
    get_test_events_folder,
    get_test_unparsed_folder,
    get_test_json_games_folder,
    monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda x: None)

    this_game = parse_replays(
        lambda game: game.uuid == "OiG7qvC9QOaSKVGlesdpWQ",
        unparsed_folder=get_test_unparsed_folder,
        events_folder=get_test_events_folder,
        pickle_folder=get_test_replay_pickle_folder,
        screenshot_iterator=mock_screenshot_iterator,
    )[0]

    json_out = this_game.serialize_to_json(json_folder=get_test_json_games_folder)
    assert False