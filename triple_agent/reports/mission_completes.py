from collections import defaultdict, Counter
from typing import List, Dict

from triple_agent.reports.report_utilities import create_bar_plot
from triple_agent.reports.generic_query import query
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import (
    MISSIONS_ENUM_TO_COLOR,
    MISSION_PLOT_ORDER,
    MISSION_LETTERS_TO_ENUM,
    Missions,
    print_complete_string,
)


def _mission_completes(games: List[Game], data_dictionary: Counter):
    for game in games:
        for mission in Missions:
            if mission & game.completed_missions:
                data_dictionary[mission] += 1


def mission_completion_query(games: List[Game], title: str, **kwargs):
    default_kwargs = {
        "data_stack_order": MISSION_PLOT_ORDER,
        "data_color_dict": MISSIONS_ENUM_TO_COLOR,
    }

    default_kwargs.update(kwargs)

    query(games, title, _mission_completes, **default_kwargs)


def mission_completion(
    games: List[Game], title: str, venue_mode_dict: Dict[str, str] = None
):
    overall_key = "Overall"
    times_enabled = defaultdict(Counter)
    times_performed = defaultdict(Counter)
    games_count_by_venue = Counter()

    for game in games:
        if venue_mode_dict is None or (
            game.venue in venue_mode_dict.keys()
            and game.game_type == venue_mode_dict[game.venue]
        ):

            games_count_by_venue[game.venue] += 1
            games_count_by_venue[overall_key] += 1

            times_enabled[game.venue] += Counter(
                print_complete_string(game.picked_missions).replace(" ", "")
            )
            times_enabled[overall_key] += Counter(
                print_complete_string(game.picked_missions).replace(" ", "")
            )

            times_performed[game.venue] += Counter(
                print_complete_string(game.completed_missions).replace(" ", "")
            )
            times_performed[overall_key] += Counter(
                print_complete_string(game.completed_missions).replace(" ", "")
            )

    for venue, total_games in sorted(
        games_count_by_venue.items(), key=lambda x: (x[0] != overall_key, x[0])
    ):

        percs = []
        uncompleted = []
        percs_labels = []
        uncompleted_labels = []

        for letter, _ in MISSION_LETTERS_TO_ENUM.items():
            perf = times_performed[venue][letter]
            avail = times_enabled[venue][letter]
            perc_avail = 0 if total_games == 0 else (avail / total_games)
            perc_complete_bar = 0 if avail == 0 else (perf / total_games)
            perc_complete_label = 0 if avail == 0 else (perf / avail)

            percs.append(perc_complete_bar)
            percs_labels.append(f"{perf:>3}/{avail:>3}\n{perc_complete_label:>5.1%}")

            uncompleted.append(perc_avail - perc_complete_bar)
            uncompleted_labels.append(
                f"{avail:>3}/{total_games:>3}\n{perc_avail:>5.1%}"
            )

        if venue_mode_dict is not None and venue in venue_mode_dict.keys():
            mode_str = " " + venue_mode_dict[venue]
        else:
            mode_str = ""

        create_bar_plot(
            f"{title} - {venue} {mode_str}",
            [percs, uncompleted],
            [m.name for m in MISSION_LETTERS_TO_ENUM.values()],
            bar_labels=[percs_labels, uncompleted_labels],
            colors=["xkcd:green", "xkcd:light grey"],
            percentage=True,
        )
