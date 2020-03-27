from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum
from triple_agent.constants.colors import PlotColorsBase


class Lights(ReverseOrderedEnum):
    Lowlight = 0
    Neutral = auto()
    Highlight = auto()


def create_lights_color_dict(plot_colors: PlotColorsBase):
    return {
        Lights.Lowlight: plot_colors.dark_grey,
        Lights.Neutral: plot_colors.grey,
        Lights.Highlight: plot_colors.white,
    }
