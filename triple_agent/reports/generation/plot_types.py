import contextlib
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
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
    apply_data_labels,
    create_plot_hatching,
    create_data_labels,
    trim_empty_labels,
)

DARK_MODE_BACKGROUND_COLOR = "#383838"
LIGHT_MODE_BACKGROUND_COLOR = "white"

# TODO: The distinction between a single stack vs. actual stacked data needs to be more explicit.
# Right now, it's a bit of a hodge-podge with primary_order being used in both ways.


def create_line_plot(
    axis_properties: AxisProperties,
    data_properties: DataPlotProperties,
    fig: plt.Figure = None,
):
    with setup_dark_mode_context(axis_properties, fig):
        if fig is None:  # pragma: no cover
            show = True
            fig, axis = plt.subplots(
                figsize=(12, 8),
                facecolor=DARK_MODE_BACKGROUND_COLOR
                if axis_properties.dark_mode
                else LIGHT_MODE_BACKGROUND_COLOR,
            )
        else:
            show = False
            fig.set_size_inches(12, 8)
            axis = fig.subplots()

        colors = create_plot_colors(
            axis_properties.primary_color_dict,
            data_properties.frame,
            data_properties.stacks_are_categories,
        )

        category_labels, stack_labels = create_category_legend_labels(
            axis_properties.primary_label_dict,
            data_properties.frame.columns,
            data_properties.frame.index,
            data_properties.stacks_are_categories,
        )

        ticks = list(range(len(data_properties.frame.iloc[-1])))

        max_value = data_properties.frame.max().max()

        for this_data, this_color, stack_label in zip(
            data_properties.frame.itertuples(index=False), colors, stack_labels
        ):
            axis.plot(
                ticks,
                this_data,
                color=this_color[0],
                linestyle="-",
                marker="o",
                markersize=12,
                linewidth=4,
                label=stack_label,
            )

        _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

        _create_legend_if_needed(axis, fig)

        _set_axis_properties(axis, ticks, axis_properties)

        _add_portrait_x_axis_if_needed(
            axis, fig, category_labels, axis_properties.x_axis_portrait
        )

        _save_fig_if_needed(fig, axis_properties.savefig)

        if show:  # pragma: no cover
            plt.show()


def create_bar_plot(
    axis_properties: AxisProperties,
    data_properties: DataPlotProperties,
    fig: plt.Figure = None,
):
    with setup_dark_mode_context(axis_properties, fig):
        if fig is None:  # pragma: no cover
            show = True
            fig, axis = plt.subplots(
                figsize=(12, 8),
                facecolor=DARK_MODE_BACKGROUND_COLOR
                if axis_properties.dark_mode
                else LIGHT_MODE_BACKGROUND_COLOR,
            )
        else:
            show = False
            fig.set_size_inches(12, 8)
            axis = fig.subplots()

        category_labels, stack_labels = create_category_legend_labels(
            axis_properties.primary_label_dict,
            data_properties.frame.columns,
            data_properties.frame.index,
            data_properties.stacks_are_categories,
        )

        hatching = create_plot_hatching(
            axis_properties.primary_hatch_dict,
            data_properties.frame.columns,
            data_properties.frame.index,
            data_properties.stacks_are_categories,
        )

        data_labels = create_data_labels(
            data_properties.frame,
            axis_properties.data_label_style,
            axis_properties.y_axis_percentage,
        )

        ticks = list(range(len(data_properties.frame.columns)))

        max_value = max(data_properties.frame.sum())

        patches = draw_bars(axis, axis_properties, data_properties, ticks, stack_labels)

        for row_hatch, row_patches, row_data_labels in zip(
            hatching, patches, data_labels
        ):
            apply_hatches(row_hatch, row_patches)
            apply_data_labels(axis, max_value, row_patches, row_data_labels)

        _set_y_axis_scale_and_ticks(axis, max_value, axis_properties.y_axis_percentage)

        _create_legend_if_needed(axis, fig)

        _set_axis_properties(axis, ticks, axis_properties)

        _add_portrait_x_axis_if_needed(
            axis, fig, category_labels, axis_properties.x_axis_portrait
        )

        _save_fig_if_needed(fig, axis_properties.savefig)

        if show:  # pragma: no cover
            plt.show()


def draw_bars(axis, axis_properties, data_properties, ticks, stack_labels):

    colors = create_plot_colors(
        axis_properties.primary_color_dict,
        data_properties.frame,
        data_properties.stacks_are_categories,
    )

    bottoms = data_properties.frame.iloc[::-1, :].cumsum().iloc[::-1, :].values

    bottoms = np.append(
        bottoms[1:, :], np.zeros((1, bottoms.shape[1]), int), axis=0
    ).tolist()

    patches = []

    # reverse so current_bottom calculation still makes sense
    for stack, color, bottom, stack_label in zip(
        data_properties.frame.itertuples(index=False), colors, bottoms, stack_labels
    ):
        patches.append(
            axis.bar(
                x=ticks,
                height=list(stack),
                bottom=bottom,
                color=color,
                edgecolor="black",
                label=stack_label,
            )
        )

    return patches


def apply_hatches(hatching, patches):
    for data_hatch, patch in zip(hatching, patches):
        patch.set_hatch(data_hatch)


def create_pie_chart(
    axis_properties: AxisProperties,
    data_properties: DataPlotProperties,
    fig: plt.Figure = None,
):
    with setup_dark_mode_context(axis_properties, fig):
        # Pie chart assumes this will be the case, so confirm.
        assert data_properties.stacks_are_categories

        if fig is None:  # pragma: no cover
            show = True
            fig, axis = plt.subplots(
                figsize=(8, 8),
                facecolor=DARK_MODE_BACKGROUND_COLOR
                if axis_properties.dark_mode
                else LIGHT_MODE_BACKGROUND_COLOR,
            )
        else:
            show = False
            fig.set_size_inches(8, 8)
            axis = fig.subplots()

        axis.set_title(axis_properties.title)

        colors = create_plot_colors(
            axis_properties.primary_color_dict,
            data_properties.frame,
            data_properties.stacks_are_categories,
            is_pie_chart=True,
        )

        hatching = create_plot_hatching(
            axis_properties.primary_hatch_dict,
            data_properties.frame.columns,
            data_properties.frame.index,
            data_properties.stacks_are_categories,
        )

        category_labels, _ = create_category_legend_labels(
            axis_properties.primary_label_dict,
            data_properties.frame.columns,
            data_properties.frame.index,
            data_properties.stacks_are_categories,
        )

        # pie is only going to use the lowest data "stack"
        wedge_data = data_properties.frame.iloc[-1]

        trimmed_labels = trim_empty_labels(wedge_data, category_labels)

        patches, _, _ = axis.pie(
            wedge_data,
            labels=trimmed_labels,
            colors=colors[0],
            autopct=lambda x: "" if x == 0 else f"{x:1.1f}%",
            pctdistance=1.1,
            labeldistance=1.2,
            wedgeprops={"edgecolor": "black", "linewidth": 1},
        )

        apply_hatches(hatching[0], patches)

        _save_fig_if_needed(fig, axis_properties.savefig)

        if show:  # pragma: no cover
            plt.show()


def create_progress_plot(
    x_data, y_data, colors, axis_properties: AxisProperties, fig: plt.Figure = None
):
    with setup_dark_mode_context(axis_properties, fig):
        if fig is None:  # pragma: no cover
            show = True
            fig, axis = plt.subplots(
                figsize=(12, 8),
                facecolor=DARK_MODE_BACKGROUND_COLOR
                if axis_properties.dark_mode
                else LIGHT_MODE_BACKGROUND_COLOR,
            )
        else:
            show = False
            fig.set_size_inches(12, 8)
            axis = fig.subplots()

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

        if show:  # pragma: no cover
            plt.show()


def setup_dark_mode_context(axis_properties, fig):
    if axis_properties.dark_mode:
        context = plt.style.context("dark_background")
        if fig is not None:
            fig.set_facecolor(DARK_MODE_BACKGROUND_COLOR)
    else:
        context = contextlib.nullcontext()
    return context


def create_histogram(
    axis_properties: AxisProperties, data, bin_size, major_locator=60, fig=None
):
    with setup_dark_mode_context(axis_properties, fig):
        if fig is None:  # pragma: no cover
            show = True
            fig, axis = plt.subplots(
                figsize=(12, 8),
                facecolor=DARK_MODE_BACKGROUND_COLOR
                if axis_properties.dark_mode
                else LIGHT_MODE_BACKGROUND_COLOR,
            )
        else:
            show = False
            fig.set_size_inches(12, 8)
            axis = fig.subplots()

        cumulative_bins, data_bins = create_bins(bin_size, data)

        heights, _, _ = axis.hist(data, data_bins, color="xkcd:green", edgecolor="k")

        if axis_properties.cumulative_histogram:
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

        _set_axis_properties(axis, data_bins, axis_properties, tight=True)

        # TODO: figure out a better major locator size
        axis.xaxis.set_major_locator(MultipleLocator(major_locator))
        axis.xaxis.set_minor_locator(MultipleLocator(bin_size))

        _save_fig_if_needed(fig, axis_properties.savefig)

        if show:  # pragma: no cover
            plt.show()
