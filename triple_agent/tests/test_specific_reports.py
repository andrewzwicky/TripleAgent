from collections import Counter, defaultdict

import pytest
from triple_agent.reports.generation.plot_utilities import create_data_dictionary
from triple_agent.reports.generation.generic_query import populate_data_properties
from triple_agent.reports.specific.action_tests import (
    _at_rates_excluding_difficults,
    _difficult_at_rate,
)
from triple_agent.classes.action_tests import ActionTest
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from triple_agent.classes.missions import MISSION_PLOT_ORDER, Missions
from triple_agent.reports.specific.mission_choices import _count_mission_choices
from triple_agent.reports.specific.game_outcomes import _categorize_outcomes
from triple_agent.reports.specific.fingerprints import _categorize_fp_sources
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.timeline import TimelineCategory

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
    (
        _categorize_outcomes,
        lambda g: g.sniper,
        False,
        defaultdict(
            Counter,
            {
                "zerotka": Counter({WinType.CivilianShot: 1, WinType.SpyShot: 3}),
                "Calvin Schoolidge": Counter({WinType.TimeOut: 1, WinType.SpyShot: 3}),
            },
        ),
    ),
]


@pytest.mark.quick
@pytest.mark.parametrize(
    "query_function,groupby,percent_normalized_data,expected_data_dict",
    CREATE_DATA_DICTIONARY_TEST_CASES,
)
def test_create_data_dictionary(
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


SPECIFIC_REPORT_CASES = [
    (
        DataQueryProperties(query_function=_count_mission_choices),
        [[8, 8, 7, 8, 7, 7, 7, 4]],
        MISSION_PLOT_ORDER,
        None,
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices, groupby=lambda g: g.spy
        ),
        [[4, 4], [4, 4], [4, 3], [4, 4], [4, 3], [3, 4], [3, 4], [2, 2]],
        ["Calvin Schoolidge", "zerotka"],
        MISSION_PLOT_ORDER,
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices, reversed_data_sort=True
        ),
        [[4, 7, 7, 7, 8, 7, 8, 8]],
        MISSION_PLOT_ORDER[::-1],
        None,
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices,
            groupby=lambda g: g.spy,
            stack_order=[Missions.Fingerprint, Missions.Inspect, Missions.Seduce],
        ),
        [[4, 3], [4, 4], [4, 4]],
        ["Calvin Schoolidge", "zerotka"],
        [Missions.Fingerprint, Missions.Inspect, Missions.Seduce],
    ),
    (
        DataQueryProperties(query_function=_categorize_fp_sources),
        [[1, 1]],
        # TODO: be more explicit about sort here, not sure why this is the way it is
        [(TimelineCategory.Books, False), (TimelineCategory.Statues, False)],
        None,
    ),
]


@pytest.mark.parametrize(
    "data_query,exp_data,exp_category_order,exp_stack_order", SPECIFIC_REPORT_CASES
)
def test_each_report(
    data_query,
    exp_data,
    exp_category_order,
    exp_stack_order,
    get_preparsed_timeline_games,
):
    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == exp_data
    assert data_properties.category_order == exp_category_order
    assert data_properties.stack_order == exp_stack_order
