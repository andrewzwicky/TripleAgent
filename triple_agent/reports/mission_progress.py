from typing import List

from matplotlib import pyplot as plt

from triple_agent.utilities.game import Game
from triple_agent.utilities.outcomes import WINTYPES_TO_COLORS
from triple_agent.utilities.timeline import TimelineCategory


def mission_progress(games: List[Game], title: str):
    times = []
    progresses = []
    colors = []

    for game in games:
        # todo: get all games with start clock seconds
        if game.start_clock_seconds is not None:
            game_times = [0]
            game_progress = [0]
            game_mission_count = 0
            req_missions = int(game.game_type[1])
            for event in game.timeline:
                if event.category & TimelineCategory.MissionComplete:
                    # todo: include partial missions (inspects / fingerprint)
                    game_times.append(event.elapsed_time / game.start_clock_seconds)
                    game_mission_count += 1
                    game_progress.append(game_mission_count / req_missions)
            times.append(game_times)
            progresses.append(game_progress)
            colors.append(WINTYPES_TO_COLORS[game.win_type])

    fig, axis = plt.subplots(figsize=(14, 10))

    alpha = 0.05

    for t, p, c in zip(times, progresses, colors):
        axis.plot(t, p, linewidth=4, alpha=alpha, color=c)
        # axis.scatter(t[-1], p[-1], alpha=alpha, marker="o", color="k")

    axis.set_ylim(bottom=0)
    axis.set_xlim(left=0)

    axis.set_xlabel("Percent of Start Time Elapsed")
    axis.set_ylabel("Mission Progress")

    axis.set_yticklabels(["{:,.0%}".format(x) for x in axis.get_yticks()])
    axis.set_xticklabels(["{:,.0%}".format(x) for x in axis.get_xticks()])

    axis.set_title(title)

    plt.show()
