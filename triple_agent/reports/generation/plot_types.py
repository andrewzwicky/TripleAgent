from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
)
from triple_agent.reports.generation.report_utilities import (
    create_plot_colors,
    create_bins,
    _set_y_axis_scale_and_ticks,
    _create_legend_if_needed,
    _set_axis_properties,
    _add_portrait_x_axis_if_needed,
    _save_fig_if_needed,
    _create_data_label,
    create_plot_hatching,
    create_stack_labels,
    create_category_labels,
    _get_data_labels,
)


"""
TODO: The distinction between a single stack vs. actual stacked data needs to be more explicit.
Right now, it's a bit of a hodge-podge with stack_order being used in both ways.
"""


def create_line_plot(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(12, 8))

    colors = create_plot_colors(
        axis_properties.data_color_dict, data_properties.stack_order
    )

    stack_labels = create_stack_labels(
        axis_properties.data_stack_label_dict, data_properties.stack_order
    )

    category_labels = create_category_labels(data_properties.category_order)

    ticks = list(range(len(data_properties.data[0])))

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

    _create_legend_if_needed(axis, fig, stack_labels)

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, category_labels, axis_properties.x_axis_portrait
    )

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def create_bar_plot(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(12, 8))

    colors = create_plot_colors(
        axis_properties.data_color_dict, data_properties.stack_order
    )

    hatching = create_plot_hatching(
        axis_properties.data_hatch_dict, data_properties.stack_order
    )

    stack_labels = create_stack_labels(
        axis_properties.data_stack_label_dict, data_properties.stack_order
    )

    category_labels = create_category_labels(data_properties.category_order)

    data_labels = _get_data_labels(
        data_properties.data, axis_properties.data_label_style
    )
    ticks = list(range(len(data_properties.data[0])))

    max_value = max((map(sum, zip(*data_properties.data))))

    current_bottom = [0] * len(data_properties.data[0])

    for current_data_stack, (this_data, this_color) in enumerate(
        zip(data_properties.data, colors)
    ):
        patches = axis.bar(
            ticks, this_data, bottom=current_bottom, color=this_color, edgecolor="black"
        )
        current_bottom = [c + d for c, d in zip(current_bottom, this_data)]

        if data_labels is not None:
            for tick_value_label_tuple in zip(
                ticks, current_bottom, data_labels[current_data_stack]
            ):
                _create_data_label(axis, max_value, *tick_value_label_tuple)

        if hatching is not None:
            for patch in patches:
                if hatching[current_data_stack] is not None:
                    patch.set_hatch(hatching[current_data_stack])

    _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

    _create_legend_if_needed(axis, fig, stack_labels)

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, category_labels, axis_properties.x_axis_portrait
    )

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


def create_pie_chart(
    axis_properties: AxisProperties, data_properties: DataPlotProperties
):
    fig, axis = plt.subplots(figsize=(8, 8))

    axis.set_title(axis_properties.title)

    colors = create_plot_colors(
        axis_properties.data_color_dict, data_properties.category_order
    )

    hatching = create_plot_hatching(
        axis_properties.data_hatch_dict, data_properties.category_order
    )

    category_labels = create_category_labels(data_properties.category_order)

    # pie is only going to use the lowest data "stack"
    wedge_data = data_properties.data[0]

    # wedge_labels = trim_empty_labels(
    #     wedge_data, [labelify(item) for item in data_properties.stack_order]
    # )

    patches = axis.pie(
        wedge_data,
        labels=category_labels,
        colors=colors,
        autopct="%1.1f%%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    if hatching is not None:
        for data_hatch, patch in zip(hatching, patches[0]):
            if data_hatch is not None:
                patch.set_hatch(data_hatch)

    _save_fig_if_needed(fig, axis_properties.savefig)

    plt.show()


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
