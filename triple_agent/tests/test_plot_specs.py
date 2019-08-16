import pytest
from triple_agent.reports.generation.plot_specs import (
    DataQueryProperties,
    AxisProperties,
    PlotLabelStyle,
)

DATA_QUERY_CASES = [
    (DataQueryProperties(), DataQueryProperties(), DataQueryProperties()),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        DataQueryProperties(),
        DataQueryProperties(stack_order=[1, 2, 3]),
    ),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        5,
        DataQueryProperties(stack_order=[1, 2, 3]),
    ),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        DataQueryProperties(limit=20),
        DataQueryProperties(stack_order=[1, 2, 3], limit=20),
    ),
    (
        DataQueryProperties(stack_order=[1, 2, 3]),
        DataQueryProperties(stack_order=[4, 5, 6]),
        DataQueryProperties(stack_order=[1, 2, 3]),
    ),
    (AxisProperties(), AxisProperties(), AxisProperties()),
    (
        AxisProperties(title="test"),
        AxisProperties(title="test not this"),
        AxisProperties(title="test"),
    ),
    (
        AxisProperties(),
        AxisProperties(data_color_dict={"x": "x", "p": "l"}),
        AxisProperties(data_color_dict={"x": "x", "p": "l"}),
    ),
    (
        AxisProperties(data_label_style=PlotLabelStyle.Full),
        None,
        AxisProperties(data_label_style=PlotLabelStyle.Full),
    ),
]


@pytest.mark.parametrize("initial,suggested,expected", DATA_QUERY_CASES)
def test_update_plot_specs(initial, suggested, expected):
    initial.update(suggested)

    assert initial == expected
