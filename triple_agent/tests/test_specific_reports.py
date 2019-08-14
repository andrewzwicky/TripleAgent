from collections import Counter, defaultdict

import pytest
from triple_agent.reports.generation.plot_utilities import create_data_dictionary
from triple_agent.reports.generation.generic_query import populate_data_properties
from triple_agent.reports.specific.action_tests import (
    _at_rates_excluding_difficults,
    _difficult_at_rate,
)
from triple_agent.classes.action_tests import ActionTest
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
)
from triple_agent.classes.missions import (
    MISSIONS_ENUM_TO_COLOR,
    MISSION_PLOT_ORDER,
    Missions,
)
from triple_agent.reports.specific.mission_completes import _mission_completes

CREATE_DATA_DICTIONARY_TEST_CASES = [
    (_difficult_at_rate, None, False, Counter()),
    (_difficult_at_rate, None, True, Counter()),
    (
        _at_rates_excluding_difficults,
        None,
        False,
        Counter(
            {
                ActionTest.Green: 13,
                ActionTest.White: 19,
                ActionTest.Red: 1,
                ActionTest.Ignored: 1,
            }
        ),
    ),
    (
        _at_rates_excluding_difficults,
        None,
        True,
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
        False,
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
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.spy,
        True,
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
        False,
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
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.sniper,
        True,
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
        False,
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
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.venue,
        True,
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
    "query_function,groupby,percent_normalized_data,expected_data_dict",
    CREATE_DATA_DICTIONARY_TEST_CASES,
)
def test_included_reports(
    query_function,
    groupby,
    percent_normalized_data,
    expected_data_dict,
    get_preparsed_timeline_games,
):
    data_dict = create_data_dictionary(
        get_preparsed_timeline_games, query_function, groupby, percent_normalized_data
    )

    assert data_dict == expected_data_dict
    assert type(data_dict) == type(expected_data_dict)


def test_mission_completion_query(get_preparsed_timeline_games):
    data_query = DataQueryProperties()

    data_query.query_function = _mission_completes
    data_query.data_stack_order = MISSION_PLOT_ORDER
    data_query.data_color_dict = MISSIONS_ENUM_TO_COLOR
    data_query.groupby = lambda g: g.spy
    data_query.category_data_order = Missions.Fingerprint
    data_query.data_stack_order = [
        Missions.Fingerprint,
        Missions.Seduce,
        Missions.Bug,
        Missions.Contact,
    ]

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )
