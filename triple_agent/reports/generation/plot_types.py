from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
)
from triple_agent.reports.generation.report_utilities import (
    create_plot_colors,
    create_category_legend_labels,
    create_bins,
    _set_y_axis_scale_and_ticks,
    _create_legend_if_needed,
    _set_axis_properties,
    _add_portrait_x_axis_if_needed,
    _save_fig_if_needed,
    _create_data_label,
    create_plot_hatching,
    create_data_labels,
)

# TODO: The distinction between a single stack vs. actual stacked data needs to be more explicit.
# Right now, it's a bit of a hodge-podge with stack_order being used in both ways.


def create_line_plot(
    axis_properties: AxisProperties,
    data_properties: DataPlotProperties,
    fig: plt.Figure = None,
):
    if fig is None:
        show = True
        fig, axis = plt.subplots(figsize=(12, 8))
    else:
        show = False
        fig.set_size_inches(12, 8)
        axis = fig.subplots()

    colors = create_plot_colors(
        axis_properties.data_color_dict,
        data_properties.frame,
        data_properties.stacks_are_categories,
    )

    category_labels, stack_labels = create_category_legend_labels(
        axis_properties.data_stack_label_dict,
        data_properties.frame.columns,
        data_properties.frame.index,
        data_properties.stacks_are_categories,
    )

    ticks = list(range(len(data_properties.frame.iloc[-1])))

    max_value = data_properties.frame.max().max()

    for _, (this_data, this_color) in enumerate(
        zip(data_properties.frame.itertuples(index=False), colors)
    ):
        axis.plot(
            ticks,
            this_data,
            color=this_color[0],
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

    if show:
        plt.show()


def create_bar_plot(
    axis_properties: AxisProperties,
    data_properties: DataPlotProperties,
    fig: plt.Figure = None,
):
    if fig is None:
        show = True
        fig, axis = plt.subplots(figsize=(12, 8))
    else:
        show = False
        fig.set_size_inches(12, 8)
        axis = fig.subplots()

    category_labels, stack_labels = create_category_legend_labels(
        axis_properties.data_stack_label_dict,
        data_properties.frame.columns,
        data_properties.frame.index,
        data_properties.stacks_are_categories,
    )

    ticks = list(range(len(data_properties.frame.columns)))

    max_value = max(data_properties.frame.sum())

    draw_bars(axis, axis_properties, data_properties, max_value, ticks)

    _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

    _create_legend_if_needed(axis, fig, stack_labels)

    _set_axis_properties(axis, ticks, axis_properties)

    _add_portrait_x_axis_if_needed(
        axis, fig, category_labels, axis_properties.x_axis_portrait
    )

    _save_fig_if_needed(fig, axis_properties.savefig)

    if show:
        plt.show()


def draw_bars(axis, axis_properties, data_properties, max_value, ticks):
    data_labels = create_data_labels(
        data_properties.frame, axis_properties.data_label_style
    )

    colors = create_plot_colors(
        axis_properties.data_color_dict,
        data_properties.frame,
        data_properties.stacks_are_categories,
    )

    hatching = create_plot_hatching(
        axis_properties.data_hatch_dict,
        data_properties.frame.columns,
        data_properties.frame.index,
        data_properties.stacks_are_categories,
    )
    # reverse so current_bottom calculation still makes sense
    for current_data_stack, (stack, color, row_data_labels) in enumerate(
        zip(
            data_properties.frame[::-1].itertuples(index=False),
            reversed(colors),
            reversed(data_labels),
        )
    ):
        current_bottom = (
            data_properties.frame[::-1].iloc[:current_data_stack].sum().values.tolist()
        )

        patches = axis.bar(
            x=ticks,
            height=list(stack),
            bottom=current_bottom,
            color=color,
            edgecolor="black",
        )

        for tick_value_label_tuple in zip(ticks, current_bottom, row_data_labels):
            _create_data_label(axis, max_value, *tick_value_label_tuple)

        apply_hatches(
            None if hatching is None else hatching[current_data_stack], patches
        )


def apply_hatches(hatching, patches):
    if hatching is not None:
        for data_hatch, patch in zip(hatching, patches):
            if data_hatch is not None:
                patch.set_hatch(data_hatch)


def create_pie_chart(
    axis_properties: AxisProperties,
    data_properties: DataPlotProperties,
    fig: plt.Figure = None,
):
    # Pie chart assumes this will be the case, so confirm.
    assert data_properties.stacks_are_categories

    if fig is None:
        show = True
        fig, axis = plt.subplots(figsize=(8, 8))
    else:
        show = False
        fig.set_size_inches(8, 8)
        axis = fig.subplots()

    axis.set_title(axis_properties.title)

    colors = create_plot_colors(
        axis_properties.data_color_dict,
        data_properties.frame,
        data_properties.stacks_are_categories,
    )

    hatching = create_plot_hatching(
        axis_properties.data_hatch_dict,
        data_properties.frame.columns,
        data_properties.frame.index,
        data_properties.stacks_are_categories,
    )

    category_labels, _ = create_category_legend_labels(
        axis_properties.data_stack_label_dict,
        data_properties.frame.columns,
        data_properties.frame.index,
        data_properties.stacks_are_categories,
    )

    # pie is only going to use the lowest data "stack"
    wedge_data = data_properties.frame.iloc[-1]

    patches, _, _ = axis.pie(
        wedge_data,
        labels=category_labels,
        colors=colors[0],
        autopct="%1.1f%%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    apply_hatches(hatching, patches)

    _save_fig_if_needed(fig, axis_properties.savefig)

    if show:
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
