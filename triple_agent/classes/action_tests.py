from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum


class ActionTest(ReverseOrderedEnum):
    NoAT = 0
    Green = auto()
    White = auto()
    Ignored = auto()
    Red = auto()
    Canceled = auto()


AT_TO_COLORS_RGB = {
    ActionTest.Green: "xkcd:green",
    ActionTest.White: "xkcd:white",
    ActionTest.Ignored: "xkcd:off white",
    ActionTest.Red: "xkcd:red",
    ActionTest.Canceled: "xkcd:light grey",
}


AT_TO_COLORS_DARK_MODE = {
    ActionTest.Green: "#44749D",
    ActionTest.White: "EBE7E0",
    ActionTest.Ignored: "xkcd:light grey",
    ActionTest.Red: "xkcd:light pink",
    ActionTest.Canceled: "xkcd:dark grey",
}
