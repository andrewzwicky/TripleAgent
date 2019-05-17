from collections import Counter
from typing import List

from matplotlib import pyplot as plt
from scipy.stats import binom
import numpy as np
import math
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches

from triple_agent.reports.report_utilities import create_bar_plot
from triple_agent.utilities.characters import Characters
from triple_agent.utilities.game import Game
from triple_agent.utilities.roles import Roles
from triple_agent.utilities.timeline import TimelineCategory


def _low_end(x):
    return (1 - x) / 2


def _high_end(x):
    return 1 - ((1 - x) / 2)


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (
        idx == len(array)
        or math.fabs(value - array[idx - 1]) < math.fabs(value - array[idx])
    ):
        return idx - 1
    else:
        return idx


def _generic_role_selection(
    games: List[Game], title: str, role: Roles, color=None, statistics=True
):
    # TODO: stacked bar by event?
    roles = Counter({char: 0 for char in Characters})

    del roles[Characters.Damon]
    del roles[Characters.Toby]

    for game in games:
        for event in game.timeline:
            if (event.category & TimelineCategory.Cast) and (role in event.role):
                roles[event.cast_name[0]] += 1
                break

    spies, times_picked = zip(*sorted(list(roles.items()), key=lambda x: -x[1]))

    total_games = len(games)

    percent_picked = [t / total_games for t in times_picked]

    axis = create_bar_plot(
        title,
        [percent_picked],
        [spy.name + " " * 12 for spy in spies],
        bar_labels=[times_picked],
        y_label="% of Games Selected",
        colors=[color],
        label_rotation=90,
        percentage=True,
        portrait_x_axis=True,
        no_show=True,
    )

    if statistics:
        prob = 0.95
        n = len(games)
        k = np.arange(0, n)
        # noinspection PyTypeChecker
        p = 1 / (len(Characters) - 2)
        cdf = binom.cdf(k, n, p)
        bottom = k[find_nearest(cdf, _low_end(prob))] / n
        top = k[find_nearest(cdf, _high_end(prob))] / n

        # noinspection PyTypeChecker
        rect = mpatches.Rectangle(
            (-1, bottom), len(Characters) + 1, top - bottom, ec="none"
        )
        collection = PatchCollection([rect], alpha=0.2, color="k")
        axis.add_collection(collection)

    plt.show()


def spy_selection(games: List[Game], title: str, statistics=True):
    _generic_role_selection(games, title, Roles.Spy, "xkcd:green", statistics)


def st_selection(games: List[Game], title: str, statistics=True):
    _generic_role_selection(
        games, title, Roles.SeductionTarget, "xkcd:light red", statistics
    )


def amba_selection(games: List[Game], title: str, statistics=True):
    _generic_role_selection(
        games, title, Roles.Ambassador, "xkcd:light magenta", statistics
    )


def double_agent_selection(games: List[Game], title: str, statistics=True):
    _generic_role_selection(
        games, title, Roles.DoubleAgents, "xkcd:light yellow", statistics
    )
