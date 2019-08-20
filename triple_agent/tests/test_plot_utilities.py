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
            data=[[5], [17], [1], [1], [1]],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.Canceled,
            ],
            columns=[None],
        ),
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
            data=[[13 / 34], [19 / 34], [1 / 34], [1 / 34]],
            index=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Ignored,
                ActionTest.Red,
            ],
            columns=[None],
        ),
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
    ),
]


@pytest.mark.quick
@pytest.mark.plotting
@pytest.mark.parametrize("data_dictionary, exp_data_frame", CREATE_DATA_FRAME_CASES)
def test_create_initial_data_frame(data_dictionary, exp_data_frame):
    frame = create_initial_data_frame(data_dictionary)

    # ignore the order of rows/columns, those will be sorted later
    pandas.testing.assert_frame_equal(frame, exp_data_frame, check_like=True)


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
        lambda name_series: name_series[1][ActionTest.White],
        False,
        pandas.DataFrame(
            data=[
                [1, 6, 2, 5],
                [3, 7, 7, 17],
                [0, 1, 0, 1],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
            ],
            columns=["Ballroom", "Balcony", "Terrace", "Gallery"],
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
        lambda name_series: (
            name_series[1][ActionTest.White],
            name_series[1][ActionTest.Green],
        ),
        False,
        pandas.DataFrame(
            data=[
                [1, 2, 6, 5],
                [3, 7, 7, 17],
                [0, 0, 1, 1],
                [0, 1, 0, 1],
                [0, 0, 0, 1],
            ],
            columns=["Ballroom", "Terrace", "Balcony", "Gallery"],
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
        True,
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
        lambda name_series: name_series[0],
        False,
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
        lambda name_series: name_series[0],
        True,
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
        sorted(SCL5_VENUE_MODES.keys()),
        False,
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
    "input_frame, category_order, reverse_category_order, exp_frame", SORT_FRAME_CASES
)
def test_sort_frame_categories(
    input_frame, category_order, reverse_category_order, exp_frame
):
    frame = sort_and_limit_frame_categories(
        input_frame, category_order, reverse_category_order
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
        False,
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
            data=[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.Canceled,
            ],
            index=[ActionTest.Green, ActionTest.White],
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
        lambda name_series: name_series[0].name,
        False,
        pandas.DataFrame(
            data=[
                [0, 0, 1, 0],
                [6, 2, 5, 1],
                [1, 0, 1, 0],
                [0, 1, 1, 0],
                [7, 7, 17, 3],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Canceled,
                ActionTest.Green,
                ActionTest.Ignored,
                ActionTest.Red,
                ActionTest.White,
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
        True,
        pandas.DataFrame(
            data=[
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [1, 0, 1, 0],
                [7, 7, 17, 3],
                [6, 2, 5, 1],
            ],
            columns=["Balcony", "Terrace", "Gallery", "Ballroom"],
            index=[
                ActionTest.Canceled,
                ActionTest.Red,
                ActionTest.Ignored,
                ActionTest.White,
                ActionTest.Green,
            ],
        ),
    ),
    (
        pandas.DataFrame(
            data=[[7, 6], [8, 11], [0, 1]],
            columns=["Calvin Schoolidge", "zerotka"],
            index=["Veranda", "Ballroom", "Balcony"],
        ),
        None,
        False,
        pandas.DataFrame(
            data=[[0, 1], [8, 11], [7, 6]],
            columns=["Calvin Schoolidge", "zerotka"],
            index=["Balcony", "Ballroom", "Veranda"],
        ),
    ),
    (
        pandas.DataFrame(
            data=[[7, 6, 4, 5], [8, 11, 0, 2], [0, 1, 4, 5]],
            columns=["A", "B", "D", "C"],
            index=[1, 2, 3],
        ),
        None,
        False,
        pandas.DataFrame(
            data=[[7, 6, 4, 5], [8, 11, 0, 2], [0, 1, 4, 5]],
            columns=["A", "B", "D", "C"],
            index=[1, 2, 3],
        ),
    ),
    (
        pandas.DataFrame(
            data=[[7, 6, 4, 5], [8, 11, 0, 2], [0, 1, 4, 5]],
            columns=["A", "B", "D", "C"],
            index=[1, 2, 3],
        ),
        None,
        True,
        pandas.DataFrame(
            data=[[0, 1, 4, 5], [8, 11, 0, 2], [7, 6, 4, 5]],
            columns=["A", "B", "D", "C"],
            index=[3, 2, 1],
        ),
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "input_frame, stack_order, reverse_stack_order, exp_frame", SORT_FRAME_STACK_CASES
)
def test_sort_frame_stacks(input_frame, stack_order, reverse_stack_order, exp_frame):
    frame = sort_frame_stacks(input_frame, stack_order, reverse_stack_order)

    pandas.testing.assert_frame_equal(frame, exp_frame)
