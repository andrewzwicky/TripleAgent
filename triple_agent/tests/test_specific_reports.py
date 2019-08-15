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
from triple_agent.reports.specific.mission_choices import _count_mission_choices

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

    data_query.query_function = _count_mission_choices

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [[8, 8, 7, 8, 7, 7, 7, 4]]
    assert data_properties.category_order == MISSION_PLOT_ORDER
    assert data_properties.stack_order == MISSION_PLOT_ORDER
    assert data_properties.colors is None
    assert data_properties.hatching is None


def test_mission_completion_query_groupby(get_preparsed_timeline_games):
    data_query = DataQueryProperties()

    data_query.query_function = _count_mission_choices
    data_query.groupby = lambda g: g.spy

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [
        [4, 4],
        [4, 4],
        [4, 3],
        [4, 4],
        [4, 3],
        [3, 4],
        [3, 4],
        [2, 2],
    ]
    assert data_properties.category_order == ["Calvin Schoolidge", "zerotka"]
    assert data_properties.stack_order == MISSION_PLOT_ORDER
    assert data_properties.colors is None
    assert data_properties.hatching is None


def test_mission_completion_query_hatching(get_preparsed_timeline_games):
    data_query = DataQueryProperties()

    data_query.query_function = _count_mission_choices
    data_query.groupby = lambda g: g.spy
    data_query.data_hatch_dict = defaultdict(lambda: None, {Missions.Fingerprint: "x"})

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [
        [4, 4],
        [4, 4],
        [4, 3],
        [4, 4],
        [4, 3],
        [3, 4],
        [3, 4],
        [2, 2],
    ]
    assert data_properties.category_order == ["Calvin Schoolidge", "zerotka"]
    assert data_properties.stack_order == MISSION_PLOT_ORDER
    assert data_properties.colors is None
    assert data_properties.hatching == [None, None, "x", None, None, None, None, None]


def test_mission_completion_query_colors(get_preparsed_timeline_games):
    data_query = DataQueryProperties()

    data_query.query_function = _count_mission_choices
    data_query.groupby = lambda g: g.spy
    data_query.data_color_dict = defaultdict(
        lambda: None, {Missions.Fingerprint: "xkcd:red", Missions.Inspect: "xkcd:blue"}
    )

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [
        [4, 4],
        [4, 4],
        [4, 3],
        [4, 4],
        [4, 3],
        [3, 4],
        [3, 4],
        [2, 2],
    ]
    assert data_properties.category_order == ["Calvin Schoolidge", "zerotka"]
    assert data_properties.stack_order == MISSION_PLOT_ORDER
    assert data_properties.colors == [
        None,
        "xkcd:blue",
        "xkcd:red",
        None,
        None,
        None,
        None,
        None,
    ]
    assert data_properties.hatching is None


def test_mission_completion_query_reversed(get_preparsed_timeline_games):
    data_query = DataQueryProperties()

    data_query.query_function = _count_mission_choices
    data_query.stack_order = MISSION_PLOT_ORDER[::-1]

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [[4, 7, 7, 7, 8, 7, 8, 8]]
    assert data_properties.category_order == MISSION_PLOT_ORDER
    assert data_properties.stack_order == MISSION_PLOT_ORDER[::-1]
    assert data_properties.colors is None
    assert data_properties.hatching is None


def test_mission_completion_query_missing_stack_items(get_preparsed_timeline_games):
    data_query = DataQueryProperties()

    data_query.query_function = _count_mission_choices
    data_query.stack_order = [Missions.Fingerprint, Missions.Inspect, Missions.Seduce]

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [[7, 8, 8]]
    assert data_properties.category_order == MISSION_PLOT_ORDER
    assert data_properties.stack_order == [
        Missions.Fingerprint,
        Missions.Inspect,
        Missions.Seduce,
    ]
    assert data_properties.colors is None
    assert data_properties.hatching is None


def test_mission_completion_query_missing_stack_items_groupby(
    get_preparsed_timeline_games
):
    data_query = DataQueryProperties()

    data_query.query_function = _count_mission_choices
    data_query.stack_order = [Missions.Fingerprint, Missions.Inspect, Missions.Seduce]
    data_query.groupby = lambda g: g.spy

    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    assert data_properties.data == [[4, 3], [4, 4], [4, 4]]
    assert data_properties.category_order == ["Calvin Schoolidge", "zerotka"]
    assert data_properties.stack_order == [
        Missions.Fingerprint,
        Missions.Inspect,
        Missions.Seduce,
    ]
    assert data_properties.colors is None
    assert data_properties.hatching is None
