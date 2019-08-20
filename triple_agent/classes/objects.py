from triple_agent.classes.timeline import TimelineCategory


OBJECT_TO_COLORS_RGB = {
    (TimelineCategory.Briefcase, True): "xkcd:beige",
    (TimelineCategory.Briefcase, False): "xkcd:beige",
    (TimelineCategory.Statues, True): "xkcd:goldenrod",
    (TimelineCategory.Statues, False): "xkcd:goldenrod",
    (TimelineCategory.Books, True): "xkcd:cerulean",
    (TimelineCategory.Books, False): "xkcd:cerulean",
    (TimelineCategory.Drinks, True): "xkcd:light grey",
    (TimelineCategory.Drinks, False): "xkcd:light grey",
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

OBJECT_PLOT_HATCH_DICT = {
    (obj, diff): r"\\" if diff else None for (obj, diff) in OBJECT_PLOT_ORDER_DIFFICULT
}
