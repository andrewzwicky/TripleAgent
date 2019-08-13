from triple_agent.reports.generation.generic_query import query
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
)
from triple_agent.classes.action_tests import (
    AT_PREFERRED_PIE_CHART_ORDER,
    AT_TO_COLORS_RGB,
)
from triple_agent.reports.specific.action_tests import _difficult_at_rate


def test_query_at(get_preparsed_timeline_games):
    axis_properties = AxisProperties()
    data_query = DataQueryProperties()

    data_query.query_function = _difficult_at_rate
    data_query.data_stack_order = AT_PREFERRED_PIE_CHART_ORDER
    data_query.data_color_dict = AT_TO_COLORS_RGB

    data_plot_properties = query(
        get_preparsed_timeline_games, data_query, axis_properties
    )
