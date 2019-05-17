from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.reports.report_utilities import create_histogram
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import Missions
from triple_agent.utilities.timeline import TimelineCategory

BUG_TO_COLORS_RGB = {"Walking": "xkcd:sea blue", "Standing": "xkcd:pumpkin"}

BUG_PLOT_LABEL_DICT = {
    ("Walking", True): "Walking (Successful)",
    ("Walking", False): "Walking (Miss)",
    ("Standing", True): "Standing (Successful)",
    ("Standing", False): "Standing (Miss)",
}

BUG_PLOT_ORDER = list(BUG_PLOT_LABEL_DICT.keys())

BUG_PLOT_HATCHING = [
    r"\\" if not success else None for bug_type, success in BUG_PLOT_ORDER
]

BUG_PLOT_COLOR = [BUG_TO_COLORS_RGB[bug_type] for bug_type, success in BUG_PLOT_ORDER]


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
        title + " [Remaining]",
        bug_times_elapsed,
        10,
        x_label="Time Remaining [sec]",
        y_label="Attempts in Time Period",
    )
    create_histogram(
        title + " [Elapsed]",
        bug_times_remaining,
        10,
        x_label="Time Elapsed [sec]",
        y_label="Attempts in Time Period",
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


def bug_success_rate(games: List[Game], title: str, **kwargs):
    query(
        games,
        title,
        _categorize_bugs,
        BUG_PLOT_ORDER,
        BUG_PLOT_COLOR,
        data_hatching=BUG_PLOT_HATCHING,
        data_item_label_dict=BUG_PLOT_LABEL_DICT,
        **kwargs,
    )
