from triple_agent.classes.timeline import TimelineCategory
from triple_agent.constants.colors import PlotColors


# TODO: create an actual first class Object enum, separate from TimelineCategory?
OBJECT_TO_COLORS_RGB = {
    (TimelineCategory.Briefcase, True): PlotColors.Color1,
    (TimelineCategory.Briefcase, False): PlotColors.Color1,
    (TimelineCategory.Statues, True): PlotColors.Color2,
    (TimelineCategory.Statues, False): PlotColors.Color2,
    (TimelineCategory.Books, True): PlotColors.Color3,
    (TimelineCategory.Books, False): PlotColors.Color3,
    (TimelineCategory.Drinks, True): PlotColors.Color4,
    (TimelineCategory.Drinks, False): PlotColors.Color4,
}

OBJECT_PLOT_LABEL_DICT_DIFFICULT = {
    (TimelineCategory.Briefcase, True): "Briefcase (Difficult)",
    (TimelineCategory.Briefcase, False): "Briefcase",
    (TimelineCategory.Statues, True): "Statue (Difficult)",
    (TimelineCategory.Statues, False): "Statue",
    (TimelineCategory.Books, True): "Book (Difficult)",
    (TimelineCategory.Books, False): "Book",
    (TimelineCategory.Drinks, True): "Drink (Difficult)",
    (TimelineCategory.Drinks, False): "Drink",
}

OBJECT_PLOT_ORDER_DIFFICULT = list(OBJECT_PLOT_LABEL_DICT_DIFFICULT.keys())

OBJECT_PLOT_HATCH_DICT = {
    (obj, diff): r"\\" if diff else None for (obj, diff) in OBJECT_PLOT_ORDER_DIFFICULT
}
