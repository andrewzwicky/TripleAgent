from typing import List

from triple_agent.reports.report_utilities import create_histogram
from triple_agent.classes.game import Game
from triple_agent.classes.missions import Missions
from triple_agent.classes.timeline import TimelineCategory


def first_flirt_timing(games: List[Game], title: str):
    """
    This function plots the first attempt at flirting.
    """
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

    create_histogram(
        title,
        first_flirt_times,
        2,
        major_locator=30,
        x_label="Elapsed Time at First Flirt [sec]",
        y_label="Number of Flirts in Time Period",
        cumulative_also=True,
    )
