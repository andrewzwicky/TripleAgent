import itertools
import os
from typing import List, Optional, Union

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from triple_agent.utilities.paths import PORTRAITS_FOLDER


def create_line_plot(
    title: str,
    data: List[List[Union[int, float]]],
    labels: List[str],
    y_label=None,
    x_label=None,
    colors: Optional[List[str]] = None,
    legend_labels: List[str] = None,
    label_rotation: int = 0,
    percentage: bool = False,
    portrait_x_axis=False,
    # TODO: division logos on x axis
    no_show=False,
    savefig=None,
):
    if colors is None:
        if len(data) == 1:
            colors = ["xkcd:green"]
        else:
            colors = itertools.repeat(None)

    if legend_labels is not None:
        # account for space at bottom of figure
        fig, axis = plt.subplots(figsize=(12 * 1.25, 8))
    else:
        fig, axis = plt.subplots(figsize=(12, 8))
    ticks = list(range(len(data[0])))

    # make sure all individual data sets are the same length
    assert len({len(d) for d in data}) == 1

    max_bar_value = max((map(max, zip(*data))))

    axis.set_title(title)

    current_bottom = [0] * len(data[0])

    for _, (this_data, this_color) in enumerate(zip(data, colors)):
        axis.plot(
            ticks,
            this_data,
            color=this_color,
            linestyle="-",
            marker="o",
            markersize=12,
            linewidth=4,
        )
        current_bottom = [c + d for c, d in zip(current_bottom, this_data)]

    axis.set_xlim(min(ticks) - 0.5, max(ticks) + 0.5)
    axis.set_xticks(ticks)

    if percentage:
        axis.yaxis.set_major_locator(MultipleLocator(0.1))
        vals = axis.get_yticks()
        axis.set_yticklabels(["{:,.0%}".format(x) for x in vals])

        if max_bar_value >= 0.99:
            axis.set_ylim(top=1)

    else:
        num_majors = 12
        increment = round(max_bar_value / num_majors)
        if increment < 1:
            increment = 1
        axis.yaxis.set_major_locator(MultipleLocator(increment))
        rounded_top = ((max_bar_value + increment) // increment) * increment
        axis.set_ylim(top=rounded_top)

    axis.set_ylim(bottom=0)
    axis.yaxis.grid(which="major", color="k")
    axis.yaxis.grid(which="minor", linestyle="--")

    if y_label is not None:
        axis.set_ylabel(y_label)

    if x_label is not None:
        axis.set_xlabel(x_label)

    axis.set_axisbelow(True)

    if portrait_x_axis:
        axis.set_xticklabels([l + " " * 10 for l in labels], rotation=label_rotation)
    else:
        axis.set_xticklabels(labels, rotation=label_rotation)

    if legend_labels is not None:
        # Shrink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        axis.legend(labels=legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))

    if portrait_x_axis:
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

    if savefig:
        plt.savefig(savefig, bbox_inches="tight")

    if not no_show:
        plt.show()

    return axis


def create_bar_plot(
    title: str,
    data: List[List[Union[int, float]]],
    labels: List[str],
    y_label=None,
    x_label=None,
    colors: Optional[List[str]] = None,
    hatches: Optional[List[Optional[str]]] = None,
    legend_labels: List[str] = None,
    bar_labels: Optional[List[List[str]]] = None,
    label_rotation: int = 0,
    percentage: bool = False,
    portrait_x_axis=False,
    # TODO: division logos on x axis
    no_show=False,
    savefig=None,
):
    if colors is None:
        if len(data) == 1:
            colors = ["xkcd:green"]
        else:
            colors = itertools.repeat(None)

    if legend_labels is not None:
        # account for space at bottom of figure
        fig, axis = plt.subplots(figsize=(12 * 1.25, 8))
    else:
        fig, axis = plt.subplots(figsize=(12, 8))
    ticks = list(range(len(data[0])))

    # make sure all individual data sets are the same length
    assert len({len(d) for d in data}) == 1

    max_bar_value = max((map(sum, zip(*data))))
    text_padding = max_bar_value * 0.01

    axis.set_title(title)

    current_bottom = [0] * len(data[0])

    for i, (this_data, this_color) in enumerate(zip(data, colors)):
        patches = axis.bar(
            ticks, this_data, bottom=current_bottom, color=this_color, edgecolor="black"
        )
        current_bottom = [c + d for c, d in zip(current_bottom, this_data)]

        if bar_labels is not None:
            for this_tick, this_value, this_label in zip(
                ticks, current_bottom, bar_labels[i]
            ):
                if this_value != 0:
                    if this_value < max_bar_value * 0.05:
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
        if hatches is not None:
            for patch in patches:
                if hatches[i] is not None:
                    patch.set_hatch(hatches[i])

    axis.set_xlim(min(ticks) - 0.5, max(ticks) + 0.5)
    axis.set_xticks(ticks)

    if percentage:
        axis.yaxis.set_major_locator(MultipleLocator(0.1))
        vals = axis.get_yticks()
        axis.set_yticklabels(["{:,.0%}".format(x) for x in vals])

        if max_bar_value >= 0.99:
            axis.set_ylim(top=1)

    else:
        num_majors = 12
        increment = round(max_bar_value / num_majors)
        if increment < 1:
            increment = 1
        axis.yaxis.set_major_locator(MultipleLocator(increment))
        rounded_top = ((max_bar_value + increment) // increment) * increment
        axis.set_ylim(top=rounded_top)

    axis.set_ylim(bottom=0)
    axis.yaxis.grid(which="major", color="k")
    axis.yaxis.grid(which="minor", linestyle="--")

    if y_label is not None:
        axis.set_ylabel(y_label)

    if x_label is not None:
        axis.set_xlabel(x_label)

    axis.set_axisbelow(True)

    if portrait_x_axis:
        axis.set_xticklabels([l + " " * 10 for l in labels], rotation=label_rotation)
    else:
        axis.set_xticklabels(labels, rotation=label_rotation)

    if legend_labels is not None:
        # Shrink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis
        axis.legend(labels=legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))

    if portrait_x_axis:
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

    if savefig:
        plt.savefig(savefig, bbox_inches="tight")

    if not no_show:
        plt.show()

    return axis


def create_pie_chart(title, data, labels, colors=None, hatches=None, savefig=None):
    _, axis = plt.subplots(figsize=(8, 8))

    axis.set_title(title)

    patches = axis.pie(
        data,
        labels=labels,
        colors=colors,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    if hatches is not None:
        for data_hatch, patch in zip(hatches, patches[0]):
            if data_hatch is not None:
                patch.set_hatch(data_hatch)

    if savefig:
        plt.savefig(savefig, bbox_inches="tight")

    plt.show()


def create_histogram(
    title,
    data,
    bin_size,
    major_locator=60,
    x_label=None,
    y_label=None,
    cumulative_also=False,
    savefig=None,
):
    _, axis = plt.subplots(figsize=(12, 8))
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

    if y_label is not None:
        axis.set_ylabel(y_label)

    if x_label is not None:
        axis.set_xlabel(x_label)

    if savefig:
        plt.savefig(savefig, bbox_inches="tight")

    plt.show()


def create_overlapping_lines_plot(
    title: str,
    data: List[List[List[Union[int, float]]]],
    colors: Optional[List[str]] = None,
    alpha: float = 0.05,
    y_label: Optional[str] = None,
    x_label: Optional[str] = None,
):
    _, axis = plt.subplots(figsize=(14, 10))

    x_vals, y_vals = data

    for time, progress, color in zip(x_vals, y_vals, colors):
        axis.plot(time, progress, linewidth=4, alpha=alpha, color=color)

    axis.set_ylim(bottom=0)
    axis.set_xlim(left=0)

    if y_label is not None:
        axis.set_ylabel(y_label)

    if x_label is not None:
        axis.set_xlabel(x_label)

    axis.set_yticklabels(["{:,.0%}".format(x) for x in axis.get_yticks()])
    axis.set_xticklabels(["{:,.0%}".format(x) for x in axis.get_xticks()])

    axis.set_title(title)
    plt.show()
