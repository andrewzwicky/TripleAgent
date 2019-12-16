import pytest
import os
from triple_agent.classes.game import game_load_or_new

TEST_FOLDER = os.path.abspath(os.path.dirname(__file__))


@pytest.mark.parsing
def test_serialize_correctly(
    get_test_replay_pickle_folder, get_test_json_games_folder, monkeypatch,
):
    monkeypatch.setattr("builtins.input", lambda x: None)

    this_game = game_load_or_new(
        uuid="mPZZrUvxQzeJYLQRbZOd7g", pickle_folder=get_test_replay_pickle_folder
    )

    this_game.serialize_to_json(json_folder=get_test_json_games_folder)

    json_expected = open(
        os.path.join(TEST_FOLDER, "test_validation_json", "mPZZrUvxQzeJYLQRbZOd7g.json")
    ).read()
    json_actual = open(
        os.path.join(get_test_json_games_folder, "mPZZrUvxQzeJYLQRbZOd7g.json")
    ).read()

    assert json_expected == json_actual

    os.remove(os.path.join(get_test_json_games_folder, "mPZZrUvxQzeJYLQRbZOd7g.json"))
