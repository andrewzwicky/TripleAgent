from typing import List, Union, Any, Dict, Optional

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
    axis_properties, data_props = populate_data_properties(
        games, data_query, axis_properties
    )

    if axis_properties.force_line:
        create_line_plot(axis_properties, data_props)
    elif axis_properties.force_bar or len(data_props.data) > 1:
        create_bar_plot(axis_properties, data_props)
    else:
        create_pie_chart(axis_properties, data_props)


def populate_data_properties(
    games: List[Game],
    data_query: DataQueryProperties,
    axis_properties: Optional[AxisProperties] = None,
):
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
    data_stack_order, data_props.data = create_data_stacks(
        data_props.category_labels, data_dictionary, data_query.data_stack_order
    )

    data_props.colors = create_data_colors(data_query.data_color_dict, data_stack_order)

    # TODO: reversed legend labels/handles
    # create data stack labels
    data_props.stack_labels = create_data_stack_labels(
        data_query.data_stack_label_dict, data_stack_order
    )

    data_props.hatching = create_data_hatching(
        data_query.data_hatch_dict, data_stack_order
    )

    return axis_properties, data_props


def create_data_colors(data_color_dict, data_stack_order):
    return (
        None
        if data_color_dict is None
        else [data_color_dict[data_part] for data_part in data_stack_order]
    )


def create_data_stack_labels(
    data_stack_label_dict: Dict[Any, str], data_stack_order: List[Any]
) -> List[str]:
    if data_stack_label_dict is not None:
        return [
            data_stack_label_dict[plot_order_item]
            for plot_order_item in data_stack_order
        ]

    return list(map(labelify, data_stack_order))


def create_data_hatching(
    data_hatch_dict: Optional[Dict[Any, Optional[str]]], data_stack_order: List[Any]
) -> Optional[List[Optional[str]]]:
    if data_hatch_dict is not None:
        return [
            data_hatch_dict[plot_order_item] for plot_order_item in data_stack_order
        ]

    return None
