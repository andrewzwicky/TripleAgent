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
from triple_agent.reports.specific.fingerprints import (
    _categorize_fp_sources,
    _categorize_successful_fp_sources,
)
from triple_agent.classes.outcomes import WinType
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.classes.characters import Characters
from triple_agent.reports.specific.character_selection import (
    _determine_st, _determine_amba, _determine_spy, _determine_da
)
from triple_agent.reports.specific.banana_breads import (
    _all_banana_breads,
    _first_banana_bread,
)
from triple_agent.reports.specific.bug import _categorize_bugs
from triple_agent.reports.generation.plot_specs import AxisProperties
from triple_agent.classes.venues import Venue
import pandas

CREATE_DATA_DICTIONARY_TEST_CASES = [
    (
        _difficult_at_rate,
        None,
        False,
        defaultdict(Counter, {None: Counter({ActionTest.Green: 1})}),
    ),
    (
        _difficult_at_rate,
        None,
        True,
        defaultdict(Counter, {None: Counter({ActionTest.Green: 1})}),
    ),
    (
        _at_rates_excluding_difficults,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        ActionTest.Green: 16,
                        ActionTest.White: 20,
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
                        ActionTest.Green: 16 / 38,
                        ActionTest.White: 20 / 38,
                        ActionTest.Red: 1 / 38,
                        ActionTest.Ignored: 1 / 38,
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
                "pwndnoob": Counter({ActionTest.Green: 3, ActionTest.White: 1}),
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
                "pwndnoob": Counter({ActionTest.Green: 3 / 4, ActionTest.White: 1 / 4}),
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
                "jd105l": Counter({ActionTest.Green: 3, ActionTest.White: 1}),
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
                "jd105l": Counter({ActionTest.Green: 3 / 4, ActionTest.White: 1 / 4}),
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
                Venue.HighRise: Counter({ActionTest.Green: 1, ActionTest.White: 1}),
                Venue.Library: Counter(
                    {ActionTest.Green: 7, ActionTest.White: 7, ActionTest.Ignored: 1}
                ),
                Venue.Courtyard: Counter({ActionTest.Green: 6, ActionTest.White: 6}),
                Venue.Ballroom: Counter(
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
                Venue.HighRise: Counter(
                    {ActionTest.Green: 1 / 2, ActionTest.White: 1 / 2}
                ),
                Venue.Library: Counter(
                    {
                        ActionTest.Green: 7 / 15,
                        ActionTest.White: 7 / 15,
                        ActionTest.Ignored: 1 / 15,
                    }
                ),
                Venue.Courtyard: Counter(
                    {ActionTest.Green: 6 / 12, ActionTest.White: 6 / 12}
                ),
                Venue.Ballroom: Counter(
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
                "jd105l": Counter({WinType.CivilianShot: 1}),
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
        defaultdict(Counter, {None: Counter({"fake": 1, "real": 7})}),
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
                "Gp5L4amETsGIPVwh5fdjkA": Counter({"real": 1}),
            },
        ),
    ),
    (
        _first_banana_bread,
        None,
        False,
        defaultdict(Counter, {None: Counter({"fake": 1, "real": 7})}),
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
                "Gp5L4amETsGIPVwh5fdjkA": Counter({"real": 1}),
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
                        ("Walking", True): 2,
                        ("Standing", True): 0,
                        ("Standing", False): 0,
                    }
                )
            },
        ),
    ),
    (
        _determine_spy,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        Characters.Morgan: 2,
                        Characters.Duke: 1,
                        Characters.Sikh: 1,
                        Characters.Plain: 1,
                        Characters.Helen: 1,
                        Characters.Rocker: 1,
                        Characters.Carlos: 1,
                        Characters.Salmon: 1,
                    }
                )
            },
        ),
    ),
    (
        _determine_amba,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        Characters.Irish: 1,
                        Characters.Taft: 1,
                        Characters.Plain: 1,
                        Characters.Helen: 1,
                        Characters.Oprah: 1,
                        Characters.Salmon: 4,
                    }
                )
            },
        ),
    ),
    (
        _determine_da,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        Characters.Disney: 3,
                        Characters.Carlos: 1,
                        Characters.Sikh: 1,
                        Characters.Oprah: 1,
                        Characters.Duke: 2,
                        Characters.Sari: 1,
                    }
                )
            },
        ),
    ),
    (
        _determine_st,
        None,
        False,
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        Characters.Irish: 1,
                        Characters.Teal: 1,
                        Characters.Alice: 1,
                        Characters.Carlos: 3,
                        Characters.Taft: 1,
                        Characters.Bling: 1,
                        Characters.Queen: 1,
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
                "Gp5L4amETsGIPVwh5fdjkA": Counter(
                    {
                        ("Walking", True): 1,
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
            data=[[9, 9, 8, 9, 8, 8, 8, 5]], columns=MISSION_PLOT_ORDER, index=[None]
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
            data=[
                [4, 1, 4],
                [4, 1, 4],
                [4, 1, 3],
                [4, 1, 4],
                [4, 1, 3],
                [3, 1, 4],
                [3, 1, 4],
                [2, 1, 2],
            ],
            columns=["Calvin Schoolidge/steam", "pwndnoob", "zerotka"],
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
                [4 / 28, 1 / 8, 4 / 28],
                [4 / 28, 1 / 8, 4 / 28],
                [4 / 28, 1 / 8, 3 / 28],
                [4 / 28, 1 / 8, 4 / 28],
                [4 / 28, 1 / 8, 3 / 28],
                [3 / 28, 1 / 8, 4 / 28],
                [3 / 28, 1 / 8, 4 / 28],
                [2 / 28, 1 / 8, 2 / 28],
            ],
            columns=["Calvin Schoolidge/steam", "pwndnoob", "zerotka"],
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
            data=[[5, 8, 8, 8, 9, 8, 9, 9]],
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
            data=[[4, 1, 3], [4, 1, 4], [4, 1, 4]],
            columns=["Calvin Schoolidge/steam", "pwndnoob", "zerotka"],
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
            data=[[3, 1, 4], [4, 1, 4], [4, 1, 4]],
            columns=["zerotka", "pwndnoob", "Calvin Schoolidge/steam"],
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
                (TimelineCategory.Books, True),
            ],
        ),
        pandas.DataFrame(
            data=[[1, 2, 1]],
            index=[None],
            columns=[
                (TimelineCategory.Statues, False),
                (TimelineCategory.Books, False),
                (TimelineCategory.Books, True),
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
        DataQueryProperties(query_function=_categorize_fp_sources,),
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
        DataQueryProperties(query_function=_categorize_successful_fp_sources,),
        pandas.DataFrame(
            data=[[2]], index=[None], columns=[(TimelineCategory.Statues, False),],
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
