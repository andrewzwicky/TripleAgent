from enum import IntEnum, auto


class ActionTest(IntEnum):
    NoAT = 0
    Green = auto()
    White = auto()
    Ignored = auto()
    Red = auto()
    Canceled = auto()


def assign_color(event_text):
    if "green" in event_text:
        return ActionTest.Green

    if "white" in event_text:
        return ActionTest.White

    if "ignored" in event_text:
        return ActionTest.Ignored

    if "canceled" in event_text:
        return ActionTest.Canceled

    if "red" in event_text:
        return ActionTest.Red

    return ActionTest.NoAT


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

AT_PREFERRED_PIE_CHART_COLOR = [
    AT_TO_COLORS_RGB[at] for at in AT_PREFERRED_PIE_CHART_ORDER
]
