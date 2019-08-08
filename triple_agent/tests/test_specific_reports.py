from collections import Counter

import pytest

from triple_agent.reports.specific.action_tests import _at_rates_excluding_difficults
from triple_agent.classes.action_tests import ActionTest


SPECIFIC_REPORT_TEST_CASES = [
    (
        _at_rates_excluding_difficults,
        Counter(
            {
                ActionTest.Green: 14,
                ActionTest.White: 34,
                ActionTest.Red: 2,
                ActionTest.Ignored: 2,
                ActionTest.Canceled: 1,
            }
        ),
    )
]


@pytest.mark.parametrize(
    "query_function, expected_data_dict", SPECIFIC_REPORT_TEST_CASES
)
def test_specific_reports(
    query_function, expected_data_dict, get_preparsed_timeline_games
):
    data_dict = Counter()

    query_function(get_preparsed_timeline_games, data_dict)

    assert data_dict == expected_data_dict
