from typing import List

from triple_agent.reports.generation.plot_types import create_histogram
from triple_agent.classes.game import Game
from triple_agent.reports.generation.plot_specs import AxisProperties


def game_durations(games: List[Game], title: str):
    create_histogram(
        AxisProperties(
            title=title,
            x_axis_label="Game Duration [sec]",
            y_axis_label="Game Ends in Time Period",
        ),
        [game.timeline[-1].elapsed_time for game in games],
        5,
        major_locator=30,
        cumulative_also=True,
    )

    create_histogram(
        AxisProperties(
            title=title,
            x_axis_label="Game Duration [%]",
            y_axis_label="Game Ends in Time Period",
        ),
        [
            (game.timeline[-1].elapsed_time / game.start_clock_seconds) * 100
            for game in games
        ],
        2,
        major_locator=10,
        cumulative_also=True,
    )
