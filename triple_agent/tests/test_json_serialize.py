import pytest
import os
from pathlib import Path
from triple_agent.classes.game import game_load_or_new

TEST_FOLDER = Path(__file__).resolve().parent


@pytest.mark.parsing
@pytest.mark.quick
def test_serialize_correctly(
    get_test_replay_pickle_folder, get_test_json_games_folder, monkeypatch
):
    monkeypatch.setattr("builtins.input", lambda x: None)

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    this_game.serialize_to_json(json_folder=get_test_json_games_folder)

    json_expected = open(
        TEST_FOLDER.joinpath("test_validation_json", "mPZZrUvxQzeJYLQRbZOd7g.json")
    ).read()
    json_actual = open(
        get_test_json_games_folder.joinpath("mPZZrUvxQzeJYLQRbZOd7g.json")
    ).read()

    assert json_expected == json_actual

    os.remove(get_test_json_games_folder.joinpath("mPZZrUvxQzeJYLQRbZOd7g.json"))
