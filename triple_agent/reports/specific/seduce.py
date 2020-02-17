from typing import List

from triple_agent.reports.generation.plot_types import create_histogram
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.plot_specs import AxisProperties


def first_flirt_timing(games: List[Game], title: str):  # pragma: no cover
    """
    This function plots the first attempt at flirting.
    """
    first_flirt_times = calc_first_flirt_times(games)

    create_histogram(
        AxisProperties(
            title=title,
            x_axis_label="Elapsed Time at First Flirt [sec]",
            y_axis_label="Number of Flirts in Time Period",
            cumulative_histogram=True,
        ),
        first_flirt_times,
        2,
        major_locator=30,
    )


def _calc_first_flirt_times(games):
    first_flirt_times = []
    for game in games:
        prev_len = len(first_flirt_times)
        for timeline_event in game.timeline:
            if (
                timeline_event.category & TimelineCategory.ActionTest
                and timeline_event.mission & Missions.Seduce
            ):
                first_flirt_times.append(timeline_event.elapsed_time)
                break

        if len(first_flirt_times) == prev_len:
            first_flirt_times.append(game.timeline[-1].elapsed_time)
    return first_flirt_times
