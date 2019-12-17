import os

from triple_agent.constants.paths import PLAYER_REPORT_FOLDER
from triple_agent.reports.specific.character_selection import _determine_spy
from triple_agent.reports.generation.plot_specs import DataQueryProperties
from reports.generation.generate_external_reports import generate_external_reports


def generate_player_spy_selection_report(all_replays, scl5_replays):
    generate_external_reports(
        scl5_replays,
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_selection_scl5.json"),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_selection_scl5.html"),
    )

    generate_external_reports(
        all_replays,
        DataQueryProperties(
            query_function=_determine_spy,
            groupby=lambda game: game.spy,
            percent_normalized_data=True,
        ),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_selection_all.json"),
        os.path.join(PLAYER_REPORT_FOLDER, "spy_selection_all.html"),
    )
