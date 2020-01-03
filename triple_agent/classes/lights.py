from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum


class Lights(ReverseOrderedEnum):
    Lowlight = 0
    Neutral = auto()
    Highlight = auto()


LIGHTS_TO_COLORS = {
    Lights.Lowlight: "xkcd:dark gray",
    Lights.Neutral: "xkcd:gray",
    Lights.Highlight: "xkcd:white",
}
