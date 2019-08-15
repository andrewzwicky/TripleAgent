import itertools
import os
from typing import List, Optional, Union, Any, Dict, Iterator
from enum import Enum

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from triple_agent.constants.paths import PORTRAITS_FOLDER
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
    PlotLabelStyle,
)


def labelify(unknown_item: Any, label_name_dictionary: Optional[Dict[Any, str]] = None):
    if label_name_dictionary is not None:
        return label_name_dictionary[unknown_item]

    if isinstance(unknown_item, Enum):
        return unknown_item.name

    if isinstance(unknown_item, float):
        # TODO: check this for other use cases
        return f"{unknown_item:3>.5}"

    return str(unknown_item)


def _save_fig_if_needed(fig, savefig):
    if savefig:
        fig.savefig(savefig, bbox_inches="tight")


def _create_legend_if_needed(
    axis, fig, stack_labels: Optional[List[str]], data_stack_level=None
):
    if stack_labels is not None and (data_stack_level is None or data_stack_level > 0):
        # resize the plot to allow size for legend.
        # increase figure by 25%
        width, height = fig.get_size_inches()
        fig.set_size_inches((width * 1.25, height), forward=True)

        # Shrink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        axis.legend(labels=stack_labels, loc="center left", bbox_to_anchor=(1, 0.5))


def _get_plot_colors(
    data_color_dict: Dict[Any, str],
    data: List[List[Union[int, float]]],
    stack_order: Optional[List[Any]],
) -> Union[List[Optional[str]], Iterator[Optional[str]]]:
    if data_color_dict is None:
        if len(data) == 1:
            return ["xkcd:green"]
        else:
            return itertools.repeat(None)
    else:
        return [data_color_dict[data_part] for data_part in stack_order]


def _get_plot_hatching(
    data_hatch_dict: Dict[Any, str], stack_order: Optional[List[Any]]
):
    if data_hatch_dict is None:
        return itertools.repeat(None)
    else:
        return [data_hatch_dict[data_part] for data_part in stack_order]


def _set_y_axis_scale_and_ticks(axis, max_value: Union[int, float], percentage: bool):
    if percentage:
        axis.yaxis.set_major_locator(MultipleLocator(0.1))
        vals = axis.get_yticks()
        axis.set_yticklabels(["{:,.0%}".format(x) for x in vals])

        if max_value >= 0.99:
            axis.set_ylim(top=1)

    else:
        num_majors = 12
        increment = round(max_value / num_majors)
        if increment < 1:
            increment = 1
        axis.yaxis.set_major_locator(MultipleLocator(increment))
        rounded_top = ((max_value + increment) // increment) * increment
        axis.set_ylim(top=rounded_top)


def _add_portrait_x_axis_if_needed(axis, fig, labels, portrait_x_axis):
    if portrait_x_axis:
        axis.set_xticklabels([l + " " * 10 for l in labels], rotation=90)
        fig.canvas.draw()
        for label in axis.xaxis.get_ticklabels():
            ext = label.get_window_extent()
            name = label.get_text().strip().lower()
            [[left, _], [right, top]] = fig.transFigure.inverted().transform(ext)

            portrait_image = plt.imread(
                os.path.join(PORTRAITS_FOLDER, "{}.png".format(name))
            )
            port_size = 0.045
            port_start = ((left + right) / 2) - (port_size / 2)
            newax = fig.add_axes(
                [port_start, top - port_size, port_size, port_size], zorder=-1
            )
            newax.imshow(portrait_image)
            newax.axis("off")
    else:
        axis.set_xticklabels(labels, rotation=90)


def _set_axis_properties(axis, ticks, axis_properties: AxisProperties):
    axis.set_title(axis_properties.title)

    if axis_properties.y_axis_label is not None:
        axis.set_ylabel(axis_properties.y_axis_label)

    if axis_properties.x_axis_label is not None:
        axis.set_xlabel(axis_properties.x_axis_label)

    axis.set_xlim(min(ticks) - 0.5, max(ticks) + 0.5)
    axis.set_xticks(ticks)

    axis.set_ylim(bottom=0)

    axis.yaxis.grid(which="major", color="k")
    axis.yaxis.grid(which="minor", linestyle="--")
    axis.set_axisbelow(True)


def create_line_plot(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(12, 8))

    colors = _get_plot_colors(data_properties.colors, data_properties.data)

    ticks = list(range(len(data_properties.data[0])))

    # make sure all individual data sets are the same length
    assert len({len(d) for d in data_properties.data}) == 1

    max_value = max((map(max, zip(*data_properties.data))))

    for _, (this_data, this_color) in enumerate(zip(data_properties.data, colors)):
        axis.plot(
            ticks,
            this_data,
            color=this_color,
            linestyle="-",
            marker="o",
            markersize=12,
            linewidth=4,
        )

    _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

    _create_legend_if_needed(axis, fig, data_properties.stack_order)

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, data_properties.category_order, axis_properties.x_axis_portrait
    )

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def create_bar_plot(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(12, 8))

    colors = _get_plot_colors(data_properties.colors, data_properties.data)

    ticks = list(range(len(data_properties.data[0])))

    # make sure all individual data sets are the same length
    assert len({len(d) for d in data_properties.data}) == 1

    max_value = max((map(sum, zip(*data_properties.data))))

    current_bottom = [0] * len(data_properties.data[0])

    current_data_stack = 0

    for current_data_stack, (this_data, this_color) in enumerate(
        zip(data_properties.data, colors)
    ):
        patches = axis.bar(
            ticks, this_data, bottom=current_bottom, color=this_color, edgecolor="black"
        )
        current_bottom = [c + d for c, d in zip(current_bottom, this_data)]

        if data_properties.data_labels is not None:
            for tick_value_label_tuple in zip(
                ticks, current_bottom, data_properties.data_labels[current_data_stack]
            ):
                _create_data_label(axis, max_value, *tick_value_label_tuple)

        if data_properties.hatching is not None:
            for patch in patches:
                if data_properties.hatching[current_data_stack] is not None:
                    patch.set_hatch(data_properties.hatching[current_data_stack])

    _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

    _create_legend_if_needed(
        axis, fig, data_properties.stack_order, data_stack_level=current_data_stack
    )

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, data_properties.category_order, axis_properties.x_axis_portrait
    )

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def _create_data_label(axis, max_value, this_label, this_tick, this_value):
    text_padding = max_value * 0.01

    if this_value != 0:
        if this_value < max_value * 0.05:
            y_value = this_value + text_padding
            v_align = "bottom"
        else:
            y_value = this_value - text_padding
            v_align = "top"

        axis.text(
            this_tick,
            y_value,
            str(this_label),
            color="black",
            horizontalalignment="center",
            verticalalignment=v_align,
        )


def trim_empty_labels(
    wedge_data: List[Union[int, float]], stack_labels: List[str]
) -> List[str]:
    # assume if plotting pie chart, only 1 stack is present
    total_samples = sum(wedge_data)
    results_labels = []
    for value, label in zip(wedge_data, stack_labels):
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

    return results_labels


def create_pie_chart(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(8, 8))

    axis.set_title(axis_properties.title)
    hatching = _get_plot_hatching(
        axis_properties.data_hatch_dict, data_properties.stack_order
    )

    # pie is only going to use the lowest data "stack"
    wedge_data = data_properties.data[0]
    wedge_labels = trim_empty_labels(
        wedge_data, [labelify(item) for item in data_properties.stack_order]
    )

    patches = axis.pie(
        data_properties.data[0],
        labels=wedge_labels,
        colors=data_properties.colors,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    if hatching is not None:
        for data_hatch, patch in zip(hatching, patches[0]):
            if data_hatch is not None:
                patch.set_hatch(data_hatch)

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def create_histogram(
    axis_properties: AxisProperties,
    data,
    bin_size,
    major_locator=60,
    cumulative_also=False,
    **kwargs,
):
    fig, axis = plt.subplots(figsize=(12, 8))

    cumulative_bins, data_bins = create_bins(bin_size, data)

    heights, _, _ = axis.hist(data, data_bins, color="xkcd:green", edgecolor="k")

    if cumulative_also:
        axis2 = axis.twinx()
        axis2.hist(
            data,
            bins=cumulative_bins,
            density=True,
            histtype="step",
            cumulative=True,
            color="xkcd:orange",
            linewidth=3,
        )

        axis2.set_ylim(0, 1)

    _set_y_axis_scale_and_ticks(axis, max(heights), False)

    # TODO: figure out a better major locator size
    axis.xaxis.set_major_locator(MultipleLocator(major_locator))
    axis.xaxis.set_minor_locator(MultipleLocator(bin_size))

    _set_axis_properties(axis, data_bins, axis_properties)

    _save_fig_if_needed(fig, kwargs)

    plt.show()


def create_bins(bin_size, data):
    max_data_point = max(data)
    last_bin_right = bin_size * round(max_data_point / bin_size) + bin_size
    data_bins = np.arange(0, last_bin_right + bin_size, bin_size)
    cumul_bins = np.arange(0, last_bin_right + bin_size + bin_size, bin_size)

    return cumul_bins, data_bins


def create_progress_plot(x_data, y_data, colors, axis_properties: AxisProperties):
    _, axis = plt.subplots(figsize=(14, 10))

    for x_d, y_d, color in zip(x_data, y_data, colors):
        axis.plot(x_d, y_d, linewidth=4, alpha=0.05, color=color)

    axis.set_ylim(bottom=0)
    axis.set_xlim(left=0)

    axis.set_yticklabels(["{:,.0%}".format(x) for x in axis.get_yticks()])
    axis.set_xticklabels(["{:,.0%}".format(x) for x in axis.get_xticks()])

    axis.set_title(axis_properties.title)

    if axis_properties.y_axis_label is not None:
        axis.set_ylabel(axis_properties.y_axis_label)

    if axis_properties.x_axis_label is not None:
        axis.set_xlabel(axis_properties.x_axis_label)

    plt.show()


def create_data_hatching(
    data_hatch_dict: Optional[Dict[Any, Optional[str]]], stack_order: List[Any]
) -> Optional[List[Optional[str]]]:
    if data_hatch_dict is not None:
        return [data_hatch_dict[plot_order_item] for plot_order_item in stack_order]

    return None
