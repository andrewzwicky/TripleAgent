from typing import List

from triple_agent.classes.game import Game
from triple_agent.classes.outcomes import WINTYPES_TO_COLORS
from triple_agent.classes.timeline import TimelineCategory
from triple_agent.reports.generation.report_utilities import create_progress_plot
from triple_agent.reports.generation.plot_specs import AxisProperties


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

    create_progress_plot(
        times,
        progresses,
        colors,
        AxisProperties(
            title=title,
            x_axis_label="Percent of Start Time Elapsed",
            y_axis_label="Mission Progress",
        ),
    )
