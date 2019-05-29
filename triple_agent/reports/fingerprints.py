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


def _categorize_fp_sources(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.event.startswith("started fingerprinting"):
                current_event = timeline_event
                while True:
                    following = game.timeline.get_next_spy_action(current_event)
                    if following is None:
                        break

                    if following.category & TimelineCategory.ActionTest:
                        if timeline_event.category & TimelineCategory.Books:
                            data_dictionary[(TimelineCategory.Books, True)] += 1
                        if timeline_event.category & TimelineCategory.Statues:
                            data_dictionary[(TimelineCategory.Statues, True)] += 1
                        if timeline_event.category & TimelineCategory.Drinks:
                            data_dictionary[(TimelineCategory.Drinks, True)] += 1
                        if timeline_event.category & TimelineCategory.Briefcase:
                            data_dictionary[(TimelineCategory.Briefcase, True)] += 1
                    elif following.category & TimelineCategory.MissionPartial:
                        if timeline_event.category & TimelineCategory.Books:
                            data_dictionary[(TimelineCategory.Books, False)] += 1
                        if timeline_event.category & TimelineCategory.Statues:
                            data_dictionary[(TimelineCategory.Statues, False)] += 1
                        if timeline_event.category & TimelineCategory.Drinks:
                            data_dictionary[(TimelineCategory.Drinks, False)] += 1
                        if timeline_event.category & TimelineCategory.Briefcase:
                            data_dictionary[(TimelineCategory.Briefcase, False)] += 1
                    else:
                        current_event = following
                        continue

                    break


def attempted_fingerprint_sources(games: List[Game], title: str, **kwargs):
    query(
        games,
        title,
        _categorize_fp_sources,
        OBJECT_PLOT_ORDER_DIFFICULT,
        OBJECT_TO_COLORS_RGB,
        data_hatching=OBJECT_PLOT_HATCHING_DIFFICULT,
        data_item_label_dict=OBJECT_PLOT_LABEL_DICT_DIFFICULT,
        **kwargs,
    )
