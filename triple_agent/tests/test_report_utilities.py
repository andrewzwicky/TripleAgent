from itertools import repeat

import pytest
from triple_agent.reports.generation.report_utilities import (
    create_plot_colors,
    create_stack_labels,
)
from triple_agent.classes.action_tests import ActionTest

COLOR_TEST_CASES = [
    (None, None, ["xkcd:green"]),
    ({"x": "blue", "y": "red"}, None, ["xkcd:green"]),
    ({"x": "blue", "y": "red"}, ["y", "x"], ["red", "blue"]),
    ({"x": "blue", "y": "red"}, ["y"], ["red"]),
    (None, ["a", "b", "c"], repeat(None)),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "data_color_dict, color_order, expected_colors", COLOR_TEST_CASES
)
def test_create_plot_colors(data_color_dict, color_order, expected_colors):
    colors = create_plot_colors(data_color_dict, color_order)

    if isinstance(expected_colors, repeat):
        assert type(colors) == type(expected_colors)
        assert next(colors) == next(expected_colors)
    else:
        assert colors == expected_colors


STACK_LABEL_CASES = [
    (None, None, None),
    ({"x": "blue", "y": "red"}, None, None),
    ({"x": "blue", "y": "red"}, ["y", "x"], ["red", "blue"]),
    ({"x": "blue", "y": "red"}, ["y"], ["red"]),
    (None, ["a", "b", "c"], ["a", "b", "c"]),
    (None, [4, 5, 6], ["4", "5", "6"]),
    (
        None,
        [ActionTest.Green, ActionTest.White, ActionTest.Canceled],
        ["Green", "White", "Canceled"],
    ),
]


@pytest.mark.plotting
@pytest.mark.quick
@pytest.mark.parametrize(
    "data_stack_label_dict, stack_order, expected_labels", STACK_LABEL_CASES
)
def test_create_stack_labels(data_stack_label_dict, stack_order, expected_labels):
    labels = create_stack_labels(data_stack_label_dict, stack_order)

    assert labels == expected_labels
