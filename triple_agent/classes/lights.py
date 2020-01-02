from enum import auto
from triple_agent.classes.ordered_enum import OrderedEnum


class Lights(OrderedEnum):
    Lowlight = 0
    Neutral = auto()
    Highlight = auto()


LIGHTS_TO_COLORS = {
    Lights.Lowlight: "xkcd:dark gray",
    Lights.Neutral: "xkcd:gray",
    Lights.Highlight: "xkcd:white",
}

LIGHT_PREFERRED_PIE_CHART_ORDER = [
    Lights.Lowlight,
    Lights.Neutral,
    Lights.Highlight,
]
