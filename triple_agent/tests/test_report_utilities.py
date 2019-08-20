import pytest
from triple_agent.reports.generation.report_utilities import (
    create_plot_colors,
    create_plot_hatching,
    create_data_labels,
)
from triple_agent.classes.action_tests import ActionTest
from triple_agent.reports.generation.plot_specs import PlotLabelStyle
import pandas

COLOR_TEST_CASES = [
    (
        None,
        pandas.DataFrame(
            data=[[3, 4]], columns=[ActionTest.White, ActionTest.Green], index=[None]
        ),
        True,
        False,
        [["xkcd:green", "xkcd:green"]],
    ),
    (
        None,
        pandas.DataFrame(
            data=[[3, 4]], columns=[ActionTest.White, ActionTest.Green], index=[None]
        ),
        True,
        True,
        [None],
    ),
    # this test doesn't make sense because of this disconnect between stacks_are_categories and the index == [None]a
    (
        None,
        pandas.DataFrame(
            data=[[3, 4]], columns=[ActionTest.White, ActionTest.Green], index=[None]
        ),
        False,
        False,
        [None],
    ),
    (
        {"x": "blue", "y": "red"},
        pandas.DataFrame(
            data=[[3, 4, 1], [0, 0, 0]], columns=["test", "a", "b"], index=["x", "y"]
        ),
        False,
        False,
        [["blue", "blue", "blue"], ["red", "red", "red"]],
    ),
    (
        None,
        pandas.DataFrame(
            data=[[3, 4, 1], [0, 0, 0]], columns=["test", "a", "b"], index=["x", "y"]
        ),
        False,
        False,
        [None, None],
    ),
    (
        {"x": "blue", "y": "red", "test": "green"},
        pandas.DataFrame(data=[[3, 4, 1]], columns=["test", "x", "y"], index=[None]),
        True,
        False,
        [["green", "blue", "red"]],
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "data_color_dict, frame, stacks_are_categories, is_pie_chart, expected_colors",
    COLOR_TEST_CASES,
)
def test_create_plot_colors(
    data_color_dict, frame, stacks_are_categories, is_pie_chart, expected_colors
):
    colors = create_plot_colors(
        data_color_dict, frame, stacks_are_categories, is_pie_chart
    )

    assert colors == expected_colors


HATCH_TEST_CASES = [
    (None, [ActionTest.White, ActionTest.Green], [None], True, [[None, None]]),
    # this test doesn't make sense because of this disconnect between stacks_are_categories and the index == [None]a
    (None, [ActionTest.White, ActionTest.Green], [None], False, [[None, None]]),
    (
        {"x": "//", "y": "-"},
        ["test", "a", "b"],
        ["x", "y"],
        False,
        [["//", "//", "//"], ["-", "-", "-"]],
    ),
    ({"x": "//", "y": "-"}, ["x", "y"], [None], True, [["//", "-"]]),
    (
        None,
        ["test", "a", "b"],
        ["x", "y"],
        False,
        [[None, None, None], [None, None, None]],
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "hatch_dict, columns, index, stacks_are_categories, expected_hatch",
    HATCH_TEST_CASES,
)
def test_create_plot_hatching(
    hatch_dict, columns, index, stacks_are_categories, expected_hatch
):
    hatch = create_plot_hatching(hatch_dict, columns, index, stacks_are_categories)

    assert hatch == expected_hatch


DATA_LABEL_CASES = [
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
        PlotLabelStyle.NoLabels,
        [
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
            ["", "", "", ""],
        ],
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
        PlotLabelStyle.Plain,
        [
            ["6", "2", "5", "1"],
            ["7", "7", "17", "3"],
            ["1", "0", "1", "0"],
            ["0", "1", "1", "0"],
            ["0", "0", "1", "0"],
        ],
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize("input_frame, label_style, expected_labels", DATA_LABEL_CASES)
def test_create_data_labels(input_frame, label_style, expected_labels):
    labels = create_data_labels(input_frame, label_style)

    assert labels == expected_labels
