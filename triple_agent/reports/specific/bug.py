from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.reports.generation.plot_types import create_histogram
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import (
    AxisProperties,
    DataQueryProperties,
    initialize_properties,
)
from triple_agent.constants.colors import PLOT_COLORS

BUG_TO_COLORS_RGB = {
    ("Walking", True): PLOT_COLORS.color_1,
    ("Walking", False): PLOT_COLORS.color_1,
    ("Standing", True): PLOT_COLORS.color_2,
    ("Standing", False): PLOT_COLORS.color_2,
}

BUG_PLOT_LABEL_DICT = {
    ("Walking", True): "Walking (Successful)",
    ("Walking", False): "Walking (Miss)",
    ("Standing", True): "Standing (Successful)",
    ("Standing", False): "Standing (Miss)",
}

BUG_PLOT_ORDER = list(BUG_PLOT_LABEL_DICT.keys())

BUG_PLOT_HATCH_DICT = {
    (obj, diff): r"\\" if not diff else None for (obj, diff) in BUG_PLOT_ORDER
}


def bug_attempt_timings(games: List[Game], title: str):
    bug_times_elapsed = []
    bug_times_remaining = []

    for game in games:
        for timeline_event in game.timeline:
            if (
                timeline_event.category == TimelineCategory.ActionTriggered
                and timeline_event.mission == Missions.Bug
            ):
                bug_times_elapsed.append(timeline_event.elapsed_time)
                bug_times_remaining.append(timeline_event.time)

    create_histogram(
        AxisProperties(
            title=title + " [Remaining]",
            x_axis_label="Time Remaining [sec]",
            y_axis_label="Attempts in Time Period",
        ),
        bug_times_elapsed,
        15,
    )
    create_histogram(
        AxisProperties(
            title=title + " [Elapsed]",
            x_axis_label="Time Elapsed [sec]",
            y_axis_label="Attempts in Time Period",
        ),
        bug_times_remaining,
        15,
    )


def _categorize_bugs(games, data_dictionary):
    for game in games:
        walking_success = 0
        walking_attempts = 0
        standing_success = 0
        standing_attempts = 0

        for timeline_event in game.timeline:
            if timeline_event.mission == Missions.Bug:
                if timeline_event.category & TimelineCategory.MissionComplete:
                    if "standing" in timeline_event.event:
                        standing_success += 1
                    elif "walking" in timeline_event.event:
                        walking_success += 1

                if "bug transitioned from standing to walking." in timeline_event.event:
                    standing_attempts -= 1
                    walking_attempts += 1

                if timeline_event.event.startswith("begin planting bug"):
                    if "standing" in timeline_event.event:
                        standing_attempts += 1
                    elif "walking" in timeline_event.event:
                        walking_attempts += 1

        data_dictionary[("Walking", True)] += walking_success
        data_dictionary[("Walking", False)] += walking_attempts - walking_success
        data_dictionary[("Standing", True)] += standing_success
        data_dictionary[("Standing", False)] += standing_attempts - standing_success


def bug_success_rate(
    games: List[Game],
    data_query: DataQueryProperties = None,
    axis_properties: AxisProperties = None,
):  # pragma: no cover
    axis_properties, data_query = initialize_properties(
        axis_properties,
        data_query,
        AxisProperties(
            primary_color_dict=BUG_TO_COLORS_RGB,
            primary_label_dict=BUG_PLOT_LABEL_DICT,
            primary_hatch_dict=BUG_PLOT_HATCH_DICT,
        ),
        DataQueryProperties(
            query_function=_categorize_bugs, primary_order=BUG_PLOT_ORDER
        ),
    )

    return query(games, data_query, axis_properties)
