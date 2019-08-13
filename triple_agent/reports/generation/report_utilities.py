import itertools
import os
from typing import List, Optional, Union

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from triple_agent.constants.paths import PORTRAITS_FOLDER
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
)


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


def _get_plot_colors(colors: Optional[List[str]], data: List[List[Union[int, float]]]):
    if colors is None:
        if len(data) == 1:
            colors = ["xkcd:green"]
        else:
            colors = itertools.repeat(None)
    return colors


def _set_y_axis_scale_and_ticks(axis, max_value, percentage):
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
            middle = (left + right) / 2
            port_start = middle - (port_size / 2)
            newax = fig.add_axes(
                [port_start, top - port_size, port_size, port_size], zorder=-1
            )
            newax.imshow(portrait_image)
            newax.axis("off")
    else:
        axis.set_xticklabels(labels, rotation=90)


def _set_axis_properties(axis, ticks, axis_labels: AxisProperties):
    axis.set_title(axis_labels.title)

    if axis_labels.y_axis_label is not None:
        axis.set_ylabel(axis_labels.y_axis_label)

    if axis_labels.x_axis_label is not None:
        axis.set_xlabel(axis_labels.x_axis_label)

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

    _create_legend_if_needed(axis, fig, data_properties.stack_labels)

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, data_properties, axis_properties.x_axis_portrait
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

    text_padding = max_value * 0.01

    current_bottom = [0] * len(data_properties.data[0])

    current_data_stack = 0

    for current_data_stack, (this_data, this_color) in enumerate(
        zip(data_properties.data, colors)
    ):
        patches = axis.bar(
            ticks, this_data, bottom=current_bottom, color=this_color, edgecolor="black"
        )
        current_bottom = [c + d for c, d in zip(current_bottom, this_data)]

        if data_properties.bar_labels is not None:
            for this_tick, this_value, this_label in zip(
                ticks, current_bottom, data_properties.bar_labels[current_data_stack]
            ):
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
        if data_properties.data_hatching is not None:
            for patch in patches:
                if data_properties.data_hatching[current_data_stack] is not None:
                    patch.set_hatch(data_properties.data_hatching[current_data_stack])

    _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

    _create_legend_if_needed(
        axis, fig, data_properties.stack_labels, data_stack_level=current_data_stack
    )

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, data_properties.category_labels, axis_properties.x_axis_portrait
    )

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def create_pie_chart(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(8, 8))

    axis.set_title(axis_properties.title)

    patches = axis.pie(
        # pie is only going to use the lowest data "stack"
        data_properties.data[0],
        labels=data_properties.category_labels,
        colors=data_properties.colors,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    if data_properties.data_hatching is not None:
        for data_hatch, patch in zip(data_properties.data_hatching, patches[0]):
            if data_hatch is not None:
                patch.set_hatch(data_hatch)

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def create_histogram(
    title,
    data,
    bin_size,
    major_locator=60,
    x_label=None,
    y_label=None,
    cumulative_also=False,
    **kwargs,
):
    fig, axis = plt.subplots(figsize=(12, 8))
    max_data_point = max(data)
    last_bin_right = bin_size * round(max_data_point / bin_size) + bin_size
    data_bins = np.arange(0, last_bin_right + bin_size, bin_size)
    cumul_bins = np.arange(0, last_bin_right + bin_size + bin_size, bin_size)
    axis.set_xlim(0, last_bin_right)

    heights, _, _ = axis.hist(data, data_bins, color="xkcd:green", edgecolor="k")

    if cumulative_also:
        axis2 = axis.twinx()
        axis2.hist(
            data,
            bins=cumul_bins,
            density=True,
            histtype="step",
            cumulative=True,
            color="xkcd:orange",
            linewidth=3,
        )

        axis2.set_ylim(0, 1)

    max_bar_value = max(heights)
    num_majors = 12
    increment = round(max_bar_value / num_majors)
    if increment < 1:
        increment = 1
    axis.yaxis.set_major_locator(MultipleLocator(increment))
    rounded_top = ((max_bar_value + increment) // increment) * increment
    axis.set_ylim(top=rounded_top)

    # axis.yaxis.set_major_locator(MultipleLocator(1))

    # TODO: figure out a better major locator size
    axis.xaxis.set_major_locator(MultipleLocator(major_locator))
    axis.xaxis.set_minor_locator(MultipleLocator(bin_size))

    axis.set_title(title)

    _set_axis_properties(axis, x_label, y_label)

    _save_fig_if_needed(fig, kwargs)

    plt.show()


def create_progress_plot(x_data, y_data, colors, title, x_label=None, y_label=None):
    _, axis = plt.subplots(figsize=(14, 10))

    for x_d, y_d, color in zip(x_data, y_data, colors):
        axis.plot(x_d, y_d, linewidth=4, alpha=0.05, color=color)

    axis.set_ylim(bottom=0)
    axis.set_xlim(left=0)

    _set_axis_properties(axis, x_label, y_label)

    axis.set_yticklabels(["{:,.0%}".format(x) for x in axis.get_yticks()])
    axis.set_xticklabels(["{:,.0%}".format(x) for x in axis.get_xticks()])

    axis.set_title(title)

    plt.show()
