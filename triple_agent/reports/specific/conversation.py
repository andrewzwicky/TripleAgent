from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)
from triple_agent.classes.timeline import TimelineCategory


def _count_time_in_conversation(games, data_dictionary):
    for game in games:
        spy_in_convo = False
        in_convo_time = 0
        out_of_convo_time = 0
        last_event_time = 0

        for timeline_event in game.timeline:
            if timeline_event.event == "spy enters conversation.":
                out_of_convo_time += timeline_event.elapsed_time - last_event_time
                last_event_time = timeline_event.elapsed_time
                spy_in_convo = True

            if timeline_event.event == "spy leaves conversation.":
                in_convo_time += timeline_event.elapsed_time - last_event_time
                last_event_time = timeline_event.elapsed_time
                spy_in_convo = False

            if timeline_event.category & TimelineCategory.GameEnd:
                # use last event to tally up the remaining time
                if spy_in_convo:
                    in_convo_time += timeline_event.elapsed_time - last_event_time
                else:
                    out_of_convo_time += timeline_event.elapsed_time - last_event_time

        data_dictionary[True] += in_convo_time
        data_dictionary[False] += out_of_convo_time


def cumulative_conversation_times(
    games: List[Game],
    data_query: DataQueryProperties = DataQueryProperties(),
    axis_properties: AxisProperties = AxisProperties(),
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(primary_label_dict={False: "Out Of Convo", True: "In Convo"}),
        DataQueryProperties(
            query_function=_count_time_in_conversation,
        ),
    )
    return query(games, data_query, axis_properties)
