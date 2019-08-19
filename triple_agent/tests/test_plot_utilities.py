from collections import defaultdict, Counter

import pytest

from triple_agent.reports.generation.plot_utilities import (
    create_initial_data_frame,
    sort_and_limit_frame_categories,
    sort_frame_stacks,
)
from triple_agent.classes.action_tests import ActionTest
from triple_agent.constants.events import SCL5_VENUE_MODES
import pandas


CREATE_DATA_FRAME_CASES = [
    (
        defaultdict(
            Counter,
            {
                "Balcony": Counter(
                    {ActionTest.Green: 6, ActionTest.White: 7, ActionTest.Ignored: 1}
                ),
                "Terrace": Counter(
                    {ActionTest.Green: 2, ActionTest.White: 7, ActionTest.Red: 1}
                ),
                "Gallery": Counter(
                    {
                        ActionTest.Green: 5,
                        ActionTest.White: 17,
                        ActionTest.Ignored: 1,
                        ActionTest.Canceled: 1,
                        ActionTest.Red: 1,
                    }
                ),
                "Ballroom": Counter({ActionTest.Green: 1, ActionTest.White: 3}),
            },
        ),
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        False,
    ),
    (
        defaultdict(
            Counter,
            {
                None: Counter(
                    {
                        ActionTest.Green: 5,
                        ActionTest.White: 17,
                        ActionTest.Ignored: 1,
                        ActionTest.Canceled: 1,
                        ActionTest.Red: 1,
                    }
                )
            },
        ),
        pandas.DataFrame(
            data=[[5, 17, 1, 1, 1]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
        True,
    ),
    (
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
        pandas.DataFrame(
            data=[[13 / 34, 19 / 34, 1 / 34, 1 / 34]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
            ],
            index=[None],
        ),
        True,
    ),
    (
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
        pandas.DataFrame(
            data=[[7, 6], [8, 11], [0, 1], [0, 1]],
            columns=["Calvin Schoolidge", "zerotka"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
            ],
        ),
        False,
    ),
]


@pytest.mark.quick
@pytest.mark.plotting
@pytest.mark.parametrize(
    "data_dictionary, exp_data_frame, exp_stacks_are_categories",
    CREATE_DATA_FRAME_CASES,
)
def test_create_initial_data_frame(
    data_dictionary, exp_data_frame, exp_stacks_are_categories
):
    frame, stacks_are_categories = create_initial_data_frame(data_dictionary)

    pandas.testing.assert_frame_equal(frame, exp_data_frame)
    assert stacks_are_categories == exp_stacks_are_categories


SORT_FRAME_CASES = [
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        None,
        False,
        None,
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        ActionTest.White,
        False,
        None,
        pandas.DataFrame(
            data=[
                [5, 2, 6, 1],
                [17, 7, 7, 3],
                [1, 0, 1, 0],
                [1, 1, 0, 0],
                [1, 0, 0, 0],
            ],
            columns=["Gallery", "Terrace", "Balcony", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        sum,
        False,
        None,
        pandas.DataFrame(
            data=[
                [5, 6, 2, 1],
                [17, 7, 7, 3],
                [1, 1, 0, 0],
                [1, 0, 1, 0],
                [1, 0, 0, 0],
            ],
            columns=["Gallery", "Balcony", "Terrace", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        lambda s: s,
        False,
        None,
        pandas.DataFrame(
            data=[
                [6, 1, 5, 2],
                [7, 3, 17, 7],
                [1, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Ballroom", "Gallery", "Terrace"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        lambda s: s,
        True,
        None,
        pandas.DataFrame(
            data=[
                [2, 5, 1, 6],
                [7, 17, 3, 7],
                [0, 1, 0, 1],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
            ],
            columns=["Terrace", "Gallery", "Ballroom", "Balcony"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        None,
        False,
        sorted(SCL5_VENUE_MODES.keys()),
        pandas.DataFrame(
            data=[
                [0, 6, 1, 0, 5, 0, 0, 0, 0, 0, 2, 0],
                [0, 7, 3, 0, 17, 0, 0, 0, 0, 0, 7, 0],
                [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ],
            columns=sorted(SCL5_VENUE_MODES.keys()),
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[[128, 152, 15, 15, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
        None,
        False,
        None,
        pandas.DataFrame(
            data=[[128, 152, 15, 15, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "input_frame, category_data_order, reversed_categories, category_name_order, exp_frame",
    SORT_FRAME_CASES,
)
def test_sort_frame_categories(
    input_frame,
    category_data_order,
    reversed_categories,
    category_name_order,
    exp_frame,
):
    frame = sort_and_limit_frame_categories(
        input_frame, category_data_order, category_name_order, reversed_categories
    )

    pandas.testing.assert_frame_equal(frame, exp_frame)


SORT_FRAME_STACK_CASES = [
    (
        pandas.DataFrame(
            data=[[128, 152, 15, 15, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
        None,
        True,
        pandas.DataFrame(
            data=[[128, 152, 15, 15, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
    ),
    (
        pandas.DataFrame(
            data=[[128, 152, 15, 15, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
        [ActionTest.White, ActionTest.Green],
        True,
        pandas.DataFrame(
            data=[[128, 152, 15, 15, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[None],
        ),
    ),
    (
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
        None,
        False,
        pandas.DataFrame(
            data=[
                [6, 2, 5, 1],
                [7, 7, 17, 3],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
        ),
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "input_frame, stack_order, stacks_are_categories, exp_frame", SORT_FRAME_STACK_CASES
)
def test_sort_frame_stacks(input_frame, stack_order, stacks_are_categories, exp_frame):
    frame = sort_frame_stacks(input_frame, stack_order, stacks_are_categories)

    pandas.testing.assert_frame_equal(frame, exp_frame)
