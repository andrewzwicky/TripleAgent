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
from triple_agent.reports.specific.fingerprints import _categorize_fp_sources, _categorize_successful_fp_sources
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.classes.roles import Roles
from triple_agent.reports.specific.character_selection import (
    determine_character_in_role,
)
from triple_agent.reports.specific.banana_breads import (
    _all_banana_breads,
    _first_banana_bread,
)
from triple_agent.reports.specific.bug import _categorize_bugs
from triple_agent.reports.generation.plot_specs import AxisProperties
import pandas

CREATE_DATA_DICTIONARY_TEST_CASES = [
    (_difficult_at_rate, None, False, defaultdict(Counter, {None: Counter()})),
    (_difficult_at_rate, None, True, defaultdict(Counter, {None: Counter()})),
    (
        _at_rates_excluding_difficults,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        ActionTest.Green: 13,
                        ActionTest.White: 19,
                        ActionTest.Red: 1,
                        ActionTest.Ignored: 1,
                    }
                )
            },
        ),
    ),
    (
        _at_rates_excluding_difficults,
        None,
        True,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        ActionTest.Green: 13 / 34,
                        ActionTest.White: 19 / 34,
                        ActionTest.Red: 1 / 34,
                        ActionTest.Ignored: 1 / 34,
                    }
                )
            },
        ),
    ),
    (
        _at_rates_excluding_difficults,
        lambda x: x.spy,
        False,
        defaultdict(
            Counter,
            {
                "Calvin Schoolidge/steam": Counter(
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
                "Calvin Schoolidge/steam": Counter(
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
                "Calvin Schoolidge/steam": Counter(
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
                "Calvin Schoolidge/steam": Counter(
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
                "Calvin Schoolidge/steam": Counter(
                    {WinType.TimeOut: 1, WinType.SpyShot: 3}
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
                "Calvin Schoolidge/steam": Counter(
                    {WinType.TimeOut: 1, WinType.SpyShot: 3}
                ),
            },
        ),
    ),
    (
        _all_banana_breads,
        None,
        False,
        defaultdict(Counter, {None: Counter({"fake": 1, "real": 6})}),
    ),
    (
        _all_banana_breads,
        lambda g: g.uuid,
        False,
        defaultdict(
            Counter,
            {
                "07WVnz3aR3i6445zgSCZjA": Counter({"real": 1}),
                "6OXfxIiITjm3I7xsGCl-fw": Counter({"fake": 1}),
                "AlwXGqeIS5-uDk4ezZgdSg": Counter({"real": 1}),
                "E3CAEUaVT82HIJmL03s_5A": Counter({"real": 1}),
                "hOGDHc8AQRupgwGrKm7lfg": Counter({"real": 1}),
                "mPZZrUvxQzeJYLQRbZOd7g": Counter({"real": 1}),
                "yF0YmgbdQLKsKMw097DlIQ": Counter({"real": 1}),
                "etwrSFKATD2hRWfz-KDXXg": Counter(),
            },
        ),
    ),
    (
        _first_banana_bread,
        None,
        False,
        defaultdict(Counter, {None: Counter({"fake": 1, "real": 6})}),
    ),
    (
        _first_banana_bread,
        lambda g: g.uuid,
        False,
        defaultdict(
            Counter,
            {
                "07WVnz3aR3i6445zgSCZjA": Counter({"real": 1}),
                "6OXfxIiITjm3I7xsGCl-fw": Counter({"fake": 1}),
                "AlwXGqeIS5-uDk4ezZgdSg": Counter({"real": 1}),
                "E3CAEUaVT82HIJmL03s_5A": Counter({"real": 1}),
                "hOGDHc8AQRupgwGrKm7lfg": Counter({"real": 1}),
                "mPZZrUvxQzeJYLQRbZOd7g": Counter({"real": 1}),
                "yF0YmgbdQLKsKMw097DlIQ": Counter({"real": 1}),
                "etwrSFKATD2hRWfz-KDXXg": Counter(),
            },
        ),
    ),
    (
        _categorize_bugs,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        ("Walking", False): 1,
                        ("Walking", True): 1,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                )
            },
        ),
    ),
    (
        _categorize_bugs,
        lambda g: g.uuid,
        False,
        defaultdict(
            Counter,
            {
                "07WVnz3aR3i6445zgSCZjA": Counter(
                    {
                        ("Walking", False): 1,
                        ("Walking", True): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "6OXfxIiITjm3I7xsGCl-fw": Counter(
                    {
                        ("Walking", True): 0,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "AlwXGqeIS5-uDk4ezZgdSg": Counter(
                    {
                        ("Walking", True): 0,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "E3CAEUaVT82HIJmL03s_5A": Counter(
                    {
                        ("Walking", True): 0,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "etwrSFKATD2hRWfz-KDXXg": Counter(
                    {
                        ("Walking", True): 0,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "hOGDHc8AQRupgwGrKm7lfg": Counter(
                    {
                        ("Walking", True): 1,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "mPZZrUvxQzeJYLQRbZOd7g": Counter(
                    {
                        ("Walking", True): 0,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
                "yF0YmgbdQLKsKMw097DlIQ": Counter(
                    {
                        ("Walking", True): 0,
                        ("Walking", False): 0,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                ),
            },
        ),
    ),
]


@pytest.mark.plotting
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
        DataQueryProperties(
            query_function=_count_mission_choices, primary_order=MISSION_PLOT_ORDER
        ),
        pandas.DataFrame(
            data=[[8, 8, 7, 8, 7, 7, 7, 4]], columns=MISSION_PLOT_ORDER, index=[None]
        ),
        True,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices,
            groupby=lambda g: g.spy,
            primary_order=MISSION_PLOT_ORDER,
        ),
        pandas.DataFrame(
            data=[[4, 4], [4, 4], [4, 3], [4, 4], [4, 3], [3, 4], [3, 4], [2, 2]],
            columns=["Calvin Schoolidge/steam", "zerotka"],
            index=MISSION_PLOT_ORDER,
        ),
        False,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices,
            groupby=lambda g: g.spy,
            primary_order=MISSION_PLOT_ORDER,
            percent_normalized_data=True,
        ),
        pandas.DataFrame(
            data=[
                [4 / 28, 4 / 28],
                [4 / 28, 4 / 28],
                [4 / 28, 3 / 28],
                [4 / 28, 4 / 28],
                [4 / 28, 3 / 28],
                [3 / 28, 4 / 28],
                [3 / 28, 4 / 28],
                [2 / 28, 2 / 28],
            ],
            columns=["Calvin Schoolidge/steam", "zerotka"],
            index=MISSION_PLOT_ORDER,
        ),
        False,
        AxisProperties(y_axis_percentage=True),
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices,
            primary_order=MISSION_PLOT_ORDER[::-1],
        ),
        pandas.DataFrame(
            data=[[4, 7, 7, 7, 8, 7, 8, 8]],
            columns=MISSION_PLOT_ORDER[::-1],
            index=[None],
        ),
        True,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices,
            groupby=lambda g: g.spy,
            primary_order=[Missions.Fingerprint, Missions.Inspect, Missions.Seduce],
        ),
        pandas.DataFrame(
            data=[[4, 3], [4, 4], [4, 4]],
            columns=["Calvin Schoolidge/steam", "zerotka"],
            index=[Missions.Fingerprint, Missions.Inspect, Missions.Seduce],
        ),
        False,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_count_mission_choices,
            groupby=lambda g: g.spy,
            reverse_secondary_order=True,
            primary_order=[Missions.Fingerprint, Missions.Inspect, Missions.Seduce],
        ),
        pandas.DataFrame(
            data=[[3, 4], [4, 4], [4, 4]],
            columns=["zerotka", "Calvin Schoolidge/steam"],
            index=[Missions.Fingerprint, Missions.Inspect, Missions.Seduce],
        ),
        False,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_categorize_fp_sources,
            primary_order=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Books, False),
            ],
        ),
        pandas.DataFrame(
            data=[[1, 1]],
            index=[None],
            columns=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Books, False),
            ],
        ),
        True,
        AxisProperties(),
    ),
]


@pytest.mark.plotting
@pytest.mark.parametrize(
    "data_query,exp_frame, exp_stacks_as_categories, exp_axis_properties",
    SPECIFIC_REPORT_CASES,
)
def test_each_report(
    data_query,
    exp_frame,
    exp_stacks_as_categories,
    get_preparsed_timeline_games,
    exp_axis_properties,
):
    axis_properties, data_properties = populate_data_properties(
        get_preparsed_timeline_games, data_query
    )

    pandas.testing.assert_frame_equal(data_properties.frame, exp_frame)
    assert data_properties.stacks_are_categories == exp_stacks_as_categories
    assert axis_properties == exp_axis_properties

FINGERPRINT_REPORT_CASES = [
    (
        DataQueryProperties(
            query_function=_categorize_fp_sources,
            primary_order=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Briefcase, True),
                (TimelineCategory.Books, True),
            ],
        ),
        pandas.DataFrame(
            data=[[2, 1, 1]],
            index=[None],
            columns=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Briefcase, True),
                (TimelineCategory.Books, True),
            ],
        ),
        True,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_categorize_fp_sources,
        ),
        pandas.DataFrame(
            data=[[1, 2, 1]],
            index=[None],
            columns=[
                # Follows order from TimelineCategory, which is not alphabetized
                (TimelineCategory.Briefcase, True),
                (TimelineCategory.Statues, False),
                (TimelineCategory.Books, True),
            ],
        ),
        True,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_categorize_successful_fp_sources,
            primary_order=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Briefcase, True),
                (TimelineCategory.Books, True),
            ],
        ),
        pandas.DataFrame(
            data=[[2, 0, 0]],
            index=[None],
            columns=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Briefcase, True),
                (TimelineCategory.Books, True),
            ],
        ),
        True,
        AxisProperties(),
    ),
    (
        DataQueryProperties(
            query_function=_categorize_successful_fp_sources,
        ),
        pandas.DataFrame(
            data=[[2]],
            index=[None],
            columns=[
                (TimelineCategory.Statues, False),
            ],
        ),
        True,
        AxisProperties(),
    ),
]

@pytest.mark.plotting
@pytest.mark.parametrize(
    "data_query,exp_frame, exp_stacks_as_categories, exp_axis_properties",
    FINGERPRINT_REPORT_CASES,
)
def test_fingerprint_report(
    data_query,
    exp_frame,
    exp_stacks_as_categories,
    get_preparsed_fingerprint_game,
    exp_axis_properties,
):
    axis_properties, data_properties = populate_data_properties(
        get_preparsed_fingerprint_game, data_query
    )

    pandas.testing.assert_frame_equal(data_properties.frame, exp_frame)
    assert data_properties.stacks_are_categories == exp_stacks_as_categories
    assert axis_properties == exp_axis_properties