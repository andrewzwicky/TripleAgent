import pytest

from triple_agent.parsing.replay.get_parsed_replays import get_parsed_replays
from triple_agent.classes.scl_set import sort_games_into_sets


@pytest.mark.plotting
def test_scl_set():
    games = get_parsed_replays(
        lambda g: g.event == "SCL5" and g.division == "Diamond" and g.week == 3
    )

    sets = sort_games_into_sets(games)

    sets.sort(key=lambda s: s.players[0])

    assert sets[0].players == ("canadianbacon", "magician1099")
    assert sets[1].players == ("cleetose", "warningtrack")
    assert sets[2].players == ("kcmmmmm", "krazycaley")

    assert sets[0].score == [7, 3]
    assert sets[1].score == [3, 7]
    assert sets[2].score == [6, 6]

    assert sets[0].division == "Diamond"
    assert sets[1].division == "Diamond"
    assert sets[2].division == "Diamond"

    assert sets[0].week == 3
    assert sets[1].week == 3
    assert sets[2].week == 3

    assert sets[0].tie == False
    assert sets[1].tie == False
    assert sets[2].tie == True
