import itertools
from collections import Counter, defaultdict
from enum import Enum
from typing import List, Callable, Optional, Any, Dict

from triple_agent.reports.report_utilities import create_pie_chart, create_bar_plot
from triple_agent.utilities.game import Game


def query(
    games: List[Game],
    title: str,
    query_function: Callable,
    data_plot_order: List[Any] = None,
    data_color_dict: Dict[str, str] = None,
    data_hatching: List[Optional[str]] = None,
    groupby: Callable = None,
    order: Callable = None,
    sort_data_item: Any = None,
    reversed_data_sort: bool = False,
    limit: Optional[int] = None,
    counts_plot: bool = True,
    percentile_plot: bool = True,
    data_item_label_dict: Dict[Any, str] = None,
):

    data_dictionary = defaultdict(Counter)

    if groupby is None:
        groupby = lambda g: True

    if order is None:
        order = lambda g: True

    for category, cat_games in itertools.groupby(
        sorted(games, key=groupby), key=groupby
    ):
        query_function(cat_games, data_dictionary[category])

    categories = list(data_dictionary.keys())
    percentile_categories = list(data_dictionary.keys())

    stacked_data = []
    percentile_data = []

    data_sum = {cat: sum(data_dictionary[cat].values()) for cat in categories}

    if sort_data_item is not None:
        if sort_data_item is sum:
            categories.sort(
                key=lambda c: 0
                if not data_sum[c]
                else -sum(data_dictionary[c].values())
            )
            percentile_categories.sort(
                key=lambda c: 0
                if not data_sum[c]
                else -sum(data_dictionary[c].values())
            )
        elif callable(sort_data_item):
            categories.sort(key=lambda c: sort_data_item(data_dictionary[c], None))
            percentile_categories.sort(
                key=lambda c: sort_data_item(data_dictionary[c], data_sum[c])
            )
        else:
            categories.sort(
                key=lambda c: 0
                if not data_sum[c]
                else -data_dictionary[c][sort_data_item]
            )
            percentile_categories.sort(
                key=lambda c: 0
                if not data_sum[c]
                else -data_dictionary[c][sort_data_item] / data_sum[c]
            )

        if reversed_data_sort:
            categories = list(reversed(categories))
            percentile_categories = list(reversed(percentile_categories))
    else:
        categories.sort(key=order)
        percentile_categories.sort(key=order)

    if limit is not None:
        if limit < len(categories):
            categories = categories[:limit]
            percentile_categories = percentile_categories[:limit]

    if data_plot_order is None:
        data_parts = set()
        for k, v in data_dictionary.items():
            for _k, _v in v.items():
                data_parts.add(_k)

        data_plot_order = sorted(data_parts)

    for data_part in data_plot_order:
        stacked_data.append([data_dictionary[cat][data_part] for cat in categories])
        percentile_data.append(
            [
                0
                if not data_sum[cat]
                else data_dictionary[cat][data_part] / data_sum[cat]
                for cat in percentile_categories
            ]
        )

    if data_item_label_dict is not None:
        data_plot_order_labels = [
            data_item_label_dict[plot_order_item] for plot_order_item in data_plot_order
        ]

    else:
        data_plot_order_labels = [
            plot_order_item.name
            if isinstance(plot_order_item, Enum)
            else str(plot_order_item)
            for plot_order_item in data_plot_order
        ]

    if data_color_dict:
        data_colors = [data_color_dict[data_part] for data_part in data_plot_order]
        percentile_data_colors = [
            data_color_dict[data_part] for data_part in data_plot_order
        ]
    else:
        data_colors = None
        percentile_data_colors = None

    if categories == [True]:
        results_values = [stack[0] for stack in stacked_data]
        results_sum = sum(results_values)

        results_labels = []
        for value, label in zip(results_values, data_plot_order_labels):
            if not value:
                results_labels.append("")
            else:
                if results_sum:
                    results_labels.append(
                        label + f"  {value}/{results_sum} {value / results_sum:.0%}"
                    )
                else:
                    results_labels.append(label + f"  {value}")

        create_pie_chart(
            title,
            results_values,
            labels=results_labels,
            colors=data_colors,
            hatches=data_hatching,
        )

    else:
        if counts_plot:
            create_bar_plot(
                title + " [counts]",
                stacked_data,
                categories,
                legend_labels=data_plot_order_labels,
                colors=data_colors,
                hatches=data_hatching,
                label_rotation=90,
            )

        if percentile_plot:
            create_bar_plot(
                title + " [%]",
                percentile_data,
                percentile_categories,
                legend_labels=data_plot_order_labels,
                colors=percentile_data_colors,
                hatches=data_hatching,
                label_rotation=90,
                percentage=True,
            )
