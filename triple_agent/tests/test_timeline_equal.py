import pytest
from copy import deepcopy
from triple_agent.classes.game import game_load_or_new


@pytest.mark.quick
def test_timeline_equal(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        uuid="mPZZrUvxQzeJYLQRbZOd7g", pickle_folder=get_test_replay_pickle_folder
    )
    modified_game = deepcopy(this_game)

    assert this_game.timeline == modified_game.timeline


@pytest.mark.quick
def test_timeline_equal_not_implemented(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        uuid="mPZZrUvxQzeJYLQRbZOd7g", pickle_folder=get_test_replay_pickle_folder
    )
    modified_game = deepcopy(this_game)

    assert this_game.timeline != modified_game.timeline[0]


@pytest.mark.quick
def test_timeline_equal_not_implemented_no_lines(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        uuid="mPZZrUvxQzeJYLQRbZOd7g", pickle_folder=get_test_replay_pickle_folder
    )
    modified_game = deepcopy(this_game)
    del modified_game.timeline.lines

    assert this_game.timeline != modified_game.timeline
