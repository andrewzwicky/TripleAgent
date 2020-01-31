from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum
from triple_agent.constants.colors import PLOT_COLORS


class ActionTest(ReverseOrderedEnum):
    NoAT = 0
    Green = auto()
    White = auto()
    Ignored = auto()
    Red = auto()
    Canceled = auto()


AT_TO_COLORS_RGB = {
    ActionTest.Green: PLOT_COLORS.color_3,
    ActionTest.White: PLOT_COLORS.white,
    ActionTest.Ignored: PLOT_COLORS.light_grey,
    ActionTest.Red: PLOT_COLORS.color_2,
    ActionTest.Canceled: PLOT_COLORS.dark_grey,
}
