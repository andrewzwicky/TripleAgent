from collections import Counter, defaultdict

import pytest
from triple_agent.reports.generation.plot_utilities import create_data_dictionaries
from triple_agent.reports.specific.action_tests import (
    _at_rates_excluding_difficults,
    _difficult_at_rate,
)
from triple_agent.classes.action_tests import ActionTest


CREATE_DATA_DICTIONARY_TEST_CASES = [
    (_difficult_at_rate, None, Counter(), Counter()),
    (
        _at_rates_excluding_difficults,
        None,
        Counter(
            {
                ActionTest.Green: 13,
                ActionTest.White: 19,
                ActionTest.Red: 1,
                ActionTest.Ignored: 1,
            }
        ),
        Counter(
            {
                ActionTest.Green: 13 / 34,
                ActionTest.White: 19 / 34,
                ActionTest.Red: 1 / 34,
                ActionTest.Ignored: 1 / 34,
            }
        ),
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.spy,
        defaultdict(
            Counter,
            {
                "Calvin Schoolidge": Counter(
                    {ActionTest.Green: 7, ActionTest.White: 8}
                ),
                "zerotka": Counter(
                    {
                        ActionTest.Green: 6,
                        ActionTest.White: 11,
                        ActionTest.Red: 1,
                        ActionTest.Ignored: 1,
                    }
                ),
            },
        ),
        defaultdict(
            Counter,
            {
                "Calvin Schoolidge": Counter(
                    {ActionTest.Green: 7 / 15, ActionTest.White: 8 / 15}
                ),
                "zerotka": Counter(
                    {
                        ActionTest.Green: 6 / 19,
                        ActionTest.White: 11 / 19,
                        ActionTest.Red: 1 / 19,
                        ActionTest.Ignored: 1 / 19,
                    }
                ),
            },
        ),
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.sniper,
        defaultdict(
            Counter,
            {
                "zerotka": Counter({ActionTest.Green: 7, ActionTest.White: 8}),
                "Calvin Schoolidge": Counter(
                    {
                        ActionTest.Green: 6,
                        ActionTest.White: 11,
                        ActionTest.Red: 1,
                        ActionTest.Ignored: 1,
                    }
                ),
            },
        ),
        defaultdict(
            Counter,
            {
                "zerotka": Counter(
                    {ActionTest.Green: 7 / 15, ActionTest.White: 8 / 15}
                ),
                "Calvin Schoolidge": Counter(
                    {
                        ActionTest.Green: 6 / 19,
                        ActionTest.White: 11 / 19,
                        ActionTest.Red: 1 / 19,
                        ActionTest.Ignored: 1 / 19,
                    }
                ),
            },
        ),
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.venue,
        defaultdict(
            Counter,
            {
                "High-Rise": Counter({ActionTest.Green: 1, ActionTest.White: 1}),
                "Library": Counter(
                    {ActionTest.Green: 4, ActionTest.White: 6, ActionTest.Ignored: 1}
                ),
                "Courtyard": Counter({ActionTest.Green: 6, ActionTest.White: 6}),
                "Ballroom": Counter(
                    {ActionTest.Green: 2, ActionTest.White: 6, ActionTest.Red: 1}
                ),
            },
        ),
        defaultdict(
            Counter,
            {
                "High-Rise": Counter(
                    {ActionTest.Green: 1 / 2, ActionTest.White: 1 / 2}
                ),
                "Library": Counter(
                    {
                        ActionTest.Green: 4 / 11,
                        ActionTest.White: 6 / 11,
                        ActionTest.Ignored: 1 / 11,
                    }
                ),
                "Courtyard": Counter(
                    {ActionTest.Green: 6 / 12, ActionTest.White: 6 / 12}
                ),
                "Ballroom": Counter(
                    {
                        ActionTest.Green: 2 / 9,
                        ActionTest.White: 6 / 9,
                        ActionTest.Red: 1 / 9,
                    }
                ),
            },
        ),
    ),
]


@pytest.mark.quick
@pytest.mark.parametrize(
    "query_function,groupby,expected_data_dict,expected_data_dict_percent",
    CREATE_DATA_DICTIONARY_TEST_CASES,
)
def test_included_reports(
    query_function,
    groupby,
    expected_data_dict,
    expected_data_dict_percent,
    get_preparsed_timeline_games,
):
    data_dict, data_dict_percent = create_data_dictionaries(
        get_preparsed_timeline_games, query_function, groupby
    )

    assert data_dict == expected_data_dict
    assert data_dict_percent == expected_data_dict_percent
