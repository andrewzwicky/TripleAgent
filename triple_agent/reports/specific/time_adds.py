from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.reports.generation.report_utilities import create_histogram
from triple_agent.classes.game import Game
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    create_properties_if_none,
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
    create_properties_if_none(axis_properties, data_query)

    data_query.query_function = _count_time_adds

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
        title + " [Elapsed]",
        time_adds_elapsed,
        10,
        x_label="Time Elapsed [sec]",
        y_label="Time Adds in Time Period",
    )

    create_histogram(
        title + " [Remaining]",
        time_adds_remaining,
        10,
        x_label="Time Remaining [sec]",
        y_label="Time Adds in Time Period",
    )
