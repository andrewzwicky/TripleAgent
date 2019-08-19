from collections import defaultdict

import pytest
from matplotlib.testing.decorators import check_figures_equal
from matplotlib.ticker import MultipleLocator

import pandas
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
)
from triple_agent.reports.generation.plot_types import (
    create_pie_chart,
    create_bar_plot,
    create_line_plot,
)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_pie_chart_simple(test_figure, reference_figure):

    reference_figure.set_size_inches(8, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Test Title")
    ref_ax.pie(
        [1, 2, 3, 4, 4],
        labels=["A", "B", "C", "D", "E"],
        colors=["red", "blue", "black", "yellow", "white"],
        autopct="%1.1f%%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    axis_properties = AxisProperties(
        title="Test Title",
        data_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[1, 2, 3, 4, 4]], columns=["A", "B", "C", "D", "E"], index=[None]
        ),
        stacks_are_categories=True,
    )

    create_pie_chart(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_pie_chart_hatch(test_figure, reference_figure):

    reference_figure.set_size_inches(8, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Test Title")
    patches, _, _ = ref_ax.pie(
        [1, 2, 3, 4, 4],
        labels=["A", "B", "C", "D", "E"],
        colors=["red", "blue", "black", "yellow", "white"],
        autopct="%1.1f%%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )
    patches[0].set_hatch("-")

    axis_properties = AxisProperties(
        title="Test Title",
        data_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        data_hatch_dict=defaultdict(lambda: None, {"A": "-"}),
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[1, 2, 3, 4, 4]], columns=["A", "B", "C", "D", "E"], index=[None]
        ),
        stacks_are_categories=True,
    )

    create_pie_chart(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_pie_chart_stack_label_dict(test_figure, reference_figure):

    reference_figure.set_size_inches(8, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Test Title")
    patches, _, _ = ref_ax.pie(
        [1, 2, 3, 4, 4],
        labels=["ATest", "BTest", "", "", ""],
        colors=["red", "blue", "black", "yellow", "white"],
        autopct="%1.1f%%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    axis_properties = AxisProperties(
        title="Test Title",
        data_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        data_stack_label_dict=defaultdict(lambda: "", {"A": "ATest", "B": "BTest"}),
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[1, 2, 3, 4, 4]], columns=["A", "B", "C", "D", "E"], index=[None]
        ),
        stacks_are_categories=True,
    )

    create_pie_chart(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_bar_simple(test_figure, reference_figure):

    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.bar(
        [0, 1, 2, 3, 4],
        [4, 5, 7, 9, 2],
        color=["red", "blue", "black", "yellow", "white"],
        edgecolor="black",
    )
    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=10)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major", color="k")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    axis_properties = AxisProperties(
        title="Bar",
        data_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[4, 5, 7, 9, 2]], columns=["A", "B", "C", "D", "E"], index=[None]
        ),
        stacks_are_categories=True,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_bar_stacked(test_figure, reference_figure):

    reference_figure.set_size_inches(15, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.bar([0, 1, 2, 3, 4], [4, 5, 7, 9, 2], color="red", edgecolor="black")
    ref_ax.bar(
        [0, 1, 2, 3, 4],
        [1, 2, 3, 1, 6],
        color="blue",
        edgecolor="black",
        bottom=[4, 5, 7, 9, 2],
    )
    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=11)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major", color="k")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    box = ref_ax.get_position()
    ref_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ref_ax.legend(labels=["Top", "Bottom"], loc="center left", bbox_to_anchor=(1, 0.5))

    axis_properties = AxisProperties(
        title="Bar", data_color_dict={"Bottom": "red", "Top": "blue"}
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[1, 2, 3, 1, 6], [4, 5, 7, 9, 2]],
            columns=["A", "B", "C", "D", "E"],
            index=["Top", "Bottom"],
        ),
        stacks_are_categories=False,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_line_plot(test_figure, reference_figure):

    reference_figure.set_size_inches(15, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.plot(
        [0, 1, 2, 3, 4],
        [1, 2, 3, 1, 6],
        color="blue",
        linestyle="-",
        marker="o",
        markersize=12,
        linewidth=4,
    )
    ref_ax.plot(
        [0, 1, 2, 3, 4],
        [4, 5, 7, 9, 2],
        color="red",
        linestyle="-",
        marker="o",
        markersize=12,
        linewidth=4,
    )

    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=10)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major", color="k")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    box = ref_ax.get_position()
    ref_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ref_ax.legend(labels=["Top", "Bottom"], loc="center left", bbox_to_anchor=(1, 0.5))

    axis_properties = AxisProperties(
        title="Bar", data_color_dict={"Bottom": "red", "Top": "blue"}
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[1, 2, 3, 1, 6], [4, 5, 7, 9, 2]],
            columns=["A", "B", "C", "D", "E"],
            index=["Top", "Bottom"],
        ),
        stacks_are_categories=False,
    )

    create_line_plot(axis_properties, data_plot_properties, fig=test_figure)
