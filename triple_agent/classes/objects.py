from triple_agent.classes.timeline import TimelineCategory
from triple_agent.constants.colors import PlotColorsBase


# TODO: create an actual first class Object enum, separate from TimelineCategory?
def create_objects_color_dict(plot_colors: PlotColorsBase):
    return {
        (TimelineCategory.Briefcase, True): plot_colors.color_1,
        (TimelineCategory.Briefcase, False): plot_colors.color_1,
        (TimelineCategory.Statues, True): plot_colors.color_2,
        (TimelineCategory.Statues, False): plot_colors.color_2,
        (TimelineCategory.Books, True): plot_colors.color_3,
        (TimelineCategory.Books, False): plot_colors.color_3,
        (TimelineCategory.Drinks, True): plot_colors.color_4,
        (TimelineCategory.Drinks, False): plot_colors.color_4,
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
