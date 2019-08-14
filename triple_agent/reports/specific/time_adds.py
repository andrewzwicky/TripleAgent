from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.reports.generation.report_utilities import create_histogram
from triple_agent.classes.game import Game
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)


def _count_time_adds(games, data_dictionary):
    for game in games:
        this_game_time_adds = 0
        for timeline_event in game.timeline:
            if (
                timeline_event.category & TimelineCategory.ActionTest
                and timeline_event.category & TimelineCategory.TimeAdd
            ):
                this_game_time_adds += 1
        data_dictionary[this_game_time_adds] += 1


def time_add_times_per_game(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        DataQueryProperties(query_function=_count_time_adds),
    )

    query(games, data_query, axis_properties)


def time_add_times(games: List[Game], title: str):
    time_adds_elapsed = []
    time_adds_remaining = []

    for game in games:
        this_game_time_adds = 0
        for timeline_event in game.timeline:
            if (
                timeline_event.category & TimelineCategory.ActionTest
                and timeline_event.category & TimelineCategory.TimeAdd
            ):
                this_game_time_adds += 1
                time_adds_elapsed.append(timeline_event.elapsed_time)
                time_adds_remaining.append(timeline_event.time)

    create_histogram(
        AxisProperties(
            title=title + " [Elapsed]",
            x_axis_label="Time Elapsed [sec]",
            y_axis_label="Time Adds in Time Period",
        ),
        time_adds_elapsed,
        10,
    )

    create_histogram(
        AxisProperties(
            title=title + " [Remaining]",
            x_axis_label="Time Remaining [sec]",
            y_axis_label="Time Adds in Time Period",
        ),
        time_adds_remaining,
        10,
    )
