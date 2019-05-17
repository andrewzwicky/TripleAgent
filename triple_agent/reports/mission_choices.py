from collections import defaultdict, Counter
from typing import List, Dict

from triple_agent.reports.report_utilities import create_bar_plot
from triple_agent.utilities.game import Game
from triple_agent.utilities.missions import MISSION_LETTERS_TO_ENUM, Missions


def print_mission_choices(
    games: List[Game], title: str, venue_mode_dict: Dict[str, str] = None
):
    # TODO: make this more flexible for different setups, filter out 5/8 for example.
    mission_choices = defaultdict(Counter)
    venue_mode_counts = Counter()

    for game in games:
        if venue_mode_dict is None or (
            game.venue in venue_mode_dict.keys()
            and game.game_type == venue_mode_dict[game.venue]
        ):
            venue_mode_counts[(game.venue, game.game_type)] += 1
            for mission in Missions:
                if game.picked_missions & mission:
                    mission_choices[(game.venue, game.game_type)][mission] += 1

    for (venue, mode), picks in mission_choices.items():
        percs = []
        avail = venue_mode_counts[(venue, mode)]
        picked_counts = []

        for _, mission in MISSION_LETTERS_TO_ENUM.items():
            picked = picks[mission]
            picked_counts.append(picked)
            perc = 0 if avail == 0 else picked / avail
            percs.append(perc)

        create_bar_plot(
            f"{title} - {venue} {mode}",
            [percs],
            [m.name for m in MISSION_LETTERS_TO_ENUM.values()],
            bar_labels=[picked_counts],
            percentage=True,
        )
