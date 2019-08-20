import pandas
import pytest
from triple_agent.reports.generation.common_sort_functions import (
    sort_by_sniper_wins,
    sort_by_spy_wins,
)

from triple_agent.classes.outcomes import WinType

SORT_CASES = [
    (
        sort_by_spy_wins,
        (
            "Test",
            pandas.Series(
                data=[0, 1, 3, 4],
                index=[
                    WinType.SpyShot,
                    WinType.TimeOut,
                    WinType.CivilianShot,
                    WinType.MissionsWin,
                ],
            ),
        ),
        7,
    ),
    (
        sort_by_sniper_wins,
        (
            "Test",
            pandas.Series(
                data=[0, 1, 3, 4],
                index=[
                    WinType.SpyShot,
                    WinType.TimeOut,
                    WinType.CivilianShot,
                    WinType.MissionsWin,
                ],
            ),
        ),
        1,
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize("sort_func, series_tuple, exp_value", SORT_CASES)
def test_sort_by_wins(sort_func, series_tuple, exp_value):
    assert sort_func(series_tuple) == exp_value
