from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum
from triple_agent.constants.colors import PlotColorsBase


class ActionTest(ReverseOrderedEnum):
    NoAT = 0
    Green = auto()
    White = auto()
    Ignored = auto()
    Red = auto()
    Canceled = auto()


def create_action_test_color_dict(plot_colors: PlotColorsBase):
    return {
        ActionTest.Green: plot_colors.color_3,
        ActionTest.White: plot_colors.white,
        ActionTest.Ignored: plot_colors.light_grey,
        ActionTest.Red: plot_colors.color_2,
        ActionTest.Canceled: plot_colors.dark_grey,
    }
