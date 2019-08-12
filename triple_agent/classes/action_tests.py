from enum import IntEnum, auto


class ActionTest(IntEnum):
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

AT_PREFERRED_PIE_CHART_ORDER = [
    ActionTest.Green,
    ActionTest.White,
    ActionTest.Ignored,
    ActionTest.Red,
    ActionTest.Canceled,
]
