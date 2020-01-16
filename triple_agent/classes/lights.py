from enum import auto
from triple_agent.classes.ordered_enum import ReverseOrderedEnum
from triple_agent.constants.colors import PlotColors


class Lights(ReverseOrderedEnum):
    Lowlight = 0
    Neutral = auto()
    Highlight = auto()


LIGHTS_TO_COLORS = {
    Lights.Lowlight: PlotColors.DarkGrey,
    Lights.Neutral: PlotColors.Grey,
    Lights.Highlight: PlotColors.White,
}

LIGHTS_TO_COLORS_DARK_MODE = {
    Lights.Lowlight: "#8DB8AD",
    Lights.Neutral: "#EBE7E0",
    Lights.Highlight: "#C6D4E1",
}
