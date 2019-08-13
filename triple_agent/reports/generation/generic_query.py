from collections import defaultdict
from typing import List, Union, Any, Dict

from triple_agent.reports.generation.report_utilities import (
    create_pie_chart,
    create_bar_plot,
    create_line_plot,
    labelify,
)
from triple_agent.reports.generation.plot_utilities import (
    create_sorted_categories,
    create_data_dictionary,
    limit_categories,
    create_data_stacks,
)
from triple_agent.classes.game import Game
from triple_agent.classes.scl_set import SCLSet
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
    DataQueryProperties,
)


def query(
    games: Union[List[Game], List[SCLSet]],
    data_query: DataQueryProperties,
    axis_properties: AxisProperties = None,
):
    """
    query is the default plotting interface.  Given a list of games/sets, and a function to
    classidy them, it will plot either a pie chart, bar plot, or stacked bar plot.  Can be used to
    created simple queries quickly.
    """
    if axis_properties is None:
        axis_properties = AxisProperties()

    if data_query.percent_normalized_data:
        axis_properties.y_axis_percentage = True

    data_props = DataPlotProperties()

    # create data dictionary
    data_dictionary = create_data_dictionary(
        games,
        data_query.query_function,
        data_query.groupby,
        data_query.percent_normalized_data,
    )

    # create the list of x-axis categories. percentile needs to be it's own list
    # so it can be separately sorted between the counts plot and the percentile plot
    data_props.category_labels = create_sorted_categories(
        data_dictionary,
        data_query.category_data_order,
        data_query.reversed_data_sort,
        data_query.category_name_order,
    )

    # limit categories to reduce clutter
    data_props.category_labels = limit_categories(
        data_props.category_labels, data_query.limit
    )

    # sort
    data_props.stack_labels, data_props.data = create_data_stacks(
        data_props.category_labels, data_dictionary, data_query.data_stack_order
    )

    data_props.colors = create_data_colors(
        data_query.data_color_dict, data_props.stack_labels
    )

    # TODO: reversed legend labels/handles
    # create data stack labels
    data_props.stack_labels = rename_data_stacks(
        data_query.data_stack_label_dict, data_props.stack_labels
    )

    data_props.stack_labels = list(map(labelify, data_props.stack_labels))

    if axis_properties.force_line:
        create_line_plot(axis_properties, data_props)
    elif axis_properties.force_bar or isinstance(data_dictionary, defaultdict):
        create_bar_plot(axis_properties, data_props)
    else:
        create_pie_chart(axis_properties, data_props)

    return data_props


def create_data_colors(data_color_dict, data_stack_order):
    return (
        None
        if data_color_dict is None
        else [data_color_dict[data_part] for data_part in data_stack_order]
    )


def rename_data_stacks(
    data_stack_label_dict: Dict[Any, str], stack_labels: List[Any]
) -> List[str]:
    if data_stack_label_dict is not None:
        return [
            data_stack_label_dict[plot_order_item] for plot_order_item in stack_labels
        ]

    return stack_labels
