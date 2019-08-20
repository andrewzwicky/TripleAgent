import pytest

from triple_agent.classes.missions import Missions
from triple_agent.classes.books import Books
from triple_agent.classes.timeline import TimelineCoherency, Timeline


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_correct(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"

    # check that the game is coherent to begin with.
    assert game.is_timeline_coherent() == TimelineCoherency.Coherent


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_no_timeline(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    game.timeline = None

    assert game.is_timeline_coherent() == TimelineCoherency.NoTimeline


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_no_game_start(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 31]

    assert game.is_timeline_coherent() == TimelineCoherency.NoGameStart


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_no_game_end(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove end event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 102]

    assert game.is_timeline_coherent() == TimelineCoherency.NoGameEnding


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_no_game_start_or_end(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i not in [31, 102]]

    assert (
        game.is_timeline_coherent()
        == TimelineCoherency.NoGameStart | TimelineCoherency.NoGameEnding
    )


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_guest_count_and_spy(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 0]

    assert (
        game.is_timeline_coherent()
        == TimelineCoherency.SpyNotCastInBeginning
        | TimelineCoherency.GuestCountMismatch
    )


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_guest_count(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 9]

    assert game.is_timeline_coherent() == TimelineCoherency.GuestCountMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_start_clock(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline[0].time = 200

    assert (
        game.is_timeline_coherent()
        == TimelineCoherency.StartClockMismatch | TimelineCoherency.TimeRewind
    )


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_start_clock_2(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.start_clock_seconds = 200

    assert game.is_timeline_coherent() == TimelineCoherency.StartClockMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_guest_count_amba(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 1]

    assert game.is_timeline_coherent() == TimelineCoherency.GuestCountMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_missing_book(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline[48].books = (None, Books.Green)

    assert game.is_timeline_coherent() == TimelineCoherency.BookMissingColor


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_rewind(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = Timeline(game.timeline.lines + game.timeline.lines[-10:])

    assert game.is_timeline_coherent() == TimelineCoherency.TimeRewind


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_complete_mismatch(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.completed_missions = game.completed_missions & ~Missions.Fingerprint

    assert game.is_timeline_coherent() == TimelineCoherency.CompletedMissionsMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_selected_mismatch(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.selected_missions = game.selected_missions & ~Missions.Fingerprint

    assert game.is_timeline_coherent() == TimelineCoherency.SelectedMissionsMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_picked_mismatch(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.picked_missions = game.picked_missions & ~Missions.Fingerprint

    assert game.is_timeline_coherent() == TimelineCoherency.PickedMissionsMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_complete_mismatch_2(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 78]

    assert game.is_timeline_coherent() == TimelineCoherency.CompletedMissionsMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_selected_mismatch_2(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 18]

    assert game.is_timeline_coherent() == TimelineCoherency.SelectedMissionsMismatch


@pytest.mark.parsing
@pytest.mark.quick
def test_timeline_coherent_picked_mismatch_2(get_preparsed_timeline_games):
    game = get_preparsed_timeline_games[0]
    assert game.uuid == "07WVnz3aR3i6445zgSCZjA"
    # remove start event from timeline
    game.timeline = [t for i, t in enumerate(game.timeline) if i != 27]

    assert game.is_timeline_coherent() == TimelineCoherency.PickedMissionsMismatch
