from typing import List

from triple_agent.reports.generation.generic_query import query
from triple_agent.reports.generation.report_utilities import create_histogram
from triple_agent.classes.game import Game
from triple_agent.classes.timeline import TimelineCategory

_FAKE = "fake"
_REAL = "real"
FAKE_REAL_COLORS = {_FAKE: "xkcd:grey", _REAL: "xkcd:yellowish"}
FAKE_REAL_ORDER = [_FAKE, _REAL]


def _all_banana_breads(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if (
                timeline_event.category & TimelineCategory.BananaBread
                and timeline_event.event.endswith("started.")
            ):
                if timeline_event.event.startswith(_FAKE):
                    data_dictionary[_FAKE] += 1
                else:
                    data_dictionary[_REAL] += 1


def _first_banana_bread(games, data_dictionary):
    for game in games:
        first_seen = False
        for timeline_event in game.timeline:
            if (
                timeline_event.category & TimelineCategory.BananaBread
                and timeline_event.event.endswith("started.")
            ):
                if timeline_event.event.startswith(_FAKE):
                    if not first_seen:
                        data_dictionary[_FAKE] += 1

                else:
                    if not first_seen:
                        data_dictionary[_REAL] += 1

                first_seen = True


def all_banana_bread_percentages(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": FAKE_REAL_ORDER,
        "data_color_dict": FAKE_REAL_COLORS,
    }

    default_kwargs.update(kwargs)

    query(games, title, _all_banana_breads, **default_kwargs)


def first_banana_bread_percentages(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": FAKE_REAL_ORDER,
        "data_color_dict": FAKE_REAL_COLORS,
    }

    default_kwargs.update(kwargs)

    query(games, title, _first_banana_bread, **default_kwargs)


def banana_split(games: List[Game], title: str):
    """
    This function plots the time it takes for the spy to leave the CC after the most recent BB.
    """
    bb_times = []

    for game in games:
        bb_uttered = False
        bb_time_elapsed = 0

        for timeline_event in game.timeline:
            if (
                timeline_event.category & TimelineCategory.BananaBread
                and timeline_event.event.endswith("uttered.")
            ):
                bb_uttered = True
                bb_time_elapsed = timeline_event.elapsed_time

            if (
                bb_uttered
                and timeline_event.category & TimelineCategory.Conversation
                and timeline_event.event.startswith("spy le")
            ):
                bb_uttered = False
                bb_times.append(timeline_event.elapsed_time - bb_time_elapsed)
                bb_time_elapsed = 0

    create_histogram(
        title,
        bb_times,
        1,
        major_locator=10,
        x_label="Time Elapsed Since BB [sec]",
        y_label="Number of Leaves in Window",
        cumulative_also=True,
    )
