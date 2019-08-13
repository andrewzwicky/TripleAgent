from collections import Counter, defaultdict
from enum import Enum
from typing import List, Union

from triple_agent.reports.generation.report_utilities import (
    create_pie_chart,
    create_bar_plot,
    create_line_plot,
)
from triple_agent.reports.generation.plot_utilities import (
    create_sorted_categories,
    create_data_dictionaries,
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

    data_props_counts = DataPlotProperties()
    data_props_percent = DataPlotProperties()

    # create data dictionary
    data_dictionary_count, data_dictionary_percent = create_data_dictionaries(
        games, data_query.query_function, data_query.groupby
    )

    # create the list of x-axis categories. percentile needs to be it's own list
    # so it can be separately sorted between the counts plot and the percentile plot
    data_props_counts.category_labels = create_sorted_categories(
        data_dictionary_count,
        data_query.category_data_order,
        data_query.reversed_data_sort,
        data_query.category_name_order,
    )
    data_props_percent.category_labels = create_sorted_categories(
        data_dictionary_percent,
        data_query.category_data_order,
        data_query.reversed_data_sort,
        data_query.category_name_order,
    )

    # limit categories to reduce clutter
    data_props_counts.category_labels = limit_categories(
        data_props_counts.category_labels, data_query.limit
    )
    data_props_percent.category_labels = limit_categories(
        data_props_percent.category_labels, data_query.limit
    )

    # sort
    data_stack_order_counts, data_props_counts.data = create_data_stacks(
        data_props_counts.category_labels,
        data_dictionary_count,
        data_query.data_stack_order,
    )
    data_stack_order_percent, data_props_percent.data = create_data_stacks(
        data_props_percent.category_labels,
        data_dictionary_percent,
        data_query.data_stack_order,
    )

    # TODO: reversed legend labels/handles
    # create data stack labels
    data_props_counts.stack_labels = create_data_plot_labels(
        data_query.data_stack_label_dict, data_stack_order_counts
    )
    data_props_percent.stack_labels = create_data_plot_labels(
        data_query.data_stack_label_dict, data_stack_order_percent
    )

    data_props_counts.colors = create_data_colors(
        data_query.data_color_dict, data_stack_order_counts
    )
    data_props_percent.colors = create_data_colors(
        data_query.data_color_dict, data_stack_order_percent
    )

    # TODO: add in y-axis labels, etc.

    if isinstance(data_dictionary_count, Counter):
        if data_query.force_bar:
            create_bar_plot(axis_properties, data_props_counts)

        elif data_query.force_line:
            create_line_plot(axis_properties, data_props_counts)
        else:
            create_pie_chart_labels(data_props_counts)

            create_pie_chart(axis_properties, data_props_counts)
    elif isinstance(data_dictionary_count, defaultdict):
        if data_query.force_line:
            create_line_plot(axis_properties, data_props_counts)
        else:
            create_bar_plot(axis_properties, data_props_counts)
    else:
        raise ValueError


def create_pie_chart_labels(data_props_counts: DataPlotProperties):
    # assume if plotting pie chart, only 1 stack is present
    total_samples = sum(data_props_counts.data[0])
    results_labels = []
    for value, label in zip(
        data_props_counts.data[0], data_props_counts.category_labels
    ):
        if not value:
            results_labels.append("")
        else:
            if total_samples:
                results_labels.append(
                    labelify(label)
                    + f"  {value}/{total_samples} {value / total_samples:.0%}"
                )
            else:
                results_labels.append(labelify(label) + f"  {value}")
    data_props_counts.category_labels = results_labels


def create_data_colors(data_color_dict, data_stack_order):
    return (
        None
        if data_color_dict is None
        else [data_color_dict[data_part] for data_part in data_stack_order]
    )


def create_data_plot_labels(data_stack_label_dict, data_stack_order):
    if data_stack_label_dict is not None:
        data_plot_order_labels = [
            data_stack_label_dict[plot_order_item]
            for plot_order_item in data_stack_order
        ]

    else:
        data_plot_order_labels = []

        for plot_order_item in data_stack_order:
            data_plot_order_labels.append(labelify(plot_order_item))

    return data_plot_order_labels


def labelify(plot_order_item):
    if isinstance(plot_order_item, Enum):
        return plot_order_item.name

    if isinstance(plot_order_item, float):
        # TODO: check this for other use cases
        return f"{plot_order_item:3>.5}"

    return str(plot_order_item)
