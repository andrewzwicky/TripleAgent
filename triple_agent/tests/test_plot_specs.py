import pytest
from triple_agent.reports.generation.plot_specs import (
    DataQueryProperties,
    AxisProperties,
    PlotLabelStyle,
    initialize_properties,
)

DATA_QUERY_CASES = [
    (DataQueryProperties(), DataQueryProperties(), DataQueryProperties()),
    (
        DataQueryProperties(primary_order=[1, 2, 3]),
        DataQueryProperties(),
        DataQueryProperties(primary_order=[1, 2, 3]),
    ),
    (
        DataQueryProperties(primary_order=[1, 2, 3]),
        5,
        DataQueryProperties(primary_order=[1, 2, 3]),
    ),
    (
        DataQueryProperties(primary_order=[1, 2, 3]),
        DataQueryProperties(limit=20),
        DataQueryProperties(primary_order=[1, 2, 3], limit=20),
    ),
    (
        DataQueryProperties(primary_order=[1, 2, 3]),
        DataQueryProperties(primary_order=[4, 5, 6]),
        DataQueryProperties(primary_order=[1, 2, 3]),
    ),
    (AxisProperties(), AxisProperties(), AxisProperties()),
    (
        AxisProperties(title="test"),
        AxisProperties(title="test not this"),
        AxisProperties(title="test"),
    ),
    (
        AxisProperties(),
        AxisProperties(primary_color_dict={"x": "x", "p": "l"}),
        AxisProperties(primary_color_dict={"x": "x", "p": "l"}),
    ),
    (
        AxisProperties(data_label_style=PlotLabelStyle.Full),
        None,
        AxisProperties(data_label_style=PlotLabelStyle.Full),
    ),
]


@pytest.mark.plotting
@pytest.mark.parametrize("initial,suggested,expected", DATA_QUERY_CASES)
def test_update_plot_specs(initial, suggested, expected):
    initial.update(suggested)

    assert initial == expected


PLOT_SPEC_INIT_CASES = [
    (None, None, None, None, AxisProperties(), DataQueryProperties()),
    (
        AxisProperties(),
        DataQueryProperties(),
        None,
        None,
        AxisProperties(),
        DataQueryProperties(),
    ),
    (
        None,
        None,
        AxisProperties(),
        DataQueryProperties(),
        AxisProperties(),
        DataQueryProperties(),
    ),
    (
        AxisProperties(title="test"),
        DataQueryProperties(primary_order=[1, 2, 3]),
        AxisProperties(title="test not this"),
        DataQueryProperties(limit=20),
        AxisProperties(title="test"),
        DataQueryProperties(primary_order=[1, 2, 3], limit=20),
    ),
]


@pytest.mark.plotting
@pytest.mark.parametrize(
    "initial_axis_props, initial_data_query_props, suggested_axis_props, suggested_data_query_props, expected_axis_props, expected_data_query_props",
    PLOT_SPEC_INIT_CASES,
)
def test_initialize_properties(
    initial_axis_props,
    initial_data_query_props,
    suggested_axis_props,
    suggested_data_query_props,
    expected_axis_props,
    expected_data_query_props,
):
    axis_props, data_query_props = initialize_properties(
        initial_axis_props,
        initial_data_query_props,
        suggested_axis_props,
        suggested_data_query_props,
    )

    assert axis_props == expected_axis_props
    assert data_query_props == expected_data_query_props
