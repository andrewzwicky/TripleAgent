from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.classes.objects import (
    OBJECT_PLOT_ORDER_DIFFICULT,
    OBJECT_TO_COLORS_RGB,
    OBJECT_PLOT_HATCH_DICT,
    OBJECT_PLOT_LABEL_DICT_DIFFICULT,
)
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)


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


def attempted_fingerprint_sources(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=OBJECT_TO_COLORS_RGB,
            primary_label_dict=OBJECT_PLOT_LABEL_DICT_DIFFICULT,
            primary_hatch_dict=OBJECT_PLOT_HATCH_DICT,
        ),
        DataQueryProperties(
            query_function=_categorize_fp_sources,
            primary_order=OBJECT_PLOT_ORDER_DIFFICULT,
        ),
    )

    return query(games, data_query, axis_properties)
