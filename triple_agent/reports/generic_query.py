from collections import Counter, defaultdict
from enum import Enum
from typing import List, Callable, Optional, Any, Dict, Union

from triple_agent.reports.report_utilities import (
    create_pie_chart,
    create_bar_plot,
    create_line_plot,
)
from triple_agent.reports.plot_utilities import (
    create_sorted_categories,
    create_data_dictionary,
    limit_categories,
    create_data_stacks,
    create_data_label,
)
from triple_agent.utilities.game import Game
from triple_agent.utilities.scl_set import SCLSet

from dataclasses import dataclass


@dataclass
class OutputOptions:
    force_line: bool = False
    force_bar: bool = False
    portrait_x_axis: bool = False
    savefig: Optional[str] = None


@dataclass
class DataOptions:
    data_stack_order: List[Any] = None
    groupby: Callable = None
    category_name_order: Callable[[str], int] = None
    category_data_order: Any = None
    reversed_data_sort: bool = False
    limit: Optional[int] = None
    data_stack_label_dict: Dict[Any, str] = None
    data_color_dict: Dict[str, str] = None
    percent: bool = False

@dataclass
class VisualOptions:



@dataclass(init=False)
class PlottableData:
    categories: List[str]
    data_colors: List[str]
    data_dictionary: Union[defaultdict, Counter]
    data_stack_labels: List[str]
    stacked_data: Union[List[Union[int, float]], List[List[Union[int, float]]]]


def query(
    games: Union[List[Game], List[SCLSet]],
    title: str,
    query_function: Callable,
    data_options: DataOptions = None,
    output_options: OutputOptions = None,
 ):
    """
    query is the default plotting interface.  Given a list of games/sets, and a function to
    classify them, it will plot either a pie chart, bar plot, or stacked bar plot.  Can be used to
    created simple queries quickly.
    """
    data_options = DataOptions() if data_options is None else data_options
    output_options = OutputOptions() if output_options is None else output_options

    plottable_data = create_data_objects(data_options, games, query_function, percent=data_options.percent)

    plot_functions = []

    if output_options.force_bar:
        plot_functions.append(create_bar_plot)
        # create_bar_plot(
        #     title,
        #     stacked_data,
        #     labels=data_stack_labels_counts,
        #     bar_labels=[stacked_data],
        #     # legend_labels=data_stack_labels,
        #     colors=data_colors_counts,
        #     **kwargs,
        # )

    elif output_options.force_line:
        plot_functions.append(create_line_plot)
        # create_line_plot(
        #
        #     title,
        #     [stacked_data],
        #     labels=data_stack_labels_counts,
        #     colors=data_colors_counts,
        #     **kwargs,
        # )
    else:
        if isinstance(plottable_data.data_dictionary, Counter):
            plot_functions.append(create_pie_chart)

    for plot_function in plot_functions:
        plot_function(title, plottable_data.stacked_data, )


def create_data_objects(data_options, games, query_function, percent=False):
    output = PlottableData()

    # create data dictionary
    output.data_dictionary = create_data_dictionary(
        games, query_function, data_options.groupby, percent=percent
    )
    # create the list of x-axis categories. percentile needs to be it's own list
    # so it can be separately sorted between the counts plot and the percentile plot
    output.data_dictionary.categories = create_sorted_categories(
        output.data_dictionary,
        data_options.category_data_order,
        data_options.reversed_data_sort,
        data_options.category_name_order,
    )

    # limit categories to reduce clutter
    output.categories = limit_categories(output.data_dictionary.categories, data_options.limit)

    # sort
    data_stack_order, stacked_data = create_data_stacks(
        output.categories, output.data_dictionary, data_options.data_stack_order
    )

    # TODO: reversed legend labels/handles
    # create data stack labels
    output.data_stack_labels = create_data_plot_labels(
        data_options.data_stack_label_dict, data_stack_order
    )

    output.data_colors = create_data_colors(data_options.data_color_dict, data_stack_order)

    return output


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
        data_plot_order_labels = [
            plot_order_item.name
            if isinstance(plot_order_item, Enum)
            else str(plot_order_item)
            for plot_order_item in data_stack_order
        ]
    return data_plot_order_labels
