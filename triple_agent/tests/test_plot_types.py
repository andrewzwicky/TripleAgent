from collections import defaultdict

import pytest
from matplotlib.testing.decorators import check_figures_equal
from matplotlib.ticker import MultipleLocator

import pandas
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataPlotProperties,
    PlotLabelStyle,
)
from triple_agent.reports.generation.plot_types import (
    create_pie_chart,
    create_bar_plot,
    create_line_plot,
)

from triple_agent.classes.missions import MISSION_PLOT_ORDER
from triple_agent.classes.action_tests import ActionTest


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
def test_pie_chart_AT_labels(test_figure, reference_figure):

    reference_figure.set_size_inches(8, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("AT Pie Chart")
    ref_ax.pie(
        [1, 2, 3, 4, 4],
        labels=["Green", "White", "Red", "Canceled", "Ignored"],
        colors=[
            "xkcd:green",
            "xkcd:white",
            "xkcd:red",
            "xkcd:light grey",
            "xkcd:off white",
        ],
        autopct="%1.1f%%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    axis_properties = AxisProperties(
        title="AT Pie Chart",
        data_color_dict={
            ActionTest.Green: "xkcd:green",
            ActionTest.White: "xkcd:white",
            ActionTest.Ignored: "xkcd:off white",
            ActionTest.Red: "xkcd:red",
            ActionTest.Canceled: "xkcd:light grey",
        },
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[1, 2, 3, 4, 4]],
            columns=[
                ActionTest.Green,
                ActionTest.White,
                ActionTest.Red,
                ActionTest.Canceled,
                ActionTest.Ignored,
            ],
            index=[None],
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
    patches = ref_ax.bar(
        [0, 1, 2, 3, 4],
        [1, 2, 3, 1, 6],
        color="blue",
        edgecolor="black",
        bottom=[4, 5, 7, 9, 2],
        label="Top",
    )
    ref_ax.bar(
        [0, 1, 2, 3, 4], [4, 5, 7, 9, 2], color="red", edgecolor="black", label="Bottom"
    )

    for p in patches:
        p.set_hatch("\\")

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

    ref_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    axis_properties = AxisProperties(
        title="Bar",
        data_color_dict={"Bottom": "red", "Top": "blue"},
        data_hatch_dict={"Top": "\\", "Bottom": None},
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
        label="Top",
    )
    ref_ax.plot(
        [0, 1, 2, 3, 4],
        [4, 5, 7, 9, 2],
        color="red",
        linestyle="-",
        marker="o",
        markersize=12,
        linewidth=4,
        label="Bottom",
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

    ref_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

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


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_mission_choice_bar(test_figure, reference_figure):

    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Mission Choices")
    ref_ax.bar(
        range(8), [4, 7, 7, 7, 8, 7, 8, 8], color="xkcd:green", edgecolor="black"
    )

    ref_ax.set_xticklabels(
        [
            "Seduce",
            "Inspect",
            "Fingerprint",
            "Contact",
            "Bug",
            "Swap",
            "Purloin",
            "Transfer",
        ],
        rotation=90,
    )

    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=9)

    ref_ax.set_xlim(-0.5, 7.5)
    ref_ax.set_xticks(range(8))

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major", color="k")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    axis_properties = AxisProperties(title="Mission Choices", force_bar=True)
    data_plot_properties = DataPlotProperties(
        pandas.DataFrame(
            data=[[4, 7, 7, 7, 8, 7, 8, 8]], columns=MISSION_PLOT_ORDER, index=[None]
        ),
        stacks_are_categories=True,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_bar_simple_labels(test_figure, reference_figure):
    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.bar(
        [0, 1, 2, 3, 4],
        [4, 5, 7, 10, 2],
        color=["red", "blue", "black", "yellow", "white"],
        edgecolor="black",
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

    ref_ax.text(
        0,
        4 - (10 * 0.01),
        str(4),
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        1,
        5 - (10 * 0.01),
        str(5),
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        2,
        7 - (10 * 0.01),
        str(7),
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        3,
        10 - (10 * 0.01),
        str(10),
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        4,
        2 - (10 * 0.01),
        str(2),
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    axis_properties = AxisProperties(
        title="Bar",
        data_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        data_label_style=PlotLabelStyle.Plain,
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[4, 5, 7, 10, 2]], columns=["A", "B", "C", "D", "E"], index=[None]
        ),
        stacks_are_categories=True,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)
