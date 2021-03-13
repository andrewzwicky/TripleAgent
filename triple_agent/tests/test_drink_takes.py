import pytest
from collections import Counter
from triple_agent.reports.specific.drink_rejects import _drink_takes


@pytest.mark.plotting
def test_drink_takes(get_preparsed_timeline_games):
    actual = Counter()
    _drink_takes(get_preparsed_timeline_games, actual)
    assert actual == Counter({"reject": 9, "take": 3, "purloin": 2})
