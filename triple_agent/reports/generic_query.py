from collections import Counter, defaultdict
from enum import Enum
from typing import List, Callable, Optional, Any, Dict, Union

from triple_agent.reports.report_utilities import create_pie_chart, create_bar_plot
from triple_agent.reports.plot_utilities import (
    create_sorted_categories,
    create_data_dictionary,
    limit_categories,
)
from triple_agent.utilities.game import Game
from triple_agent.utilities.scl_set import SCLSet


def query(
    games: Union[List[Game], List[SCLSet]],
    title: str,
    query_function: Callable,
    data_stack_order: List[Any] = None,
    data_color_dict: Dict[str, str] = None,
    data_hatching: List[Optional[str]] = None,
    groupby: Callable = None,
    category_name_order: Callable[[str], int] = None,
    category_data_order: Any = None,
    reversed_data_sort: bool = False,
    limit: Optional[int] = None,
    counts_plot: bool = True,
    percentile_plot: bool = True,
    data_stack_label_dict: Dict[Any, str] = None,
    force_bar=False,
    portrait_x_axis=False,
):
    """
    query is the default plotting interface.  Given a list of games/sets, and a function to
    classidy them, it will plot either a pie chart, bar plot, or stacked bar plot.  Can be used to
    created simple queries quickly.
    """

    # create data dictionary
    data_dictionary, data_sum = create_data_dictionary(games, query_function, groupby)

    # create the list of x-axis categories. percentile needs to be it's own list
    # so it can be separately sorted between the counts plot and the percentile plot
    categories, percentile_categories = create_sorted_categories(
        data_dictionary,
        data_sum,
        category_data_order,
        reversed_data_sort,
        category_name_order,
    )

    # limit categories to reduce clutter
    categories, percentile_categories = limit_categories(
        categories, percentile_categories, limit
    )

    # sort
    data_stack_order, percentile_data, stacked_data = create_data_stacks(
        categories, percentile_categories, data_dictionary, data_sum, data_stack_order
    )

    # TODO: reversed legend labels/handles
    # create data stack labels
    data_stack_labels = create_data_plot_labels(data_stack_label_dict, data_stack_order)

    data_colors, percentile_data_colors = create_data_colors(
        data_color_dict, data_stack_order
    )

    if isinstance(data_dictionary, Counter):
        if force_bar:
            create_bar_plot(
                title,
                [stacked_data],
                labels=data_stack_labels,
                bar_labels=[stacked_data],
                legend_labels=data_stack_labels,
                colors=data_colors,
                hatches=data_hatching,
                label_rotation=90,
                portrait_x_axis=portrait_x_axis,
            )
        else:
            total_samples = sum(stacked_data)
            results_labels = []

            for value, label in zip(stacked_data, data_stack_labels):
                if not value:
                    results_labels.append("")
                else:
                    if total_samples:
                        results_labels.append(
                            label
                            + f"  {value}/{total_samples} {value / total_samples:.0%}"
                        )
                    else:
                        results_labels.append(label + f"  {value}")

            create_pie_chart(
                title,
                stacked_data,
                labels=results_labels,
                colors=data_colors,
                hatches=data_hatching,
            )
    elif isinstance(data_dictionary, defaultdict):
        if counts_plot:
            create_bar_plot(
                title + " [counts]",
                stacked_data,
                categories,
                legend_labels=data_stack_labels,
                colors=data_colors,
                hatches=data_hatching,
                label_rotation=90,
                portrait_x_axis=portrait_x_axis,
            )

        if percentile_plot:
            create_bar_plot(
                title + " [%]",
                percentile_data,
                percentile_categories,
                legend_labels=data_stack_labels,
                colors=percentile_data_colors,
                hatches=data_hatching,
                label_rotation=90,
                percentage=True,
                portrait_x_axis=portrait_x_axis,
            )
    else:
        raise ValueError


def create_data_colors(data_color_dict, data_stack_order):
    if data_color_dict is not None:
        data_colors = [data_color_dict[data_part] for data_part in data_stack_order]
        percentile_data_colors = [
            data_color_dict[data_part] for data_part in data_stack_order
        ]
    else:
        data_colors = None
        percentile_data_colors = None
    return data_colors, percentile_data_colors


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


def create_data_stacks(
    categories, percentile_categories, data_dictionary, data_sum, data_stack_order
):
    stacked_data = []
    percentile_data = []

    if isinstance(data_dictionary, defaultdict):
        if data_stack_order is None:
            data_parts = set()
            for k, v in data_dictionary.items():
                for _k, _v in v.items():
                    data_parts.add(_k)

            data_stack_order = sorted(data_parts)

        for data_part in data_stack_order:
            stacked_data.append([data_dictionary[cat][data_part] for cat in categories])
            percentile_data.append(
                [
                    0
                    if not data_sum[cat]
                    else data_dictionary[cat][data_part] / data_sum[cat]
                    for cat in percentile_categories
                ]
            )
    elif isinstance(data_dictionary, Counter):
        data_stack_order = categories
        stacked_data = [data_dictionary[cat] for cat in categories]
        percentile_data = [
            0 if not data_sum[cat] else data_dictionary[cat] / data_sum[cat]
            for cat in percentile_categories
        ]
    else:
        raise ValueError

    return data_stack_order, percentile_data, stacked_data
