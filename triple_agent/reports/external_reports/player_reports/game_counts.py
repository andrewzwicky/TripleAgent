import os

from triple_agent.constants.paths import PLAYER_REPORT_FOLDER
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from triple_agent.reports.generation.generate_external_reports import (
    generate_external_reports,
)


def _count_games(games, data_dictionary):
    data_dictionary["Count"] += len(games)


def player_game_count_reports(all_replays, scl5_replays):
    generate_external_reports(
        scl5_replays,
        DataQueryProperties(query_function=_count_games, groupby=lambda game: game.spy),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_game_count_scl5.json"),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_game_count_scl5.html"),
    )

    generate_external_reports(
        all_replays,
        DataQueryProperties(query_function=_count_games, groupby=lambda game: game.spy),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_game_count_all.json"),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_game_count_all.html"),
    )
