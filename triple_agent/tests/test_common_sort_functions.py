import pytest
from triple_agent.reports.generation.common_sort_functions import (
    sort_by_sniper_wins,
    sort_by_spy_wins,
)
from triple_agent.reports.specific.game_outcomes import _categorize_outcomes
from triple_agent.reports.generation.plot_utilities import create_data_dictionary


def test_sort_by_wins(get_preparsed_timeline_games):
    data_dictionary = create_data_dictionary(
        get_preparsed_timeline_games, _categorize_outcomes, groupby=lambda g: g.sniper
    )

    assert sort_by_spy_wins(data_dictionary["zerotka"]) == 1
    assert sort_by_spy_wins(data_dictionary["Calvin Schoolidge"]) == 0
    assert sort_by_sniper_wins(data_dictionary["zerotka"]) == 3
    assert sort_by_sniper_wins(data_dictionary["Calvin Schoolidge"]) == 4
