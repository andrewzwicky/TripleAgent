import pytest
from copy import deepcopy
from triple_agent.classes.game import game_load_or_new


@pytest.mark.quick
def test_game_equal(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )
    modified_game = deepcopy(this_game)

    assert this_game == modified_game


@pytest.mark.quick
def test_game_not_equal_not_implemented(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    assert this_game.timeline != this_game


@pytest.mark.quick
def test_game_not_equal_not_implemented_str(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    assert "str" != this_game


@pytest.mark.quick
def test_game_not_equal_spy(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.spy = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_sniper(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.sniper = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_spy_username(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.spy_username = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_sniper_username(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.sniper_username = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_venue(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.venue = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_win_type(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.win_type = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_game_type(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.game_type = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_picked_missions(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.picked_missions = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_selected_missions(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.selected_missions = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_completed_missions(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.completed_missions = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_start_time(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.start_time = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_guest_count(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.guest_count = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_start_clock_seconds(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.start_clock_seconds = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_duration(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.duration = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_uuid(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.uuid = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_event(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.event = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_division(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.division = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_week(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.week = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_timeline(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.timeline = None

    assert this_game != modified_game


@pytest.mark.quick
def test_game_not_equal_winner(get_test_replay_pickle_folder):

    this_game = game_load_or_new(
        {"uuid": "mPZZrUvxQzeJYLQRbZOd7g"}, pickle_folder=get_test_replay_pickle_folder
    )

    modified_game = deepcopy(this_game)
    modified_game.winner = None

    assert this_game != modified_game

