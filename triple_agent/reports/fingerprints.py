from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.objects import (
    OBJECT_PLOT_ORDER_DIFFICULT,
    OBJECT_TO_COLORS_RGB,
    OBJECT_PLOT_HATCHING_DIFFICULT,
    OBJECT_PLOT_LABEL_DICT_DIFFICULT,
)
from triple_agent.utilities.timeline import TimelineCategory


def __iterate_and_count_potential_prints(game, timeline_event, data_dictionary):
    current_event = timeline_event
    while True:
        following = game.timeline.get_next_spy_action(current_event)
        if following is None:
            break

        if following.category & TimelineCategory.ActionTest:
            difficult = True
        elif following.category & TimelineCategory.MissionPartial:
            difficult = False
        else:
            current_event = following
            continue

        if timeline_event.category & TimelineCategory.Books:
            data_dictionary[(TimelineCategory.Books, difficult)] += 1
        if timeline_event.category & TimelineCategory.Statues:
            data_dictionary[(TimelineCategory.Statues, difficult)] += 1
        if timeline_event.category & TimelineCategory.Drinks:
            data_dictionary[(TimelineCategory.Drinks, difficult)] += 1
        if timeline_event.category & TimelineCategory.Briefcase:
            data_dictionary[(TimelineCategory.Briefcase, difficult)] += 1

        break


def _categorize_fp_sources(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.event.startswith("started fingerprinting"):
                __iterate_and_count_potential_prints(
                    game, timeline_event, data_dictionary
                )


def attempted_fingerprint_sources(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": OBJECT_PLOT_ORDER_DIFFICULT,
        "data_color_dict": OBJECT_TO_COLORS_RGB,
        "data_hatching": OBJECT_PLOT_HATCHING_DIFFICULT,
        "data_stack_label_dict": OBJECT_PLOT_LABEL_DICT_DIFFICULT,
    }

    default_kwargs.update(kwargs)

    query(games, title, _categorize_fp_sources, **default_kwargs)
