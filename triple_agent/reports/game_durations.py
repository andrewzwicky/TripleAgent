from typing import List

from triple_agent.reports.report_utilities import create_histogram
from triple_agent.utilities.game import Game


def game_durations(games: List[Game], title: str):
    create_histogram(
        title,
        [game.timeline[-1].elapsed_time for game in games],
        5,
        major_locator=30,
        x_label="Game Duration [sec]",
        y_label="Game Ends in Time Period",
        cumulative_also=True,
    )

    create_histogram(
        title,
        [
            (game.timeline[-1].elapsed_time / game.start_clock_seconds) * 100
            for game in games
        ],
        2,
        major_locator=10,
        x_label="Game Duration [%]",
        y_label="Game Ends in Time Period",
        cumulative_also=True,
    )
