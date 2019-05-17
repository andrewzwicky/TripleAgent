from triple_agent.utilities.timeline import TimelineCategory

OBJECT_TO_COLORS_RGB = {
    TimelineCategory.Briefcase: "xkcd:beige",
    TimelineCategory.Statues: "xkcd:goldenrod",
    TimelineCategory.Books: "xkcd:cerulean",
    TimelineCategory.Drinks: "xkcd:light grey",
}

OBJECT_PLOT_ORDER = [
    TimelineCategory.Briefcase,
    TimelineCategory.Statues,
    TimelineCategory.Books,
    TimelineCategory.Drinks,
]

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

OBJECT_PLOT_COLOR_DIFFICULT = [
    OBJECT_TO_COLORS_RGB[obj] for obj, diff in OBJECT_PLOT_ORDER_DIFFICULT
]

OBJECT_PLOT_HATCHING_DIFFICULT = [
    r"\\" if diff else None for obj, diff in OBJECT_PLOT_ORDER_DIFFICULT
]

OBJECT_PLOT_COLOR = [OBJECT_TO_COLORS_RGB[obj] for obj in OBJECT_PLOT_ORDER]
