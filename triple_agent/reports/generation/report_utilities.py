import os
from typing import List, Optional, Union, Any, Dict, Tuple
from enum import Enum

from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas
from triple_agent.constants.paths import PORTRAITS_FOLDER
from triple_agent.reports.generation.plot_specs import AxisProperties, PlotLabelStyle


def labelify(unknown_item: Any, percentage: bool = False):
    if isinstance(unknown_item, Enum):
        try:
            return unknown_item.stringify()
        except AttributeError:
            return unknown_item.name

    if isinstance(unknown_item, float):
        # TODO: check this for other use cases
        if percentage:
            return f"{unknown_item*100:2.1f}"
        return f"{unknown_item:04.2f}"

    return str(unknown_item)


def _save_fig_if_needed(fig, savefig):  # pragma: no cover
    if savefig:
        fig.savefig(savefig, bbox_inches="tight", transparent=True)


def _create_legend_if_needed(axis, fig):
    handles, _ = axis.get_legend_handles_labels()
    if handles:
        # resize the plot to allow size for legend.
        # increase figure by 25%
        _, height = fig.get_size_inches()
        fig.set_size_inches((15, height), forward=True)

        # Shrink current axis by 20%
        box = axis.get_position()
        axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        # Put a legend to the right of the current axis

        axis.legend(loc="center left", bbox_to_anchor=(1, 0.5))


def create_category_legend_labels(
    primary_label_dict: Dict[Any, str],
    columns: List[Any],
    index: List[Any],
    stacks_are_categories: bool = False,
) -> Tuple[List[str], List[Optional[str]]]:
    if stacks_are_categories:
        if primary_label_dict is None:
            return list(map(labelify, columns)), [None for _ in index]

        return (
            [primary_label_dict[data_part] for data_part in columns],
            [None for _ in index],
        )

    if primary_label_dict is None:
        return list(map(labelify, columns)), list(map(labelify, index))

    return (
        list(map(labelify, columns)),
        [primary_label_dict[data_part] for data_part in index],
    )


def create_plot_colors(
    primary_color_dict: Optional[Dict[Any, Optional[str]]],
    frame: pandas.DataFrame,
    stacks_are_categories: bool = False,
    is_pie_chart: bool = False,
) -> List[Optional[List[str]]]:
    if stacks_are_categories:
        if primary_color_dict is None:
            if is_pie_chart:
                return [None for _ in frame.index]

            return frame.applymap(lambda x: "xkcd:green").values.tolist()

        # For some reason, the same operation with index being set to arrays, etc.
        # wouldn't correctly turn the indexs into a list, they would remain np arrays.
        # The strange .T will flip it back and forth to get the right values.
        stack_colors = frame.T.index.map(lambda x: primary_color_dict[x]).values
        return frame.T.apply(lambda x: stack_colors, axis="index").values.T.tolist()

    if primary_color_dict is None:
        return [None for _ in frame.index]

    stack_colors = frame.index.map(lambda x: primary_color_dict[x]).values
    return frame.apply(lambda x: stack_colors, axis="index").values.tolist()

    # return itertools.cycle(primary_color_dict[data_part] for data_part in index)


def create_data_labels(
    frame: pandas.DataFrame,
    data_label_style: PlotLabelStyle = PlotLabelStyle.NoLabels,
    percentage: bool = False,
) -> List[List[str]]:
    if data_label_style == PlotLabelStyle.Plain:
        return [
            [labelify(item, percentage) for item in stack]
            for stack in frame.itertuples(index=False)
        ]

    return [["" for _ in stack] for stack in frame.itertuples(index=False)]


def create_plot_hatching(
    primary_hatch_dict: Dict[Any, str],
    columns: List[Any],
    index: List[Any],
    stacks_are_categories: bool = False,
) -> List[List[Optional[str]]]:
    if primary_hatch_dict is None:
        return [[None for _ in columns] for _ in index]

    if stacks_are_categories:
        return [[primary_hatch_dict[data_part] for data_part in columns] for _ in index]

    return [[primary_hatch_dict[data_part] for _ in columns] for data_part in index]


def _set_y_axis_scale_and_ticks(axis, max_value: Union[int, float], percentage: bool):
    if percentage:
        axis.yaxis.set_major_locator(MultipleLocator(0.1))
        vals = axis.get_yticks()
        axis.set_yticklabels(["{:,.0%}".format(x) for x in vals])

        if max_value >= 0.99:
            axis.set_ylim(top=1)

    else:
        num_majors = 12
        increment = max(round(max_value / num_majors), 1)
        if max_value < 1:
            increment = 0.1
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


def _set_axis_properties(axis, ticks, axis_properties: AxisProperties, tight=False):
    axis.set_title(axis_properties.title)

    if axis_properties.y_axis_label is not None:
        axis.set_ylabel(axis_properties.y_axis_label)

    if axis_properties.x_axis_label is not None:
        axis.set_xlabel(axis_properties.x_axis_label)

    if tight:
        axis.set_xlim(min(ticks), max(ticks))
    else:
        axis.set_xlim(min(ticks) - 0.5, max(ticks) + 0.5)

    axis.set_xticks(ticks)

    axis.set_ylim(bottom=0)

    axis.yaxis.grid(which="major")
    axis.yaxis.grid(which="minor", linestyle="--")
    axis.set_axisbelow(True)


def apply_data_labels(axis, max_value, bar_patches, row_data_labels):
    text_padding = max_value * 0.01

    for this_patch, this_label in zip(bar_patches, row_data_labels):
        if this_patch.get_height() != 0:
            if this_patch.get_height() + this_patch.get_y() < max_value * 0.05:
                y_value = this_patch.get_height() + this_patch.get_y() + text_padding
                v_align = "bottom"
            else:
                y_value = this_patch.get_height() + this_patch.get_y() - text_padding
                v_align = "top"

            axis.text(
                this_patch.get_x() + (this_patch.get_width() / 2),
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
    results_labels = []
    for value, label in zip(wedge_data, stack_labels):
        if not value:
            results_labels.append("")
        else:
            results_labels.append(labelify(label))

    return results_labels


def create_bins(bin_size, data):
    max_data_point = max(data)
    last_bin_right = bin_size * round(max_data_point / bin_size) + bin_size
    data_bins = np.arange(0, last_bin_right + bin_size, bin_size)
    cumul_bins = np.arange(0, last_bin_right + bin_size + bin_size, bin_size)

    return cumul_bins, data_bins
