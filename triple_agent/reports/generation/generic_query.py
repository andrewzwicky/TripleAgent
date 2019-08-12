from collections import Counter, defaultdict
from enum import Enum
from typing import List, Callable, Optional, Any, Dict, Union

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
    force_line=False,
    portrait_x_axis=False,
    savefig=None,
):
    """
    query is the default plotting interface.  Given a list of games/sets, and a function to
    classidy them, it will plot either a pie chart, bar plot, or stacked bar plot.  Can be used to
    created simple queries quickly.
    """

    # create data dictionary
    data_dictionary_count, data_dictionary_percent = create_data_dictionaries(
        games, query_function, groupby
    )

    # create the list of x-axis categories. percentile needs to be it's own list
    # so it can be separately sorted between the counts plot and the percentile plot
    categories_counts = create_sorted_categories(
        data_dictionary_count,
        category_data_order,
        reversed_data_sort,
        category_name_order,
    )
    categories_percent = create_sorted_categories(
        data_dictionary_percent,
        category_data_order,
        reversed_data_sort,
        category_name_order,
    )

    # limit categories to reduce clutter
    categories_counts = limit_categories(categories_counts, limit)
    categories_percent = limit_categories(categories_percent, limit)

    # sort
    data_stack_order_counts, stacked_data = create_data_stacks(
        categories_counts, data_dictionary_count, data_stack_order
    )
    data_stack_order_percent, stacked_data_percent = create_data_stacks(
        categories_percent, data_dictionary_percent, data_stack_order
    )

    # TODO: reversed legend labels/handles
    # create data stack labels
    data_stack_labels_counts = create_data_plot_labels(
        data_stack_label_dict, data_stack_order_counts
    )
    data_stack_labels_percent = create_data_plot_labels(
        data_stack_label_dict, data_stack_order_percent
    )

    data_colors_counts = create_data_colors(data_color_dict, data_stack_order_counts)
    data_colors_percent = create_data_colors(data_color_dict, data_stack_order_percent)

    # TODO: add in y-axis labels, etc.

    if isinstance(data_dictionary_count, Counter):
        if force_bar:
            create_bar_plot(
                title,
                [stacked_data],
                labels=data_stack_labels_counts,
                bar_labels=[[labelify(d) for d in stacked_data]],
                # legend_labels=data_stack_labels,
                colors=data_colors_counts,
                hatches=data_hatching,
                label_rotation=90,
                portrait_x_axis=portrait_x_axis,
                savefig=savefig,
            )

        elif force_line:
            create_line_plot(
                title,
                [stacked_data],
                labels=data_stack_labels_counts,
                colors=data_colors_counts,
                label_rotation=90,
                portrait_x_axis=portrait_x_axis,
                savefig=savefig,
            )
        else:
            total_samples = sum(stacked_data)
            results_labels = []

            for value, label in zip(stacked_data, data_stack_labels_counts):
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
                colors=data_colors_counts,
                hatches=data_hatching,
                savefig=savefig,
            )
    elif isinstance(data_dictionary_count, defaultdict):
        if counts_plot:
            if force_line:
                create_line_plot(
                    title + " [counts]",
                    stacked_data,
                    categories_counts,
                    legend_labels=data_stack_labels_counts,
                    colors=data_colors_counts,
                    label_rotation=90,
                    portrait_x_axis=portrait_x_axis,
                    savefig=savefig,
                )
            else:
                create_bar_plot(
                    title + " [counts]",
                    stacked_data,
                    categories_counts,
                    legend_labels=data_stack_labels_counts,
                    colors=data_colors_counts,
                    hatches=data_hatching,
                    label_rotation=90,
                    portrait_x_axis=portrait_x_axis,
                    savefig=savefig,
                )

        if percentile_plot:
            if force_line:
                create_line_plot(
                    title + " [%]",
                    stacked_data_percent,
                    categories_percent,
                    legend_labels=data_stack_labels_percent,
                    colors=data_colors_percent,
                    label_rotation=90,
                    percentage=True,
                    portrait_x_axis=portrait_x_axis,
                    savefig=savefig,
                )
            else:
                create_bar_plot(
                    title + " [%]",
                    stacked_data_percent,
                    categories_percent,
                    legend_labels=data_stack_labels_percent,
                    colors=data_colors_percent,
                    hatches=data_hatching,
                    label_rotation=90,
                    percentage=True,
                    portrait_x_axis=portrait_x_axis,
                    savefig=savefig,
                )
    else:
        raise ValueError


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
