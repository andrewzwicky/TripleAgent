from collections import defaultdict
import os


import pytest
from matplotlib.testing.decorators import check_figures_equal
from matplotlib.ticker import MultipleLocator
from matplotlib import pyplot as plt

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
    create_histogram,
    create_progress_plot,
)

from triple_agent.classes.missions import MISSION_PLOT_ORDER
from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.characters import Characters
from triple_agent.constants.paths import PORTRAITS_FOLDER


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
        primary_color_dict={
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


# @pytest.mark.plotting
# @pytest.mark.matplotlib
# @check_figures_equal(extensions=["png"])
# def test_pie_chart_simple_dark_mode(test_figure, reference_figure):
#
#     reference_figure.set_size_inches(8, 8)
#     reference_figure.set_facecolor("black")
#     ref_ax = reference_figure.subplots()
#     ref_ax.set_title("Test Title")
#     ref_ax.pie(
#         [1, 2, 3, 4, 4],
#         labels=["A", "B", "C", "D", "E"],
#         colors=["red", "blue", "black", "yellow", "white"],
#         autopct="%1.1f%%",
#         pctdistance=1.1,
#         labeldistance=1.2,
#         wedgeprops={"edgecolor": "white", "linewidth": 1},
#     )
#
#     axis_properties = AxisProperties(
#         title="Test Title",
#         primary_color_dict={
#             "A": "red",
#             "B": "blue",
#             "C": "black",
#             "D": "yellow",
#             "E": "white",
#         },
#         dark_mode=True,
#     )
#     data_plot_properties = DataPlotProperties(
#         frame=pandas.DataFrame(
#             data=[[1, 2, 3, 4, 4]], columns=["A", "B", "C", "D", "E"], index=[None]
#         ),
#         stacks_are_categories=True,
#     )
#
#     create_pie_chart(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_pie_chart_simple_zero_wedge(test_figure, reference_figure):

    reference_figure.set_size_inches(8, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Test Title")
    ref_ax.pie(
        [0, 2, 3, 4, 4],
        labels=["", "B", "C", "D", "E"],
        colors=["red", "blue", "black", "yellow", "white"],
        autopct=lambda x: "" if x == 0 else f"{x:1.1f}%",
        pctdistance=1.1,
        labeldistance=1.2,
        wedgeprops={"edgecolor": "k", "linewidth": 1},
    )

    axis_properties = AxisProperties(
        title="Test Title",
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[0, 2, 3, 4, 4]], columns=["A", "B", "C", "D", "E"], index=[None]
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
        primary_color_dict={
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
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        primary_hatch_dict=defaultdict(lambda: None, {"A": "-"}),
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
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        primary_label_dict=defaultdict(lambda: "", {"A": "ATest", "B": "BTest"}),
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

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    axis_properties = AxisProperties(
        title="Bar",
        primary_color_dict={
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
def test_bar_simple_short_data_label(test_figure, reference_figure):
    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.bar([0, 1], [0.1, 5], color=["red", "blue"], edgecolor="black")
    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=6)

    ref_ax.set_xlim(-0.5, 1.5)
    ref_ax.set_xticks([0, 1])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B"], rotation=90)

    ref_ax.text(
        1,
        5 - (5 * 0.01),
        "5",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        0,
        0.1 + (5 * 0.01),
        "0.10",
        color="black",
        horizontalalignment="center",
        verticalalignment="bottom",
    )

    axis_properties = AxisProperties(
        title="Bar",
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        data_label_style=PlotLabelStyle.Plain,
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(data=[[0.1, 5]], columns=["A", "B"], index=[None]),
        stacks_are_categories=True,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_bar_simple_portrait(test_figure, reference_figure):

    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.bar([0, 1, 2, 3, 4], [4, 5, 7, 9, 2], color="#0077BB", edgecolor="black")
    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=10)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(
        [
            "Ms. O          ",
            "Mr. U          ",
            "Mr. S          ",
            "Mr. P          ",
            "Ms. F          ",
        ],
        rotation=90,
    )
    reference_figure.canvas.draw()
    for label in ref_ax.xaxis.get_ticklabels():
        ext = label.get_window_extent()
        name = label.get_text().strip().lower()
        [[left, _], [right, top]] = reference_figure.transFigure.inverted().transform(
            ext
        )

        portrait_image = plt.imread(
            os.path.join(PORTRAITS_FOLDER, "{}.png".format(name))
        )
        port_size = 0.045
        port_start = ((left + right) / 2) - (port_size / 2)
        newax = reference_figure.add_axes(
            [port_start, top - port_size, port_size, port_size], zorder=-1
        )
        newax.imshow(portrait_image)
        newax.axis("off")

    axis_properties = AxisProperties(title="Bar", x_axis_portrait=True)
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[4, 5, 7, 9, 2]],
            columns=[
                Characters.Irish,
                Characters.Duke,
                Characters.Smallman,
                Characters.Carlos,
                Characters.Alice,
            ],
            index=[None],
        ),
        stacks_are_categories=True,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_bar_simple_float_short(test_figure, reference_figure):

    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    ref_ax.bar(
        [0, 1, 2, 3, 4],
        [0.2, 0.5, 0.7, 0.9, 0.2],
        color=["red", "blue", "black", "yellow", "white"],
        edgecolor="black",
    )
    ref_ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ref_ax.set_ylim(top=0.9)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)
    ref_ax.set_ylabel("ylabel")
    ref_ax.set_xlabel("xlabel")

    axis_properties = AxisProperties(
        title="Bar",
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        y_axis_label="ylabel",
        x_axis_label="xlabel",
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[[0.2, 0.5, 0.7, 0.9, 0.2]],
            columns=["A", "B", "C", "D", "E"],
            index=[None],
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

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    box = ref_ax.get_position()
    ref_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ref_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    axis_properties = AxisProperties(
        title="Bar",
        primary_color_dict={"Bottom": "red", "Top": "blue"},
        primary_hatch_dict={"Top": "\\", "Bottom": None},
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
def test_bar_stacked_percentile(test_figure, reference_figure):

    reference_figure.set_size_inches(15, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    patches = ref_ax.bar(
        [0, 1, 2, 3, 4],
        [1 / 5, 2 / 7, 3 / 10, 1 / 10, 6 / 8],
        color="blue",
        edgecolor="black",
        bottom=[4 / 5, 5 / 7, 7 / 10, 9 / 10, 2 / 8],
        label="Top",
    )
    ref_ax.bar(
        [0, 1, 2, 3, 4],
        [4 / 5, 5 / 7, 7 / 10, 9 / 10, 2 / 8],
        color="red",
        edgecolor="black",
        label="Bottom",
    )

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.yaxis.set_major_locator(MultipleLocator(0.1))
    vals = ref_ax.get_yticks()
    ref_ax.set_yticklabels(["{:,.0%}".format(x) for x in vals])
    ref_ax.set_ylim(top=1)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    box = ref_ax.get_position()
    ref_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ref_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    ref_ax.text(
        0,
        1 - 0.01,
        "20.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        1,
        1 - 0.01,
        "28.6",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        2,
        1 - 0.01,
        "30.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        3,
        1 - 0.01,
        "10.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        4,
        1 - 0.01,
        "75.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )
    # [4 / 5, 5 / 7, 7 / 10, 9 / 10, 2 / 8]
    ref_ax.text(
        0,
        (4 / 5) - 0.01,
        "80.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        1,
        (5 / 7) - 0.01,
        "71.4",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        2,
        (7 / 10) - 0.01,
        "70.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        3,
        (9 / 10) - 0.01,
        "90.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    ref_ax.text(
        4,
        (2 / 8) - 0.01,
        "25.0",
        color="black",
        horizontalalignment="center",
        verticalalignment="top",
    )

    axis_properties = AxisProperties(
        title="Bar",
        primary_color_dict={"Bottom": "red", "Top": "blue"},
        y_axis_percentage=True,
        data_label_style=PlotLabelStyle.Plain,
    )
    data_plot_properties = DataPlotProperties(
        frame=pandas.DataFrame(
            data=[
                [1 / 5, 2 / 7, 3 / 10, 1 / 10, 6 / 8],
                [4 / 5, 5 / 7, 7 / 10, 9 / 10, 2 / 8],
            ],
            columns=["A", "B", "C", "D", "E"],
            index=["Top", "Bottom"],
        ),
        stacks_are_categories=False,
    )

    create_bar_plot(axis_properties, data_plot_properties, fig=test_figure)


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_bar_stacked_no_color(test_figure, reference_figure):

    reference_figure.set_size_inches(15, 8)
    ref_ax = reference_figure.subplots()
    ref_ax.set_title("Bar")
    patches = ref_ax.bar(
        [0, 1, 2, 3, 4],
        [1, 2, 3, 1, 6],
        edgecolor="black",
        bottom=[4, 5, 7, 9, 2],
        label="Top",
        facecolor="#0077BB",
    )
    ref_ax.bar(
        [0, 1, 2, 3, 4],
        [4, 5, 7, 9, 2],
        edgecolor="black",
        label="Bottom",
        facecolor="#CC3311",
    )

    for p in patches:
        p.set_hatch("\\")

    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=11)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    box = ref_ax.get_position()
    ref_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ref_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    axis_properties = AxisProperties(
        title="Bar", primary_hatch_dict={"Top": "\\", "Bottom": None}
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
        label="TOPTOP",
    )
    ref_ax.plot(
        [0, 1, 2, 3, 4],
        [4, 5, 7, 9, 2],
        color="red",
        linestyle="-",
        marker="o",
        markersize=12,
        linewidth=4,
        label="BOTTOMBOTTOM",
    )

    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(top=10)

    ref_ax.set_xlim(-0.5, 4.5)
    ref_ax.set_xticks([0, 1, 2, 3, 4])

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")
    ref_ax.yaxis.grid(which="minor", linestyle="--")
    ref_ax.set_axisbelow(True)

    ref_ax.set_xticklabels(["A", "B", "C", "D", "E"], rotation=90)

    box = ref_ax.get_position()
    ref_ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ref_ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    axis_properties = AxisProperties(
        title="Bar",
        primary_color_dict={"Bottom": "red", "Top": "blue"},
        primary_label_dict={"Top": "TOPTOP", "Bottom": "BOTTOMBOTTOM"},
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
    ref_ax.bar(range(8), [4, 7, 7, 7, 8, 7, 8, 8], color="#0077BB", edgecolor="black")

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

    ref_ax.yaxis.grid(which="major")
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

    ref_ax.yaxis.grid(which="major")
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
        primary_color_dict={
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


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_histogram(test_figure, reference_figure):
    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()

    ref_ax.set_title("Histogram")
    ref_ax.bar(
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 6, 4, 3, 1, 0, 0, 0, 3],
        color="xkcd:green",
        edgecolor="black",
        width=1,
        align="edge",
    )

    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(0, 7)

    ref_ax.set_xlim(0, 9)

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")

    ref_ax.set_axisbelow(True)

    ref_ax.xaxis.set_major_locator(MultipleLocator(5))
    ref_ax.xaxis.set_minor_locator(MultipleLocator(1))

    axis_properties = AxisProperties(
        title="Histogram",
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
    )

    create_histogram(
        axis_properties,
        [1, 1, 1, 1, 2, 2, 3, 4, 3, 3, 2, 2, 1, 1, 8, 8, 8],
        fig=test_figure,
        bin_size=1,
        major_locator=5,
    )


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_histogram(test_figure, reference_figure):
    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()

    ref_ax.set_title("Histogram")
    ref_ax.bar(
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 6, 4, 3, 1, 0, 0, 0, 3],
        color="#0077BB",
        edgecolor="black",
        width=1,
        align="edge",
    )

    ref_ax.yaxis.set_major_locator(MultipleLocator(1))
    ref_ax.set_ylim(0, 7)

    ref_ax.set_xlim(0, 9)

    ref_ax.set_ylim(bottom=0)

    ref_ax.yaxis.grid(which="major")

    ref_ax.set_axisbelow(True)

    ref_ax.xaxis.set_major_locator(MultipleLocator(5))
    ref_ax.xaxis.set_minor_locator(MultipleLocator(1))

    axis2 = ref_ax.twinx()
    axis2.hist(
        [1, 1, 1, 1, 2, 2, 3, 4, 3, 3, 2, 2, 1, 1, 8, 8, 8],
        bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        density=True,
        histtype="step",
        cumulative=True,
        color="#CC3311",
        linewidth=3,
    )

    axis2.set_ylim(0, 1)

    axis_properties = AxisProperties(
        title="Histogram",
        primary_color_dict={
            "A": "red",
            "B": "blue",
            "C": "black",
            "D": "yellow",
            "E": "white",
        },
        cumulative_histogram=True,
    )

    create_histogram(
        axis_properties,
        [1, 1, 1, 1, 2, 2, 3, 4, 3, 3, 2, 2, 1, 1, 8, 8, 8],
        fig=test_figure,
        bin_size=1,
        major_locator=5,
    )


@pytest.mark.plotting
@pytest.mark.matplotlib
@check_figures_equal(extensions=["png"])
def test_create_progress_plot(test_figure, reference_figure):
    reference_figure.set_size_inches(12, 8)
    ref_ax = reference_figure.subplots()

    ref_ax.plot(
        [0, 0.25, 0.65, 1], [0, 0.25, 0.65, 1], linewidth=4, alpha=0.05, color="red"
    )
    ref_ax.plot([0, 0.25, 0.65], [0, 0.45, 0.6], linewidth=4, alpha=0.05, color="blue")
    ref_ax.plot(
        [0, 0.15, 0.75, 1], [0, 0.75, 0.85, 1], linewidth=4, alpha=0.05, color="green"
    )

    ref_ax.set_ylim(bottom=0)
    ref_ax.set_xlim(left=0)

    ref_ax.set_yticklabels(["{:,.0%}".format(x) for x in ref_ax.get_yticks()])
    ref_ax.set_xticklabels(["{:,.0%}".format(x) for x in ref_ax.get_xticks()])

    ref_ax.set_xlabel("xlabel")
    ref_ax.set_ylabel("ylabel")

    ref_ax.set_title("Progress")

    axis_properties = AxisProperties(
        title="Progress", x_axis_label="xlabel", y_axis_label="ylabel"
    )

    create_progress_plot(
        [[0, 0.25, 0.65, 1], [0, 0.25, 0.65], [0, 0.15, 0.75, 1]],
        [[0, 0.25, 0.65, 1], [0, 0.45, 0.6], [0, 0.75, 0.85, 1]],
        ["red", "blue", "green"],
        axis_properties=axis_properties,
        fig=test_figure,
    )
