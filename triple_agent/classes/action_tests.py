from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum
from triple_agent.constants.colors import PlotColors


class ActionTest(ReverseOrderedEnum):
    NoAT = 0
    Green = auto()
    White = auto()
    Ignored = auto()
    Red = auto()
    Canceled = auto()


AT_TO_COLORS_RGB = {
    ActionTest.Green: PlotColors.Color3,
    ActionTest.White: PlotColors.White,
    ActionTest.Ignored: PlotColors.LightGrey,
    ActionTest.Red: PlotColors.Color2,
    ActionTest.Canceled: PlotColors.DarkGrey,
}


AT_TO_COLORS_DARK_MODE = {
    ActionTest.Green: "#44749D",
    ActionTest.White: "EBE7E0",
    ActionTest.Ignored: "xkcd:light grey",
    ActionTest.Red: "xkcd:light pink",
    ActionTest.Canceled: "xkcd:dark grey",
}
