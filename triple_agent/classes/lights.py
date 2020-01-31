from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum
from triple_agent.constants.colors import PLOT_COLORS


class Lights(ReverseOrderedEnum):
    Lowlight = 0
    Neutral = auto()
    Highlight = auto()


LIGHTS_TO_COLORS = {
    Lights.Lowlight: PLOT_COLORS.dark_grey,
    Lights.Neutral: PLOT_COLORS.grey,
    Lights.Highlight: PLOT_COLORS.white,
}
