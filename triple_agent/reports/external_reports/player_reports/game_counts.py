import os

from triple_agent.constants.paths import PLAYER_REPORT_FOLDER
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from triple_agent.reports.generation.generate_external_reports import (
    generate_external_reports,
)


def _count_games(games, data_dictionary):
    data_dictionary["Count"] += len(games)


def player_game_count_reports(replays, report_name):
    generate_external_reports(
        replays,
        DataQueryProperties(query_function=_count_games, groupby=lambda game: game.spy),
        os.path.join(PLAYER_REPORT_FOLDER, f"{report_name}.json"),
        os.path.join(PLAYER_REPORT_FOLDER, f"{report_name}.html"),
    )
