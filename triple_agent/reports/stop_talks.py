from typing import List

from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game

NOSTOP_TO_COLORS_RGB = {"NoStop": "xkcd:sea blue", "Stop": "xkcd:pumpkin"}

NOSTOP_PLOT_ORDER = list(NOSTOP_TO_COLORS_RGB.keys())


def _categorize_stop_talks(games, data_dictionary):
    for game in games:
        for timeline_event in game.timeline:
            if timeline_event.event == "stopped talking.":
                data_dictionary["Stop"] += 1
                continue

        data_dictionary["NoStop"] += 1


def stop_talk_in_game_percentage(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": NOSTOP_PLOT_ORDER,
        "data_color_dict": NOSTOP_TO_COLORS_RGB,
    }

    default_kwargs.update(kwargs)

    query(games, title, _categorize_stop_talks, **default_kwargs)
